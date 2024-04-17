from flask import Flask, abort, flash, render_template, redirect, request, session
from repositories import loginSql, userProfileSql, viewDrives, deleteSql, viewIndividualDrive, drives
from repositories.leaderboard import get_leaders
from repositories.edit_drive import edit_drive_values, get_drive, get_vehicles


from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import uuid, os

load_dotenv()


app = Flask(__name__)
global username
username = None
global firstname
global lastname
firstname = None
lastname = None

app.secret_key = os.getenv('SECRET_KEY')


bcrypt = Bcrypt(app)

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
    drives = viewDrives.get_all_drives()
    return render_template("viewDrives.html", title="Drives", drives = drives)

@app.get("/drive/<drive_id>")
def individual(drive_id):
    individualDrive = viewIndividualDrive.get_individual_drive_by_id(drive_id)
    return render_template("individualDrive.html", title ="Individual Drive", drive = individualDrive)

@app.get ("/userprofile")
def user_profile():
    if 'username' not in session:
        return redirect("/login")
    global firstname
    global lastname
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

@app.post("/edit")
def edit_drive_form():
    drive_id = request.form.get("drive_id")
    drive = get_drive(drive_id)
    vehicles = get_vehicles(drive['username'])
    print(drive)
    return render_template("editdrive.html", title="Edit Drive", drive = drive, vehicles = vehicles)

@app.post("/")
def edit_drive():
    drive_id = request.form.get("drive_id")
    drive = get_drive(drive_id)
    if drive_id == '':
        drive_id = drive['drive_id']
        
    mileage = request.form.get("mileage")
    if mileage == '':
        mileage = drive['mileage']

    duration = request.form.get("duration")
    if duration == '':
        duration = drive['duration']

    vehicle = request.form.get("vehicleSelect")
    if vehicle == '':
        vehicle = drive['vehicle_id']

    title = request.form.get("titleDrive")
    if title == '':
        title = drive['title']

    caption = request.form.get("captionDrive")
    if caption == '':
        caption = drive['caption']
    

    # # tags
    # drive_id = request.form.get("drive_id") 
    # drive_id = request.form.get("drive_id")
    # drive_id = request.form.get("drive_id")
    # drive_id = request.form.get("drive_id")
    # drive_id = request.form.get("drive_id")
    print(drive_id, mileage, duration, vehicle, title, caption)
    print("Testing")
    edit_drive_values(drive_id, mileage, duration, vehicle, title, caption)
    
    return redirect('/userprofile') 