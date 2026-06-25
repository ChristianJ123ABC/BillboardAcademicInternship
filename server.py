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

#Two Factor Authentication
#https://cryptography.io/en/latest/fernet/
#https://www.geeksforgeeks.org/python/fernet-symmetric-encryption-using-cryptography-module-in-python/
#https://www.freecodecamp.org/news/how-to-implement-two-factor-authentication-in-your-flask-app/
#https://pyauth.github.io/pyotp/
#https://github.com/pyauth/pyotp

#FUTURE NOTES: DOCKER ISSUES
#Command to fix flask_mysqldb issues with docker: ADD INTO dockerfile UNDER WORKDIR /app
#RUN apt-get update && apt-get install -y --no-install-recommends \
    #build-essential \
    #default-libmysqlclient-dev \
    #pkg-config \
    #&& rm -rf /var/lib/apt/lists/*

#app.run(debug=True, host = "0.0.0.0", port=5000) #shows bugs / errors on CMD + runs on all addresses

#Compose.yaml: ADD INTO UNDER CONTEXT
#ports:
  #    - 5000:5000
  # env_file:
  #   - .env

#Steps to run the server with docker:
#1. Install docker desktop
#2 clone the github and go into terminal and cd "location of repo"
#3 create a .env with the railway credentials
#4 run "docker compose up --build" in the terminal in VSC
#5 server will run

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


#pip install pyotp
#pip install pillow
import pyotp, qrcode
import stripe #pip install stripe

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
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
mysql = MySQL(app)

#Used to create 2FA secret key
f = Fernet(os.getenv("TOTP_ENCRYPTION_KEY").encode())


#Encryption + Decryption Functions
def encrypt2FA(plaintext):
    return f.encrypt(plaintext.encode()).decode()

def decrypt2FA(ciphertext):
    return f.decrypt(ciphertext.encode()).decode()

#Extensions used when uploading files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'mov', 'mkv',}
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
            cursor.execute("INSERT into users (email, hashed_password, firstName, lastName, businessName, 2fa_enabled) VALUES (%s, %s, %s, %s, %s,%s)", (email, hashedPass, firstName, lastName, businessName, 0)) #The 0 is used to set the 2FA to disabled on a new account
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
            #Creates temporary details to use for verifying the 2FA Code (prevent them from fully logging in without 2FA)
            if(user["2fa_enabled"] == True):
                session["pending_user_id"] = user["id"]
                session["pending_firstName"] = user["firstName"]
                session["pending_lastName"] = user["lastName"]
                session["pending_businessName"] = user["businessName"]
                session["pending_email"] = user["email"]
                return redirect(url_for("login_2fa"))
            
            #Logs the user in if they don't have 2FA
            session["user_id"] = user["id"]
            session["firstName"] = user["firstName"]
            session["lastName"] = user["lastName"]
            session["businessName"]  = user["businessName"]
            session["email"] = user["email"]
            
            flash("Login Successful!", "success")
            return redirect(url_for("dashboard"))
        
#2FA Section (Login, Verification/Setup, Enable/Disable)
@app.route("/login/2fa", methods = ["GET", "POST"])
def login_2fa():

    #Checks for user if they tried to login with 2FA
    if "pending_user_id" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users where id = %s", (session["pending_user_id"],))
        user = cursor.fetchone()
        cursor.close()

        #Decrypts the user's 2FA secret code and compares it to the authenticators code to see if it matches
        secret = decrypt2FA(user["2fa_secret"])
        if pyotp.TOTP(secret).verify(request.form["code"]):
            session.pop("pending_user_id")
            session["user_id"] = user["id"]
            session["firstName"] = session.pop("pending_firstName")
            session["lastName"] = session.pop("pending_lastName")
            session["businessName"] = session.pop("pending_businessName")
            session["email"] = session.pop("pending_email")
            flash("Login Successful!", "success")
            return redirect(url_for("dashboard"))
        
        else:
            flash("Invalid code.", "error")

    return render_template("2fa_login.html")

@app.route("/setup2FA")
def setup2FA():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (session["user_id"],))
    user = cursor.fetchone()
    cursor.close()

    #Checks if the user already has 2FA enabled
    if user["2fa_enabled"] != 0:
        flash("2FA is already enabled", "error")
        return redirect(url_for("dashboard"))
        
    #Creates the user's 2FA secret code and stores it in their database to use for verification later on.
    secret = pyotp.random_base32()

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET 2fa_secret = %s WHERE id = %s",
                   (encrypt2FA(secret), session["user_id"]))
    mysql.connection.commit()
    cursor.close()

    #Uses their secret code to generate a QR Code to scan onto their phone and use a code to login to their account
    uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=session["email"], issuer_name="Billboard Advertisement"
    )
    img = qrcode.make(uri)
    buf = BytesIO()
    img.save(buf, format="PNG")
    qr_b64 = base64.b64encode(buf.getvalue()).decode()

    return render_template("2fa_setup.html", qr_code=qr_b64)

@app.route("/setup2FA/verify", methods=["GET","POST"])
def verify_2fa():
    if "user_id" not in session:
        return redirect(url_for("login"))

    #Decrypts the user's 2FA secret code and compares it to the authenticators code to see if it matches, then it will enable 2FA onto their account if it does.
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT 2fa_secret FROM users WHERE id = %s", (session["user_id"],))
    user = cursor.fetchone()

    secret = decrypt2FA(user["2fa_secret"])
    if pyotp.TOTP(secret).verify(request.form["code"]):
        cursor.execute("UPDATE users SET 2fa_enabled = 1 WHERE id = %s", (session["user_id"],))
        mysql.connection.commit()
        cursor.close()
        flash("2FA has been enabled!", "success")
        return redirect(url_for("dashboard"))
    
    else:
        cursor.close()
        flash("Invalid code. Try again.", "error")
        return redirect(url_for("setup2FA"))

@app.route("/disable2FA")
def disable2FA():
    return render_template("2fa_disable.html")

@app.route("/disable2FA/deactivate", methods = ["POST"])
def deactivate2FA():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT 2fa_secret FROM users WHERE id = %s", (session["user_id"],))
    user = cursor.fetchone()

    #Decrypts the user's 2FA secret code and compares it to the authenticators code to see if it matches. if it does, it will remove the secret and turn their account into a non-2fa account
    secret = decrypt2FA(user["2fa_secret"])
    if pyotp.TOTP(secret).verify(request.form["code"]):
        cursor.execute("UPDATE users SET 2fa_enabled = 0, 2fa_secret = 0 WHERE id = %s",
                       (session["user_id"],))
        mysql.connection.commit()
        cursor.close()
        flash("2FA disabled. We recommend you remove your authenticator account since it is now invalid.", "success")
        return redirect(url_for("dashboard"))
    
    else:
        cursor.close()
        flash("Invalid code.", "error")

    return redirect(url_for("disable2FA"))

@app.route("/")

#Dashboard for users
@app.route("/dashboard")
def dashboard():
    #Checks if user is logged in
    if "user_id" not in session:
        flash("Please log in to access the dashboard", "error")
        return redirect(url_for("login"))
    
    else:
        
        user_id = session["user_id"]
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT advert_id, file, caption FROM advertisements WHERE user_id = %s", (user_id,))
        advertisements = cursor.fetchall()

        cursor.execute("""SELECT 2fa_enabled, subscription_plan, uploads_used, subscription_expiry FROM users WHERE id=%s """, (user_id,))
        user = cursor.fetchone()
        cursor.close()
        
        return render_template("dashboard.html", advertisements = advertisements, check2FA=user["2fa_enabled"],
    plan=user["subscription_plan"],uploads=user["uploads_used"], expiry=user["subscription_expiry"])
    


#Page for users to display their advertisments
@app.route("/uploadAdvertisement", methods = ["GET", "POST"])
def uploadAdvertisement():

    #Reminder: add in a check to see if they are subscribed to upload advertisements once upload works
   # if request.method == "GET":
    #    cursor = mysql.connection.cursor()
     #   user_id = session["user_id"]
    
    if request.method == "GET":
        return render_template("uploadAdvertisement.html")

    #Validation for files
    else:
        if request.method == "POST":
            user_id = session["user_id"]
            
            #
            #
            #Start: prakash code
            #Get user's subscription information
            cursor = mysql.connection.cursor()

            cursor.execute("""
                SELECT subscription_plan,
                       uploads_used,
                       subscription_expiry
                FROM users
                WHERE id = %s
            """, (user_id,))

            user = cursor.fetchone()

            #Check if subscription has expired
            if user["subscription_expiry"] is not None:

                from datetime import datetime

                if user["subscription_expiry"] < datetime.now():

                    flash("Your subscription has expired. Please renew your plan.", "error")

                    cursor.close()

                    return redirect(url_for("subscription"))

            #Upload limits for each plan
            limits = {
                "Basic": 2,
                "Standard": 5,
                "Premium": 999999
            }

            currentPlan = user["subscription_plan"]
            uploadsUsed = user["uploads_used"]

            #Get upload limit for current plan
            uploadLimit = limits.get(currentPlan, 0)

            #Prevent uploads if limit reached
            if uploadsUsed >= uploadLimit:

                flash(
                    f"You have reached the upload limit for the {currentPlan} plan.",
                    "error"
                )

                cursor.close()

                return redirect(url_for("dashboard"))
                # End : prakash code
                #
                #

            file = request.files['file']
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            
            #No file selected
            if not file or file.filename == '':
                flash("No file selected", "error")
                return redirect(url_for("uploadAdvertisement"))
            
            if not allowedFile(file.filename):
                flash("Invalid image type, use the following image extensions: 'png', 'jpg', 'jpeg', 'mp4', 'mov', 'mkv' ", "error")
                return redirect(url_for("uploadAdvertisement"))
            
            #Create filepath to store in database
            file.save(filepath)
            uploadFilePath = os.path.join('uploads', file.filename)

            #Insert image into database
            cursor = mysql.connection.cursor()
            caption = request.form.get('caption')
            cursor.execute("INSERT INTO advertisements (file, caption, user_id) VALUES (%s, %s,%s)", (uploadFilePath, caption, user_id))
            mysql.connection.commit()
            cursor.close()
            
            flash("Image uploaded successfully", 'success')
            return redirect(url_for('uploadAdvertisement'))
    
#Used to remove a user's advertisement if they so please
@app.route('/deleteFile/<int:id>')
def deleteFile(id):
    root = os.path.dirname(os.path.abspath(__file__))
        
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT file FROM advertisements WHERE advert_id = %s", (id,))
    adFile = cursor.fetchone()
    fileName = adFile['file'] 
    

    filePath = os.path.join(root,'static', fileName)
    os.remove(filePath)

    cursor.execute("DELETE FROM advertisements WHERE advert_id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    flash('File successfully deleted!', 'success')

    return redirect(url_for("dashboard"))

#END: Code created by Christian



#START: Code created by Prakash






# SUBSCRIPTION

@app.route("/subscription")
def subscription():

    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT subscription_plan,
               uploads_used
        FROM users
        WHERE id=%s
    """, (session["user_id"],))

    user = cursor.fetchone()

    cursor.close()

    return render_template(
        "subscription.html",
        user=user
    )


@app.route("/choose-plan/<plan>")
def choose_plan(plan):

    if "user_id" not in session:
        return redirect(url_for("login"))

    valid_plans = ["Basic", "Standard", "Premium"]

    if plan not in valid_plans:
        flash("Invalid subscription plan", "error")
        return redirect(url_for("subscription"))

    start_date = datetime.now()
    expiry_date = start_date + timedelta(days=30)

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE users
        SET subscription_plan=%s,
            uploads_used=0,
            subscription_start=%s,
            subscription_expiry=%s
        WHERE id=%s
    """, (
        plan,
        start_date,
        expiry_date,
        session["user_id"]
    ))

    mysql.connection.commit()
    cursor.close()

    flash(f"{plan} plan activated successfully!", "success")

    return redirect(url_for("dashboard"))




# SCHEDULING ROUTE

@app.route("/scheduling")
def scheduling():

    return render_template("scheduling.html")


# ANALYTICS ROUTE

@app.route("/analytics")
def analytics():

    return render_template("analytics.html")        
       

#END: Code created by Prakash       




@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))
  

#makes it so that it only runs the app when executed
if __name__ == "__main__":
    app.run(debug=True, host = "0.0.0.0", port=5000) #shows bugs / errors on CMD + runs on all addresses
    


