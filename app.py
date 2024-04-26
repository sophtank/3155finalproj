from flask import Flask, abort, flash, render_template, redirect, request, session
from repositories import Vehicle, loginSql, userProfileSql, viewDrives, deleteSql, viewIndividualDrive, drives
from repositories.leaderboard import get_leaders
from repositories.edit_drive import edit_drive_values, get_drive, get_vehicles, edit_tag_values, get_tags

from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import uuid, os

import re

load_dotenv()


app = Flask(__name__)
# global username
# username = None
# global firstname
# global lastname
# firstname = None
# lastname = None

app.secret_key = os.getenv('SECRET_KEY')


bcrypt = Bcrypt(app)

################## HOME PAGE #######################################################################
@app.get("/")
def index():
    return render_template('index.html', title ='Home')

####################### USER FUNCTIONALITY ############################################################
@app.get("/login")
def login():
    #send user to profile if already logged in
    if session:
        return redirect('/userprofile')
    return render_template('login.html', title='Login')

@app.post('/login')
def logged_in():
    #user already logged in
    if session:
        return redirect('/userprofile')

    username = request.form.get('username')
    password = request.form.get('password')

    #username and password are required
    if not username or not password:
        abort(400, 'Username and password are required')

    loginAttempt = loginSql.login(username)

    #no user exists
    if loginAttempt == []:
        return redirect('/login')
    
    #check password
    if(bcrypt.check_password_hash(loginAttempt[0]['password'], password)):
        firstname = loginAttempt[0]['first_name']
        lastname = loginAttempt[0]['last_name']
        #sessions
        session['username'] = loginAttempt[0]['username']
        return redirect('/userprofile')
    else: #password incorrect
        return redirect('/login')

#renders the signup page
@app.get('/signup')
def signup():
    #redirect to profile if already logged in
    if session:
        return redirect('/userprofile')
    return render_template('signup.html', title='Sign-Up')

#after the user signs up the user is redirected to the home page
@app.post("/signup")
def signedup():
    #abort if user is already logged in
    if session:
        return redirect('/userprofile')
    # global firstname
    # global lastname
    firstname = request.form.get('FirstName')
    lastname = request.form.get('LastName')
    # global username
    username = request.form.get('username')
    password = request.form.get('password')

    #verify needed information is given
    if not firstname or not lastname or not username or not password:
        abort(400, 'Username, password, and name are required.')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    if(loginSql.checkIFUserExists(username) != []): #user exists
        abort(400, 'User already exists')
    else:  #success
        loginSql.SignUp(username, hashed_password, firstname, lastname)
        #log user in
        session['username'] = username
    return redirect('/userprofile')

#log user out
@app.get('/logout')
def logout():
    #no session available
    if not session:
        abort(401, 'You are not logged in.')
    #clear session and redirect to home
    session.clear()
    return redirect('/')

@app.get ('/userprofile')
def user_profile():
    #make user login if not already logged in
    if 'username' not in session:
        return redirect("/login")
    # global firstname
    # global lastname
    #get data
    alldrives = userProfileSql.getAllDrives(session.get('username'))
    name = userProfileSql.getFullName(session.get('username'))
    return render_template("UserProfile.html", title = "User profile", 
                        alldrives = alldrives, 
                        firstname = name.get('first_name'), 
                        lastname = name.get('last_name'),
                        )


################################# LEADERBOARD #######################################################
#show leaderboard
@app.get('/leaderboard')
def leaderboard():
    leaders = get_leaders()
    return render_template('LeaderBoard.html', title='Leaderboard', leaders=leaders)

############################ DRIVE FUNCTIONALITY #################################################
#get create form
@app.get('/create')
def create():
    #deny acces if user not logged in
    if not session:
        abort(401, 'You must log in to create a drive.')
    
    #get user vehicles
    vehicles = Vehicle.getVehicles(session.get('username'))

    #no registered vehicles
    if vehicles == []:
        abort(400, 'You need to register a vehicle to create a drive')

    return render_template('createdrive.html', title='Create Drive', vehicles=vehicles)

@app.post('/create')
def creating():
    #make sure user is logged in
    if not session:
        abort(401, 'You must log in to create a drive')
    
    #get data
    drive_id = str(uuid.uuid4())
    vehicle_id = request.form.get('vehicle_id')
    mileage = request.form.get('mileage')
    duration = request.form.get('duration')
    title = request.form.get('titleDrive')
    caption = request.form.get('captionDrive')
    photo = 'https://img.freepik.com/free-photo/luxurious-car-parked-highway-with-illuminated-headlight-sunset_181624-60607.jpg' #temp until we figure out how to store photos
    #current date and time
    date = 'NOW()'
    user = session['username']

    #validation
    if not vehicle_id or not mileage or not duration or not title or not caption:
        abort(400, 'Missing or incomplete fields - could not create drive')
    pattern = re.compile('^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
    if not pattern.match(vehicle_id):
        abort(400, 'Invalid vehicle')
    
    if not Vehicle.getOwner(vehicle_id) or not session['username'] in Vehicle.getOwner(vehicle_id):
        print(Vehicle.getOwner(vehicle_id))
        abort(403, 'Invalid vehicle')

    if not check_numeric([mileage,duration]):
        abort (400, 'Drive mileage and duration must be numeric values')

    if not check_int([duration]):
        abort(400, 'Duration must be a whole number of minutes')
    


    #create drive
    drives.create_drive(drive_id, vehicle_id, mileage, duration, title, caption, photo, date, user)
    flash('Drive successfully created', 'success')

    #tags
    commute = request.form.get('commute')
    if commute == None:
        commute = 'FALSE'
    near_death_experience = request.form.get('NDE')
    if near_death_experience == None:
        near_death_experience = 'FALSE'
    carpool = request.form.get('carpool')
    if carpool == None:
        carpool = 'FALSE'
    highway = request.form.get('highway')
    if highway == None:
        highway = 'FALSE'
    backroad = request.form.get('backroad')
    if backroad == None:
        backroad = 'FALSE'
    edit_tag_values(drive_id, commute, near_death_experience, carpool, highway, backroad)

    #go to recent drives
    return redirect('/drives')

#view all drives
@app.get('/drives')
def get_all_drives():
    drives = viewDrives.get_all_drives()
    print(drives)
    return render_template('viewDrives.html', title='Drives', drives = drives)

#view an idividual drive
@app.get('/drive/<drive_id>')
def individual(drive_id):
    check_drive_id(drive_id)
    individualDrive = viewIndividualDrive.get_individual_drive_by_id(drive_id)
    comments = viewDrives.get_comments(drive_id)
    num_likes = viewIndividualDrive.get_num_likes(drive_id)
    if session:
        usersession = session['username']
        has_like = viewIndividualDrive.has_like(drive_id, session['username'])
    else:
        usersession = None
        has_like = None
    return render_template('individualDrive.html', title ='Individual Drive', drive = individualDrive, comments = comments, usersession=usersession, num_likes=num_likes, has_like=has_like)


# function to delete a drive based on drive id
@app.post('/drive/delete/<drive_id>')
def delete_drive(drive_id):
    check_drive_id(drive_id)

    #verify logged in
    if not session:
        abort(401, 'You must log in to delete a drive')
    #verify ownership
    if not is_owner(drive_id, session['username']):
        abort(403, 'Permission denied.  You cannot delete this drive.')

    deleteSql.deleteDrive(drive_id)
    flash('Drive successfully deleted', 'success')
    return redirect('/drives')

#make a comment
@app.post('/makecomment/<drive_id>')
def make_comment(drive_id):
    #verify drive id
    check_drive_id(drive_id)
    #verify logged in
    print(session)
    if not session:
        abort(401, 'You must log in')
    comment = request.form.get('newcomment')
    #must have text to make a comment
    if not comment:
        abort(400, 'Invalid comment')
    #make the comment :)
    viewDrives.make_comment(drive_id, session['username'], comment)
    return redirect(f'/drive/{drive_id}?showdiv=True')

#delete a comment
@app.post('/comment/delete/<comment_id>')
def deletecomment(comment_id):
    #verify comment id
    #check for valid uuid
    pattern = re.compile('^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
    if not pattern.match(comment_id):
        abort(400, 'Invalid comment ID')
    #check that comment exists
    if not viewDrives.get_comment_by_id(comment_id):
        abort(404, 'Comment does not exist')
    
    #verify logged in
    if not session:
        abort(401, 'You must log in to delete a comment')
    
    drive_id = str(viewDrives.get_drive_id_comment(comment_id).get('drive_id'))
    #verify user is owner
    if not session['username'] == (viewDrives.get_comment_owner(comment_id)).get('username') and not is_owner(drive_id, session['username']):
        print(viewDrives.get_comment_owner(comment_id))
        abort(403, 'Permission denied.  You cannot delete this comment.')
    viewDrives.delete_comment(comment_id)   
    return redirect(f'/drive/{drive_id}?showdiv=True')

#make a like
@app.post('/drive/<drive_id>/like')
def like(drive_id):
    check_drive_id(drive_id)
    #check user is logged in
    if not session:
        abort(401, 'You must log in')
    #check if user already likes
    if viewIndividualDrive.has_like(drive_id, session['username']):
        abort(400, 'You already like this drive')
    viewIndividualDrive.add_like(drive_id, session['username'])
    return redirect(f'/drive/{drive_id}')

#remove a like
@app.post('/drive/<drive_id>/dislike')
def dislike(drive_id):
    check_drive_id(drive_id)
    #check user is logged in
    if not session:
        abort(401, 'You must log in')
    #check if user already likes
    if not viewIndividualDrive.has_like(drive_id, session['username']):
        abort(400, 'You have not liked this drive')
    viewIndividualDrive.delete_like(drive_id, session['username'])
    return redirect(f'/drive/{drive_id}')

#get edit form
@app.get("/drive/<drive_id>/edit")
def edit_drive_form(drive_id):
    #verify drive id
    check_drive_id(drive_id)

    #verify login
    if not session:
        abort(401, 'You must log in')
    #verify ownership
    if not is_owner(drive_id, session['username']):
        abort(403,'Permission denied.  You cannot edit this drive.')
    drive = get_drive(drive_id)
    vehicles = get_vehicles(session['username'])
    tags = get_tags(drive_id)
    return render_template("editdrive.html", title="Edit Drive", drive = drive, vehicles = vehicles, tags = tags)

@app.post("/drive/<drive_id>/edit")
def edit_drive(drive_id):
    #verify drive id
    check_drive_id(drive_id)

    #verify login
    if not session:
        abort(401, 'You must log in')
    #verify ownership
    if not is_owner(drive_id, session['username']):
        abort(403,'Permission denied.  You cannot edit this drive.')

    if request.form.get('vehicleSelect'):
        #verify vehicle
        pattern = re.compile('^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
        if not pattern.match(request.form.get('vehicleSelect')):
            abort(400, 'Invalid vehicle')
        
    
        #verify vehicle ownership
        if not Vehicle.getOwner(request.form.get('vehicleSelect')) or not session['username'] in Vehicle.getOwner(request.form.get('vehicleSelect')):
            abort(403, 'Invalid vehicle')
        

    #verify form information
    if (request.form.get('mileage') and request.form.get('duration')) and (not check_numeric([request.form.get("mileage"), request.form.get("duration")]) or not check_int([request.form.get('duration')])):
        abort(400, 'Invalid fields for edit drive.')

    drive = get_drive(drive_id)
    #set defaults to what is used to be
    if not drive_id:
        drive_id = drive['drive_id']
    mileage = request.form.get("mileage")
    if not mileage:
        mileage = drive['mileage']
    duration = request.form.get("duration")
    if not duration:
        duration = drive['duration']
    vehicle = request.form.get("vehicleSelect")
    if not vehicle:
        vehicle = drive['vehicle_id']
    title = request.form.get("titleDrive")
    if not title:
        title = drive['title']
    caption = request.form.get("captionDrive")
    if not caption:
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


  
################### VEHICLE FUNCTIONALITY ########################################################
@app.get('/vehicles')
def vehicles():
    if not session:
        return redirect('/login')
    vehicles = Vehicle.getVehicles(session['username'])
    return render_template("vehicle.html", title="Vehicles", vehicles = vehicles)

#function to add vehicles
@app.post('/vehicles')
def add_vehicle():
    if not session:
        abort(401, 'You must login')

    make = request.form.get("make")
    model = request.form.get("model")
    year = request.form.get("year")
    color = request.form.get("color")

    if not make or not model or not year or not color:
        abort(400, 'Invalid fields.  Could not add vehicle.')
    
    pattern = re.compile('^[0-9]{4}$')
    if not pattern.match(year):
        abort(400, 'Invalid vehicle year')

    username = session ['username']
    vehicle_id = str(uuid.uuid4())

    Vehicle.addVehicle(vehicle_id, username, make, model, year, color)
    flash('Vehicle successfully added', 'success')
    return redirect("/vehicles")

#function to edit vehicles 
@app.post('/vehicles/edit')
def edit_vehicles ():
    if not session:
        abort(401, 'you must login')
    
    vehicle_id = request.form.get("vehicle_id")
    #check for valid uuid
    pattern = re.compile('^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
    if not pattern.match(vehicle_id):
        abort(400, 'Invalid vehicle')

    #check for ownership
    if not Vehicle.getOwner(vehicle_id) or not session['username'] in Vehicle.getOwner(vehicle_id):
        print(Vehicle.getOwner(vehicle_id))
        abort(403, 'Invalid vehicle')
    
    #set defaults
    vehicle_info = Vehicle.get_vehicle_by_id(vehicle_id)
    make = request.form.get("make")
    if not make:
        make = vehicle_info.get('make')
    model = request.form.get("model")
    if not model:
        model = vehicle_info.get('model')
    year = request.form.get("year")
    if not year:
        year = vehicle_info.get('year')
    color = request.form.get("color")
    if not color:
        color = vehicle_info.get('color')

    pattern = re.compile('^[0-9]{4}$')
    if not pattern.match(year):
        abort(400, 'Invalid vehicle year')

    username = session ['username']
    Vehicle.editVehicle(vehicle_id,username,make,model,year, color)
    flash('Vehicle successfully edited', 'success')
    return redirect("/vehicles")
    
#function to delete vehicles
@app.post('/vehicles/delete/<vehicle_id>')
def delete_vehicle(vehicle_id):
    if not session:
        abort(401, 'you must login')
    
    #check for valid uuid
    pattern = re.compile('^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
    if not pattern.match(vehicle_id):
        abort(400, 'Invalid vehicle')

    #check for ownership
    if not Vehicle.getOwner(vehicle_id) or not session['username'] in Vehicle.getOwner(vehicle_id):
        print(Vehicle.getOwner(vehicle_id))
        abort(403, 'Invalid vehicle')
    
    #check if vehicle is used
    if Vehicle.get_drives(vehicle_id):
        abort(400, 'You cannot delete this vehicle while it still has drives.')

    username = session ['username']
    Vehicle.deleteVehicle(vehicle_id, username)
    flash('Drive successfully deleted', 'success')
    return redirect ("/vehicles")




#################### ERROR HANDLER ###############################################################
#error handler
@app.errorhandler(Exception)
def not_found(e):
    print(e.code)
    return render_template('error.html', e=e)

################## FUNCTIONS ###################################################################
def check_numeric(nums):
    pattern = re.compile('^[1-9]\d*(\.\d+)?$')
    for i in nums:    
        if not pattern.match(i):
            return False
    return True

def check_int(nums):
    pattern = re.compile('^\d+$')
    for i in nums:
        if not pattern.match(i):
            return False
    return True

def check_drive_id(id):
    #check for valid uuid
    pattern = re.compile('^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
    if not pattern.match(id):
        abort(400, 'Invalid drive ID')
    #check that drive exists
    if not viewIndividualDrive.get_individual_drive_by_id(id):
        abort(404, 'Drive does not exist')

def is_owner(drive_id, username):
    drive = viewDrives.sql_is_owner(drive_id, username)
    if drive:
        return True
    else:
        return False