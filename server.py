#Sources:
#Psycog setup
#https://www.psycopg.org/docs/install.html

#regex for email validation
#https://www.zerobounce.net/email-guides/python-email-verification

#Register / Login
#https://www.geeksforgeeks.org/python/login-and-registration-project-using-flask-and-mysql/
#https://stackoverflow.com/questions/59380641/how-to-display-full_name-in-multiple-pages-using-flask
#https://stackoverflow.com/questions/37227780/flask-session-persisting-after-close-browser


#Connection to database
#https://www.geeksforgeeks.org/python/flask-app-configuation/app.

#Uploading / deleting files
#https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
#https://www.youtube.com/watch?v=2De9Lu9tReg
#https://www.youtube.com/watch?v=YLptAhf3wwM&t=963s



#START: CODE COMPLETED BY CHRISTIAN
from flask import Flask, render_template, redirect, url_for, request, session, flash #pip install flask
from flask_mysqldb import MySQL #pip install flask_mysqldb  (PYTHON 3.11)
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, redirect, request, render_template
from flask import request, jsonify
import os, base64
from datetime import timedelta, datetime
import re
from io import BytesIO
from io import BytesIO
import string, random
from dotenv import load_dotenv #pip install python-dotenv #used to load from .env file for security reasons (NEW THING I LEARNED)
load_dotenv(override=True)

#Fix for .env errors with railway: break down the public url into the root, host, password, etc and use that.

#pip install cryptography
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC 
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

#START: Code created by Christian
#Used to access the Database 

#Grabs information from .env file to access the database.
app = Flask(__name__, template_folder='templates')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT'))
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = os.getenv("SECRET_KEY") 
mysql = MySQL(app)



#Extensions used when uploading files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'mov', 'avi', 'mkv', 'webm'}
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')

#Validation Functions
#Format: email@domain.com / name.last@domain.co.uk
def validEmail(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

def existingEmail(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    return user


def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#Default page when you open the website and not logged in
@app.route("/")
def home():
    return redirect(url_for("login"))


#Register
@app.route("/register", methods=["GET","POST"])
def register():

    #Message if user tries to create account whilst logged in
    if "user_id" in session:
        flash("You must log out to create another account", 'warning')
        return redirect(url_for("dashboard"))
    
    #displays register page
    if request.method == "GET":
        return render_template("register.html")
    
    else:
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["email"]
        password = request.form["password"]
        businessName = request.form["businessName"]
        hashedPass = generate_password_hash(password)

        #Validation checks for email
        if not validEmail(email):
            flash("Invalid Email Format, use the following (email@domain.com / name.last@domain.co.uk)", "error")
            return render_template("register.html", businessName = businessName, firstName = firstName, lastName = lastName, email = email) #Keeps the input fields the same except password
        
        elif existingEmail(email):
            flash("Email is already registered", "error")
            return render_template("register.html", businessName = businessName, firstName = firstName, lastName = lastName, email = email) 

        #Validation checks for passwords
        elif re.search(r'[0-9]', password) is None:
            flash("Password has to contain atleast 1 number.")
            return render_template("register.html", businessName = businessName, firstName = firstName, lastName = lastName, email = email) 
            
        elif re.search(r'[a-z]', password) is None:
            flash("Password has to contain atleast 1 lowercase letter.")
            return render_template("register.html", businessName = businessName, firstName = firstName, lastName = lastName, email = email) 

        elif re.search(r'[A-Z]', password) is None:
            flash("Password has to contain atleast 1 uppercase letter.")
            return render_template("register.html", businessName = businessName, firstName = firstName, lastName = lastName, email = email) 

        #regex: https://owasp.org/www-community/password-special-characters
        elif re.search(r'[!"#$%&\'()*+,\-./:;<=>?@^_|~>]', password) is None:
            flash("Password has to contain atleast 1 special character.")
            return render_template("register.html", businessName = businessName, firstName = firstName, lastName = lastName, email = email) 

        elif len(password) < 15 or len(password) > 30:
            flash("Password has to be between 15 and 30 characters.")
            return render_template("register.html", businessName = businessName, firstName = firstName, lastName = lastName, email = email) 
        
        else:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT into users (email, hashed_password, firstName, lastName, businessName) VALUES (%s, %s, %s, %s, %s)", (email, hashedPass, firstName, lastName, businessName))
            mysql.connection.commit()

            flash(("Account Created Successfully!"), "success")
            return render_template("login.html")
        


#Login
@app.route("/login", methods = ["GET", "POST"])
def login():
    #Message if user tries to login again if they are already logged in
    if "user_id" in session:
        flash("You are already logged in", "warning")
        return redirect(url_for("dashboard"))

    if request.method == "GET":
        return render_template("login.html")
    
    else:
        #Grab email and password from form fields
        email = request.form["email"]
        password = request.form["password"]

        #Validation for form fields
        if not email or not password:
            flash("Please enter email and password", "error")
            return render_template("login.html")
        

        #Search for user
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        #User not found
        if not user:
            flash("Invalid Email Address", "error")
            return render_template("login.html")
        
        #Invalid password
        elif not check_password_hash(user["hashed_password"], password):
            flash("Incorrect password", "error")
            return render_template("login.html")
        
        #If all login details are valid:
        else:
            session["user_id"] = user["userID"]
            session["firstName"] = user["firstName"]
            session["lastName"] = user["lastName"]
            session["businessName"]  = user["businessName"]
            session["email"] = user["email"]
            
            flash("Login Successful!", "success")
            return redirect(url_for("dashboard"))


#Dashboard for users
@app.route("/dashboard")
def dashboard():
    #Checks if user is logged in
    if "user_id" not in session:
        flash("Please log in to access the dashboard", "error")
        return redirect(url_for("login"))
    
    else:
        return render_template("dashboard.html")
    


#Page for users to display their advertisments
@app.route("/uploadAdvertisement", methods = ["GET", "POST"])
def uploadAdvertisement():

    #Reminder: add in a check to see if they are subscribed to upload advertisements once upload works
   # if request.method == "GET":
    #    cursor = mysql.connection.cursor()
     #   user_id = session["user_id"]
    
    #Validation for files
    if request.method == "POST":
        file = request.files['image']
        filepath = os.path.join(app.config['UPLOAD_FOLDER']), image.filename)
        
        #No file selected
        if not file or file.filename == '':
            flash("No file selected", "error")
            return redirect(url_for("uploadAdvertisment"))
        
        if not allowedFile(file.filename):
            flash("Invalid image type, use the following image extensions: 'png', 'jpg', 'jpeg', 'mp4', 'mov', 'avi', 'mkv', 'webm' ", "error")
            return redirect(url_for("uploadAdvertisement"))
        
        file.save(filepath)
        uploadFilePath = os.path.join('uploads', file.filename)

        
        


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))
  

#makes it so that it only runs the app when executed
if __name__ == "__main__":
    app.run(debug=True) #shows bugs / errors on CMD


#END: Code created by Christian
