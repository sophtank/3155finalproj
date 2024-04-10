from flask import Flask, render_template, redirect, request, abort
from repositories import loginSql
from repositories import userProfileSql
from repositories import viewDrives
from repositories.leaderboard import get_leaders
from repositories import deleteSql
from repositories import viewIndividualDrive
from dotenv import load_dotenv


app = Flask(__name__)
global username
username = None
global firstname
global lastname
firstname = None
lastname = None

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
    loginAttempt = loginSql.login(username, password)
    print(loginAttempt)
    if(loginAttempt == []):
        return redirect("/login")
    else:
        firstname = loginAttempt[0]["first_name"]
        lastname = loginAttempt[0]["last_name"]
        print("Logged In")
        return redirect("/userprofile")
    
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
    if(loginSql.checkIFUserExists(username) != []):
        print("User already exists")
    else:
        loginSql.SignUp(username, password, firstname, lastname)
        return redirect('/userprofile')

@app.get("/leaderboard")
def leaderboard():
    leaders = get_leaders()
    return render_template("LeaderBoard.html", title="Leaderboard", leaders=leaders)

@app.get("/create")
def create():
    return render_template("createdrive.html", title="Create Drive")

@app.get("/drives")
def get_all_drives():
    drives = viewDrives.get_all_drives()
    return render_template("viewDrives.html", title="Drives", drives = drives)

@app.get("/drive/<drive_id>")
def individual(drive_id):
    individualDrive = viewIndividualDrive.get_individual_drive_by_id(drive_id)
    return render_template("individualDrive.html", title ="Individual Drive", drive = individualDrive)

@app.get ("/userprofile")
def user_profile():
    global firstname
    global lastname
    print(username)
    alldrives = userProfileSql.getAllDrives(username)
    vehicles = userProfileSql.getVehicles(username)
    return render_template("UserProfile.html", title = "User profile", 
                        alldrives = alldrives, 
                        firstname = firstname, 
                        lastname = lastname,
                        vehicles = vehicles #passing in the vehicle to the user profile dropdown
                        )

#function to post selected vehicle to user profile & display waiting on sessions to finish up
@app.post('/userprofile')
def select_vehicle():
    vehicle_id = request.form.get("vehicle_id")
    username = request.form.get("Username")

    drives = userProfileSql.getAllDrives(username)
    if not drives:
        return redirect('/create')
    
    return redirect(f"/userprofile/{username}/{vehicle_id}")

# function to delete a drive based on drive id
@app.post('/drive/<drive_id>')
def delete_drive(drive_id):
    if not drive_id:
        abort(404)

    deleteSql.deleteDrive(drive_id) 
    return redirect("/drives")

@app.get("/edit")
def edit():
    return render_template("editdrive.html", title="Edit Drive")