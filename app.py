from flask import Flask, abort, flash, render_template, redirect, request, session
from repositories import loginSql
from repositories import userProfileSql
from repositories.leaderboard import get_leaders
from flask_bcrypt import Bcrypt
import os


app = Flask(__name__)
global username
username = None
global firstname
global lastname
firstname = None
lastname = None

app.secret_key = os.getenv('SECRET_KEY')


bcrypt = Bcrypt(app)


def createDummyData():
    username1 = "testing1"
    password1 = "password1"
    firstname1 = "John"
    lastname1 = "Doe"
    hashed_password1 = bcrypt.generate_password_hash(password1).decode('utf-8')
    loginSql.SignUp(username1, hashed_password1, firstname1, lastname1)

    username2 = "testing2"
    password2 = "password2"
    firstname2 = "Jane"
    lastname2 = "Doe"
    hashed_password2 = bcrypt.generate_password_hash(password2).decode('utf-8')
    loginSql.SignUp(username2, hashed_password2, firstname2, lastname2)

    username3 = "testing3"
    password3 = "password3"
    firstname3 = "John"
    lastname3 = "Smith"
    hashed_password3 = bcrypt.generate_password_hash(password3).decode('utf-8')
    loginSql.SignUp(username3, hashed_password3, firstname3, lastname3)

    username4 = "testing4"
    password4 = "password4"
    firstname4 = "Jane"
    lastname4 = "Smith"
    hashed_password4 = bcrypt.generate_password_hash(password4).decode('utf-8')
    loginSql.SignUp(username4, hashed_password4, firstname4, lastname4)

createDummyData()


@app.get("/")
def index():
    return render_template("index.html", title ="Home")

@app.get("/login")
def login():
    return render_template("login.html", title="Login")

@app.post('/loggedIn')
def loggedIn():
    global username 
    global firstname
    global lastname
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        abort(400, "Username and password are required")
    loginAttempt = loginSql.login(username)
    if loginAttempt == []:
        return redirect("/login")
    if(bcrypt.check_password_hash(loginAttempt[0]['password'], password)):
        firstname = loginAttempt[0]['first_name']
        lastname = loginAttempt[0]['last_name']
        #sessions
        session['username'] = loginAttempt[0]['username']
        return redirect("/userprofile")
    else:
        return redirect("/login")

#renders the signup page
@app.get("/signup")
def signup():
    return render_template("signup.html", title="Sign-Up")

#after the user signs up the user is redirected to the home page
@app.post("/Signedup")
def signedup():
    global firstname
    global lastname
    firstname = request.form.get("FirstName")
    lastname = request.form.get("LastName")
    global username
    username = request.form.get("username")
    password = request.form.get("password")
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    if(loginSql.checkIFUserExists(username) != []):
        abort(400, "User already exists")
    else:
        loginSql.SignUp(username, hashed_password, firstname, lastname)
    return redirect("/userprofile")

@app.get("/leaderboard")
def leaderboard():
    leaders = get_leaders()
    return render_template("LeaderBoard.html", title="Leaderboard", leaders=leaders)

@app.get("/create")
def create():
    return render_template("createdrive.html", title="Create Drive")

@app.get("/drives")
def get_all_drives():
    return render_template("viewDrives.html", title="Drives")

@app.get("/viewDrive")
def individual():
    return render_template("individualDrive.html", title ="Individual Drive")

@app.get ("/userprofile")
def user_profile():
    if 'username' not in session:
        return redirect("/login")
    global firstname
    global lastname
    alldrives = userProfileSql.getAllDrives(username)
    return render_template("UserProfile.html", title = "User profile", alldrives = alldrives, firstname = firstname, lastname = lastname)

@app.get("/edit")
def edit():
    return render_template("editdrive.html", title="Edit Drive")