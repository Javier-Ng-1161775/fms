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
    qstr = "select id, name from mobs;" 
    connection.execute(qstr)        
    mobs = connection.fetchall()        
    return render_template("mobs.html", mobs=mobs)  

@app.route("/paddocks")
def paddocks():
    """List paddock details."""
    return render_template("paddocks.html")  


