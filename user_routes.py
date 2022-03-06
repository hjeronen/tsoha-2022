from app import app
from flask import render_template, request, redirect
import users
import courses

@app.route("/homepage")
def homepage():
    user_id = users.logged_in()
    if user_id == 0:
        return redirect("/")
    users_courses = courses.get_users_courses(user_id, users.get_user_role())
    users_info = users.get_userinfo()
    return render_template("homepage.html", courses=users_courses, info=users_info)

@app.route("/userinfo", methods=["GET", "POST"])
def user_info():
    if request.method == "GET":
        return render_template("userinfo.html")

    if request.method == "POST":
        users.check_csrf()
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        student_number = 0
        error_messages = []

        if users.get_user_role() == 'student':
            student_number = request.form["student_number"]
            if len(student_number) == 0 or student_number == 0:
                error_messages.append("Anna opiskelijanumero!")

        if len(firstname) < 1 or len(firstname) > 20:
            error_messages.append("Etunimen on oltava 1-20 merkkiä pitkä.")
        if len(lastname) < 1 or len(lastname) > 20:
            error_messages.append("Sukunimen on oltava 1-20 merkkiä pitkä.")

        if len(error_messages) == 0:
            if users.save_user_info(firstname, lastname, student_number):
                return redirect("/homepage")
            return render_template("homepage.html", error_messages=["Käyttäjätietojen tallennus ei onnistunut."])

        return render_template("userinfo.html", error_messages = error_messages,
                                                default_firstname = firstname,
                                                default_lastname = lastname,
                                                default_studentnr = student_number)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_2 = request.form["password_2"]
        role = request.form["role"]
        error_messages = []

        if len(username) < 3 or len(username) > 10:
            error_messages.append("Käyttäjätunnuksen on oltava 3-10 merkkiä pitkä.")
        if len(password) < 8 or len(password) > 15:
            error_messages.append("Salasanan on oltava 8-15 merkkiä pitkä.")
        if password != password_2:
            error_messages.append("Salasanat eivät ole samat!")

        if len(error_messages) == 0:
            register_success = users.register(username, password, role)
            login_success = users.login(username, password)
            if register_success and login_success:
                return redirect("/homepage")

            if not register_success:
                error_messages.append("Käyttäjän rekisteröinti epäonnistui. Todennäköisesti käyttäjätunnus on varattu.")
            elif not login_success:
                error_messages.append("Sisäänkirjautuminen epäonnistui.")
            return render_template("register.html", error_messages=error_messages, username=username)

        return render_template("register.html", error_messages=error_messages, username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error_messages = []

        if len(username) < 3 or len(username) > 10:
            error_messages.append("Käyttäjätunnuksen on oltava 3-10 merkkiä pitkä.")
        if len(password) > 15:
            error_messages.append("Salasanan on oltava 8-15 merkkiä pitkä.")

        if len(error_messages) == 0:
            if users.login(username, password):
                return redirect("/homepage")
            error_messages.append("Väärä käyttäjänimi tai salasana!")

        return render_template("login.html", error_messages=error_messages,
                                                username=username,
                                                password=password)

@app.route("/logout")
def logout():
    if users.logout():
        return redirect("/")
    return render_template("error.html", message="Uloskirjautuminen epäonnistui.")

@app.route("/delete_account")
def delete_account():
    if users.delete_account():
        return redirect("/")
    return render_template("error.html", message="Tilin poistaminen epäonnistui.")
