from flask import Flask, abort, flash, render_template, redirect, request, session
from repositories import Vehicle, loginSql, userProfileSql, viewDrives, deleteSql, viewIndividualDrive, drives
from repositories.leaderboard import get_leaders
from repositories.edit_drive import edit_drive_values, get_drive, get_vehicles, edit_tag_values, get_tags


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

@app.get("/logout")
def logout():
    if not session:
        abort(401, "You are not logged in.")
    session.clear()
    return redirect('/')

@app.get("/leaderboard")
def leaderboard():
    leaders = get_leaders()
    return render_template("LeaderBoard.html", title="Leaderboard", leaders=leaders)

@app.get("/create")
def create():
    vehicles = Vehicle.getVehicles(username)
    return render_template("createdrive.html", title="Create Drive", vehicles=vehicles)

@app.post("/creating")
def creating():
    drive_id = str(uuid.uuid4())
    vehicle_id = request.form.get("vehicle_id")
    mileage = request.form.get("mileage")
    duration = request.form.get("duration")
    title = request.form.get("titleDrive")
    caption = request.form.get("captionDrive")
    photo = "https://img.freepik.com/free-photo/luxurious-car-parked-highway-with-illuminated-headlight-sunset_181624-60607.jpg" #temp until we figure out how to store photos
    #current date and time
    date = "NOW()"
    user = username
    drives.create_drive(drive_id, vehicle_id, mileage, duration, title, caption, photo, date, user)
    flash('Drive successfully created', 'success')
    commute = request.form.get("commute")
    if commute == None:
        commute = 'FALSE'
    near_death_experience = request.form.get("NDE")
    if near_death_experience == None:
        near_death_experience = 'FALSE'
    carpool = request.form.get("carpool")
    if carpool == None:
        carpool = 'FALSE'
    highway = request.form.get("highway")
    if highway == None:
        highway = 'FALSE'
    backroad = request.form.get("backroad")
    if backroad == None:
        backroad = 'FALSE'
    edit_tag_values(drive_id, commute, near_death_experience, carpool, highway, backroad)
    return redirect("/userprofile")

@app.get("/drives")
def get_all_drives():
    drives = viewDrives.get_all_drives()
    print(drives)
    return render_template("viewDrives.html", title="Drives", drives = drives)

@app.get("/drive/<drive_id>")
def individual(drive_id):
    individualDrive = viewIndividualDrive.get_individual_drive_by_id(drive_id)
    comments = viewDrives.get_comments(drive_id)
    return render_template("individualDrive.html", title ="Individual Drive", drive = individualDrive, comments = comments, usersession=username)

@app.get ("/userprofile")
def user_profile():
    if 'username' not in session:
        return redirect("/login")
    global firstname
    global lastname
    alldrives = userProfileSql.getAllDrives(username)
    return render_template("UserProfile.html", title = "User profile", 
                        alldrives = alldrives, 
                        firstname = firstname, 
                        lastname = lastname,
                        )

# function to delete a drive based on drive id
@app.post('/drive/<drive_id>')
def delete_drive(drive_id):
    if 'username' not in session:
        return redirect("/login")
    if not drive_id:
        abort(404)
    if deleteSql.is_drive_owner(drive_id):
        deleteSql.deleteDrive(drive_id)
        flash('Drive successfully deleted', 'success')
        return redirect("/drives")
    else:
        return redirect("/drives")

@app.get('/Vehicles')
def Vehicles():
    if 'username' not in session:
        return redirect("/login")
    vehicles = Vehicle.getVehicles(username)
    return render_template("vehicle.html", title="Vehicles", vehicles = vehicles)

#function to add vehicles
@app.post('/Vehicles')
def add_vehicle():
    make = request.form.get("make")
    model = request.form.get("model")
    year = request.form.get("year")
    color = request.form.get("color")

    username = session ['username']
    vehicle_id = str(uuid.uuid4())

    Vehicle.addVehicle(vehicle_id, username, make, model, year, color)
    flash('Vehicle successfully added', 'success')
    return redirect("/Vehicles")

#function to edit vehicles 
@app.post('/Vehicles/edit')
def edit_vehicles ():
    vehicle_id = request.form.get("vehicle_id")
    make = request.form.get("make")
    model = request.form.get("model")
    year = request.form.get("year")
    color = request.form.get("color")

    username = session ['username']
    Vehicle.editVehicle(vehicle_id,username,make,model,year, color)
    flash('Vehicle successfully edited', 'success')
    return redirect("/Vehicles")
    
#function to delete vehicles
@app.post('/Vehicles/delete/<vehicle_id>')
def delete_vehicle(vehicle_id):
    username = session ['username']
    Vehicle.deleteVehicle(vehicle_id, username)
    flash('Drive successfully deleted', 'success')
    return redirect ("/Vehicles")


@app.post("/edit")
def edit_drive_form():
    drive_id = request.form.get("drive_id")
    drive = get_drive(drive_id)
    vehicles = get_vehicles(drive['username'])
    tags = get_tags(drive_id)
    return render_template("editdrive.html", title="Edit Drive", drive = drive, vehicles = vehicles, tags = tags)

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
    # Update Drive
    edit_drive_values(drive_id, mileage, duration, vehicle, title, caption)
    # tags
    commute = request.form.get("commute")
    if commute == None:
        commute = 'FALSE'
    near_death_experience = request.form.get("NDE")
    if near_death_experience == None:
        near_death_experience = 'FALSE'
    carpool = request.form.get("carpool")
    if carpool == None:
        carpool = 'FALSE'
    highway = request.form.get("highway")
    if highway == None:
        highway = 'FALSE'
    backroad = request.form.get("backroad")
    if backroad == None:
        backroad = 'FALSE'
    # Update Tags for Drive
    edit_tag_values(drive_id, commute, near_death_experience, carpool, highway, backroad)
    return redirect('/userprofile') 

@app.post('/makecomment/<drive_id>')
def makecomment(drive_id):
    if username is None:
        flash("You must be logged in to make a comment", "error")
        return redirect(f"/drive/{drive_id}")
    comment = request.form.get("newcomment")
    viewDrives.make_comment(drive_id, username, comment)
    return redirect(f"/drive/{drive_id}?showdiv=True")

@app.get('/delete/comment/<drive_id>/<comment_id>')
def deletecomment(comment_id, drive_id):
    viewDrives.delete_comment(comment_id)   
    return redirect(f"/drive/{drive_id}?showdiv=True")
