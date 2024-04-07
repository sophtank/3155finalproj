from flask import Flask, redirect, render_template, request
from repositories import loginSql

app = Flask(__name__)
global username
username = None

@app.get("/")
def index():
    return render_template("index.html", title ="Home")

@app.get("/login")
def login():
    return render_template("login.html", title="Login")

@app.post('/loggedIn')
def loggedIn():
    username = request.form.get("username")
    password = request.form.get("password")
    loginAttempt = loginSql.login(username, password)
    if(loginAttempt == []):
        return redirect("/login")
    else:
        print("Logged In")
        return redirect("/userprofile")

#renders the signup page
@app.get("/signup")
def signup():
    return render_template("signup.html", title="Sign-Up")

#after the user signs up the user is redirected to the home page
@app.post("/Signedup")
def signedup():
    firstname = request.form.get("FirstName")
    lastname = request.form.get("LastName")
    username = request.form.get("username")
    password = request.form.get("password")
    if(loginSql.checkIFUserExists(username) != []):
        print("User already exists")
    else:
        loginSql.SignUp(username, password, firstname, lastname)
    return redirect("/userprofile")

@app.get("/leaderboard")
def leaderboard():
    return render_template("LeaderBoard.html", title="Leaderboard")

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
    return render_template("UserProfile.html", title = "User profile")

@app.get("/edit")
def edit():
    return render_template("editdrive.html", title="Edit Drive")