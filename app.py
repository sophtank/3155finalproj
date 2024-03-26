from flask import Flask, render_template

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/login")
def login():
    return render_template("login.html")


@app.get("/signup")
def signup():
    return render_template("signup.html")

@app.get("/leaderboard")
def leaderboard():
    return render_template("LeaderBoard.html")

@app.get("/drives")
def get_all_drives():
    return render_template("viewDrives.html")
