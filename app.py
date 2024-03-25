from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signUp")
def signup():
    return render_template("signup.html")

@app.route("/leaderboard")
def leaderboard():
    return render_template("LeaderBoard.html")

@app.get("/drives")
def getAllDrives():
    return render_template("viewDrives.html")
