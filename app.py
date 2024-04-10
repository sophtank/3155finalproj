from flask import Flask, redirect, render_template, request
from dotenv import load_dotenv
from repositories import loginSql
from repositories import userProfileSql
from repositories import drives
import uuid, os

load_dotenv()

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
    global username 
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
    global username
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

@app.post("/creating")
def creating():
    drive_id = str(uuid.uuid4())
    vehicle_id = 'ffa2b0b9-efd5-4dc9-b947-d9a25af99692' #temporary until we implement sessions
    mileage = request.form.get("mileage")
    duration = request.form.get("duration")
    title = request.form.get("titleDrive")
    caption = request.form.get("captionDrive")
    #vehicle_id = request.form.get("vehicleSelect")
    photo = "https://img.freepik.com/free-photo/luxurious-car-parked-highway-with-illuminated-headlight-sunset_181624-60607.jpg" #temp until we figure out how to store photos
    #current date and time
    date = "NOW()"
    user = "stanker" #temporary until we implement sessions
    drives.create_drive(drive_id, vehicle_id, mileage, duration, title, caption, photo, date, user)
    return redirect("/userprofile")

@app.get("/drives")
def get_all_drives():
    return render_template("viewDrives.html", title="Drives")

@app.get("/viewDrive")
def individual():
    return render_template("individualDrive.html", title ="Individual Drive")

@app.get ("/userprofile")
def user_profile():
    print(username)
    alldrives = userProfileSql.getAllDrives(username)
    print(alldrives)
    return render_template("UserProfile.html", title = "User profile", alldrives = alldrives)

@app.get("/edit")
def edit():
    return render_template("editdrive.html", title="Edit Drive")