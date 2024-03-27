from flask import Flask, render_template

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html", title ="Home")

@app.get("/login")
def login():
    return render_template("login.html", title="Login")

@app.get("/signup")
def signup():
    return render_template("signup.html", title="Sign-Up")

@app.get("/leaderboard")
def leaderboard():
    return render_template("LeaderBoard.html", title="Leaderboard")


@app.route("/create")
def create():
    return render_template("createdrive.html", title="Create Drive")

@app.get("/drives")
def get_all_drives():
    return render_template("viewDrives.html", title="Drives")

@app.get ("/userprofile")
def user_profile():
    return render_template("UserProfile.html", title = "User profile")