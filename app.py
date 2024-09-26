from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from datetime import date, datetime, timedelta
import mysql.connector
import connect

app = Flask(__name__)
app.secret_key = 'COMP636 S2'

start_date = datetime(2024,10,29)
pasture_growth_rate = 65    #kg DM/ha/day
stock_consumption_rate = 14 #kg DM/animal/day

db_connection = None
 
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
    # cursor = db_connection.cursor(dictionary=True, buffered=False)
   
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
    if 'curr_date' not in session:
        session.update({'curr_date': start_date})
    return render_template("home.html")

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

@app.route("/mobs")
def mobs():
    """List the mob details (excludes the stock in each mob)."""
    connection = getCursor()        
    qstr = """
            SELECT m.id, m.name, p.name
            FROM mobs m
            JOIN paddocks p ON m.paddock_id = p.id
            ORDER BY m.name ASC;
            """
    connection.execute(qstr)        
    mobs = connection.fetchall()        
    return render_template("mobs.html", mobs=mobs)  

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
    qstr_stock_details = "SELECT id, mob_id, dob, weight FROM stock;"
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
    return render_template("paddocks.html")  


