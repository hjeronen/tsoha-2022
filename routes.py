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

@app.route("/userinfo", methods=["GET", "POST"])
def user_info():
    if request.method == "GET":
        if login_service.find_userinfo():
            info = login_service.get_userinfo()
            return render_template("show_userinfo.html", list=info)
        return render_template("userinfo.html")
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        student_number = 0
        if login_service.check_user_role() == 'student':
            student_number = request.form["student_number"]
        if login_service.save_user_info(firstname, lastname, student_number):
            return render_template("success.html")
        else:
            return render_template("error.html")

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
