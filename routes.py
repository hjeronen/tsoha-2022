from app import app
from flask import render_template, request, redirect
import login_service
import time

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        if login_service.register(username, password, role):
            return render_template("success.html")
        else:
            return render_template("error.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if login_service.login(username, password):
            return render_template("success.html")
        else:
            return render_template("error.html")
    
@app.route("/logout")
def logout():
    if login_service.logout():
        return render_template("success.html")
    else:
        return render_template("error.html")
    
@app.route("/delete_account")
def delete_account():
    if login_service.delete_account():
        return render_template("success.html")
    else:
        return render_template("error.html")
