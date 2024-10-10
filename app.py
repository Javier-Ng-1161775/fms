from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from datetime import date, datetime, timedelta
import mysql.connector
import connect

from pathlib import Path

app = Flask(__name__)
app.secret_key = 'COMP636 S2'

start_date = datetime(2024,10,29)
pasture_growth_rate = 65    #kg DM/ha/day
stock_consumption_rate = 14 #kg DM/animal/day

db_connection = None

def get_date():
    cursor = getCursor()        
    qstr = "select curr_date from curr_date;"  
    cursor.execute(qstr)        
    curr_date = cursor.fetchone()[0]        
    return curr_date

def getCursor():
    """Gets a new dictionary cursor for the database.
    If necessary, a new database connection is created here and used for all
    subsequent to getCursor()."""
    global db_connection
 
    if db_connection is None or not db_connection.is_connected():
        db_connection = mysql.connector.connect(user=connect.dbuser, \
            password=connect.dbpass, host=connect.dbhost,
            database=connect.dbname, autocommit=True)
       
    cursor = db_connection.cursor(buffered=False)   # returns a list
   
    return cursor

def calculate_age(dob):
    if dob is None:
        return None
    if isinstance(dob, datetime):
        dob_datetime = dob
    else:
        dob_datetime = datetime.combine(dob, datetime.min.time())  # Convert to datetime
    age = (start_date - dob_datetime).days // 365  # Calculate age in years
    return age

@app.route("/")
def home():
    # Check if the current date is in the session; if not, set it to start_date
    if 'curr_date' not in session:
        session['curr_date'] = start_date
    
    # Use the session value for curr_date
    curr_date = session['curr_date']
    
    return render_template("home.html", curr_date=curr_date)

@app.route("/clear-date")
def clear_date():
    """Clear session['curr_date']. Removes 'curr_date' from session dictionary."""
    session.pop('curr_date')
    return redirect(url_for('paddocks'))  

@app.route("/reset-date")
def reset_date():
    """Reset session['curr_date'] to the project start_date value."""
    session.update({'curr_date': start_date})
    return redirect(url_for('paddocks'))  

@app.route("/reset")
def reset():
    """Reset data to original state."""
    THIS_FOLDER = Path(__file__).parent.resolve()
    with open(THIS_FOLDER / 'fms-reset.sql', 'r') as f:
        mqstr = f.read()
        for qstr in mqstr.split(";"):
            cursor = getCursor()
            cursor.execute(qstr)
    get_date()

    return redirect(url_for('paddocks'))  

@app.route("/mobs")
def mobs():
    """List the mob details (excludes the stock in each mob)."""
    connection = getCursor()        
    qstr_mobs = """
    SELECT 
        m.id, m.name, p.name
    FROM 
        mobs m
    JOIN 
        paddocks p ON m.paddock_id = p.id
    ORDER BY 
        m.name ASC;
    """
    connection.execute(qstr_mobs)        
    mobs = connection.fetchall()

    # Fetch available paddocks
    qstr_available_paddocks = """
    SELECT * 
    FROM paddocks
    WHERE id NOT IN (SELECT paddock_id FROM mobs);
    """
    connection.execute(qstr_available_paddocks)
    available_paddocks = connection.fetchall()

    return render_template("mobs.html", mobs=mobs, available_paddocks=available_paddocks)

@app.route("/stocks")
def stocks():
    """List the stock details"""
    connection = getCursor()        
    qstr_mob = """
    SELECT 
        m.id AS mob_id,
        m.name AS mob_name, 
        p.name AS paddock_name,
        COUNT(s.id) AS number_of_stock, 
        ROUND(AVG(s.weight), 2) AS average_weight
    FROM 
        mobs m
    JOIN 
        paddocks p ON m.paddock_id = p.id
    LEFT JOIN 
        stock s ON m.id = s.mob_id
    GROUP BY 
        m.id, p.name
    ORDER BY 
        m.name ASC;
    """
    connection.execute(qstr_mob)        
    stocks = connection.fetchall()
    
    # Fetch detailed stock data
    qstr_stock_details = """
    SELECT 
        id, mob_id, dob, weight 
    FROM 
        stock 
    ORDER BY 
        id;
    """
    connection.execute(qstr_stock_details)
    stock_details = connection.fetchall()
    
    print(stock_details)

    # Calculate age for each stock detail
    stock_details_with_age = []
    for detail in stock_details:
        dob = detail[2]  
        age = calculate_age(dob)
        stock_details_with_age.append(detail + (age,))  # Append age as a new column
    
    connection.close()
    
    return render_template("stocks.html", stocks=stocks, stock_details=stock_details_with_age)

@app.route("/paddocks")
def paddocks():
    """List paddock details."""
    connection = getCursor()        
    qstr_paddocks = """
    SELECT 
        p.id AS paddock_id,
        p.name AS paddock_name,
        p.area AS paddock_area,
        p.dm_per_ha AS dm_per_ha,
        p.total_dm AS total_dm,
        m.name AS mob_name,
        COUNT(s.id) AS number_of_stock
    FROM 
        paddocks p
    LEFT JOIN 
        mobs m ON p.id = m.paddock_id
    LEFT JOIN 
        stock s ON m.id = s.mob_id
    GROUP BY 
        p.id, m.id
    ORDER BY 
        p.name ASC;
            """
    connection.execute(qstr_paddocks)        
    paddocks = connection.fetchall()     
    return render_template("paddocks.html", paddocks=paddocks)  

@app.route("/move_mob", methods=["POST"])
def move_mob():
    """Move a mob to a different paddock."""
    connection = None
 
    mob_id = request.form.get("mob_id")
    new_paddock_id = request.form.get("paddock_id")

    connection = getCursor()

    update_query = "UPDATE mobs SET paddock_id = %s WHERE id = %s"
    connection.execute(update_query, (new_paddock_id, mob_id))

    flash("Mob moved successfully!", "success")
    return redirect(url_for("mobs")) 

#create a paddocks/add route
@app.route("/add_paddock", methods=["GET", "POST"])
def add_paddock():
    """Route to add a new paddock."""
    if request.method == "POST":
        try:
            name = request.form.get("name")
            area = float(request.form.get("area"))
            dm_per_ha = float(request.form.get("dm_per_ha"))
            
            total_dm = area * dm_per_ha
            
            connection = getCursor()

            # Check if paddock with the same name already exists
            check_query = "SELECT * FROM paddocks WHERE name = %s"
            connection.execute(check_query, (name,))
            existing_paddock = connection.fetchone()

            if existing_paddock:
                flash(f"Paddock with name '{name}' already exists. Please choose a different name.", "danger")
                return redirect(url_for("add_paddock"))
         
            # Insert the new paddock into the database
            insert_query = """
            INSERT INTO paddocks (name, area, dm_per_ha, total_dm)
            VALUES (%s, %s, %s, %s)
            """
            connection.execute(insert_query, (name, area, dm_per_ha, total_dm))
            
            flash("Paddock added successfully!", "success")

        # Adding an error catch all 
        except Exception as e:
            print(f"Error adding paddock: {e}")
            flash("Failed to add paddock. Please try again.", "danger")

        return redirect(url_for("paddocks"))  # Redirect back to the paddocks page
    
    return render_template("add_paddock.html")

@app.route("/paddock_details", methods=['GET'])  # Uses the GET method to extract the data from the URL (after the ? in the URL)
def paddock_details():

    connection = getCursor()
    id = request.args.get('id')         
    qstr = "SELECT * FROM paddocks WHERE id = %s;"
    qargs = (id,)   
    connection.execute(qstr,qargs)      
    paddock_details = connection.fetchone()      
    return render_template("paddock_details.html", paddock_details=paddock_details)

@app.route("/paddock_details/edit", methods=['GET'])
def paddock_details_edit():

    connection = getCursor()
    id = request.args.get('id')
    qstr = "SELECT * FROM paddocks where id = %s;"
    qargs = (id,)
    connection.execute(qstr,qargs)
    paddock_details = connection.fetchone()
    return render_template("paddock_details_edit.html", paddock_details=paddock_details)   # This page displays a form that can return data.

@app.route("/paddock_details/edit/update", methods=['POST'])   
def paddock_details_edit_update():

    connection = getCursor()
    formvals = request.form    # Returns a dictionary of {form-element-name: value} pairs
    
    # Calculate the total DM based on area and dm_per_ha
    total_dm = float(formvals['area']) * float(formvals['dm_per_ha'])
    
    qstr = """update paddocks         
                set name = %s, area = %s, dm_per_ha = %s, total_dm = %s					
                where id = %s;"""   
    qargs = (formvals['name'], formvals['area'], formvals['dm_per_ha'], total_dm, formvals['id'])    
    connection.execute(qstr,qargs)          
                                            
    return redirect("/paddock_details?id="+formvals['id'])   

@app.route("/advance_date", methods=["POST"])
def advance_date():
    """Advance the current date by one day and recalculate pasture values."""
    global start_date
    start_date += timedelta(days=1)

    # Store the new current date in the session
    session['curr_date'] = start_date

    connection = getCursor()
    
    # Fetch all paddocks
    fetch_paddocks_query = """
    SELECT 
        p.id AS paddock_id,
        p.area AS paddock_area,
        p.total_dm AS total_dm,
        COUNT(s.id) AS number_of_stock
    FROM 
        paddocks p
    LEFT JOIN 
        mobs m ON p.id = m.paddock_id
    LEFT JOIN 
        stock s ON m.id = s.mob_id
    GROUP BY 
        p.id;
    """
    connection.execute(fetch_paddocks_query)
    paddocks = connection.fetchall()

    for paddock in paddocks:
        paddock_id = paddock[0]
        area = paddock[1]
        total_dm = paddock[2]
        number_of_stock = paddock[3]

        # Calculate growth and consumption
        growth = area * pasture_growth_rate
        consumption = number_of_stock * stock_consumption_rate

        # Recalculate total DM
        new_total_dm = total_dm + growth - consumption
        if new_total_dm < 0:
           new_total_dm = 0
         
        # Recalculate DM/ha
        new_dm_per_ha = new_total_dm / area if area > 0 else 0
        if new_dm_per_ha < 0:
           new_dm_per_ha = 0

        # Update paddock details in the database
        update_query = """UPDATE paddocks 
                          SET total_dm = %s, dm_per_ha = %s 
                          WHERE id = %s;"""
        connection.execute(update_query, (new_total_dm, new_dm_per_ha, paddock_id))

    flash("Current date advanced by one day, and pasture values recalculated!", "success")
    return redirect(url_for("paddocks"))  # Redirect to paddocks page
