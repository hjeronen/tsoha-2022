from distutils.log import error
from app import app
from flask import render_template, request, redirect
import login_service
import courses

@app.route("/homepage")
def homepage():
    # if not login_service.check_csrf():
    #     return render_template("error.html")
    user_id = login_service.get_userID()
    users_courses = courses.get_users_courses(user_id, login_service.get_user_role())
    user_info = login_service.get_userinfo()
    return render_template("homepage.html", courses=users_courses, info=user_info)

@app.route("/userinfo", methods=["GET", "POST"])
def user_info():
    if request.method == "GET":
        return render_template("userinfo.html")
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        student_number = 0
        errorMessages = []
        if login_service.get_user_role() == 'student':
            student_number = request.form["student_number"]
            if len(student_number) == 0 or student_number == 0:
                errorMessages.append("Anna opiskelijanumero!")
        if len(firstname) == 0:
            errorMessages.append("Etunimi ei voi olla tyhjä!")
        if len(lastname) == 0:
            errorMessages.append("Sukunimi ei voi olla tyhjä!")
        if len(errorMessages) == 0:
            if login_service.save_user_info(firstname, lastname, student_number):
                return redirect("/homepage")
            return render_template("error.html", message = "Käyttäjätietojen tallennus ei onnistunut")
        else:
            return render_template("userinfo.html", errorMessages = errorMessages)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_2 = request.form["password_2"]
        role = request.form["role"]
        errorMessages = []

        if len(username) < 3 or len(username) > 10:
            errorMessages.append("Käyttäjätunnuksen on oltava 3-10 merkkiä pitkä.")
        if len(password) < 8:
            errorMessages.append("Salasanan on oltava vähintään 8 merkkiä pitkä.")
        if password != password_2:
            errorMessages.append("Salasanat eivät ole samat!")

        if len(errorMessages) == 0:
            register_success = login_service.register(username, password, role)
            login_success = login_service.login(username, password)
            if register_success and login_success:
                return redirect("/homepage")
            else:
                message = ""
                if not register_success:
                    message = "Käyttäjän rekisteröinti epäonnistui."
                elif not login_success:
                    message = "Sisäänkirjautuminen epäonnistui."
                return render_template("error.html", message = message)
                
        return render_template("register.html", errorMessages=errorMessages, defaultName=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if login_service.login(username, password):
            return redirect("/homepage")
        else:
            return render_template("login.html", errorMessages=["Väärä käyttäjänimi tai salasana!"], defaultName = username, defaultPassword = password)
    
@app.route("/logout")
def logout():
    if login_service.logout():
        return redirect("/")
    else:
        return render_template("error.html", message = "Uloskirjautuminen epäonnistui.")
    
@app.route("/delete_account")
def delete_account():
    if login_service.delete_account():
        return redirect("/")
    else:
        return render_template("error.html")