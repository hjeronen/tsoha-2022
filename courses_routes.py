from app import app
from flask import render_template, request, redirect
import login_service
import courses
import exercises
import materials

@app.route("/enroll/<int:course_id>", methods=["GET", "POST"])
def enroll(course_id):
    course = courses.get_course(course_id)
    if not course:
        return render_template("error.html", message = "Kurssia ei löytynyt.")

    if request.method == "GET":
        return render_template("enroll.html", course_id = course_id, course_name=course[1])

    if request.method == "POST":
        student_id = login_service.get_userID()
        errorMessages = []
        user_role = login_service.get_user_role()
        if user_role == "teacher":
            errorMessages.append("Opettajat eivät voi ilmoittautua kursseille.")
        if not login_service.has_userinfo():
            errorMessages.append("Täydennä ensin käyttäjätietosi!")
        if courses.check_if_student_is_enrolled(course_id, student_id):
            errorMessages.append("Olet jo ilmoittautunut kurssille!")
        if len(errorMessages) == 0:
            if courses.enroll_on_course(course_id, student_id, user_role):
                return redirect("/course_page/" + str(course_id))
            else:
                return render_template("error.html", message = "Ilmoittautuminen epäonnistui.")
        return render_template("enroll.html", course_id = course_id, course_name=course[1], errorMessages = errorMessages)

@app.route("/course_page/<int:course_id>")
def show_coursepage(course_id):
    info = courses.get_course(course_id)
    if info:
        id = info[0]
        course_name = info[1]
        description = info[2]
        teacher_id = info[3]
        teacher = info[4] + ' ' + info[5]
        enrolled = False
        owner = False
        course_exercises = exercises.get_exercises(course_id)
        exercise_answers = []
        course_materials = materials.get_course_materials(course_id)
        user_id = login_service.get_userID()
        if user_id != 0:
            if teacher_id == user_id:
                owner = True
                exercise_answers = exercises.get_all_course_exercise_answers(course_id)
            if login_service.get_user_role() == 'student':
                enrolled = courses.check_if_student_is_enrolled(course_id, user_id)
                if enrolled:
                    exercise_answers = exercises.get_students_course_exercise_answers(user_id, course_id)
        return render_template("course_page.html", id = course_id, 
                                                course_name = course_name, 
                                                description = description, 
                                                teacher=teacher, 
                                                enrolled=enrolled, 
                                                owner=owner, 
                                                exercise_list = course_exercises, 
                                                answers = exercise_answers,
                                                materials = course_materials)
    else:
        return render_template("error.html", message = "Kurssitietoja ei löytynyt.")

@app.route("/add_course", methods=["GET", "POST"])
def add_course():
    if request.method == "GET":
        message = ""
        if not login_service.has_userinfo():
            message = "Täytä ensin käyttäjätietosi!"
            return render_template("error.html", message = message)
        return render_template("add_course.html")
    if request.method == "POST":
        course_name = request.form["course_name"]
        description = request.form["description"]
        user_id = login_service.get_userID()
        user_role = login_service.get_user_role()
        errorMessages = []
        if len(course_name) < 3:
            errorMessages.append("Kurssin nimen on oltava vähintään 3 kirjainta!")
        if len(description) == 0:
            errorMessages.append("Kurssilla on oltava kuvaus!")
        if len(errorMessages) == 0:
            if courses.add_course(user_id, user_role, course_name, description):
                return redirect("/homepage")
            else:
                return render_template("error.html", message = "Kurssin lisäys ei onnistunut.")
        else:
            return render_template("add_course.html", errorMessages = errorMessages, defaultName = course_name, defaultDescription = description)
            

@app.route("/update_course/<int:course_id>", methods=["GET", "POST"])
def update_course(course_id):
    if request.method == "GET":
        info = courses.get_course(course_id)
        if info:
            course_name = info[1]
            description = info[2]
            return render_template("update_course.html", course_id = course_id, course_name = course_name, description = description)
        else:
            return render_template("error.html", message = "Kurssia {{ course_id }} ei löytynyt tietokannasta")
    if request.method == "POST":
        course_name = request.form["course_name"]
        description = request.form["description"]
        user_id = login_service.get_userID()
        user_role = login_service.get_user_role()
        errorMessages = []
        if len(course_name) < 3:
            errorMessages.append("Kurssin nimen on oltava vähintään 3 kirjainta!")
        if len(description) == 0:
            errorMessages.append("Kurssilla on oltava kuvaus!")
        if len(errorMessages) == 0:
            if courses.update_course(user_id, user_role, course_id, course_name, description):
                return redirect("/course_page/" + str(course_id))
            else:
                return render_template("error.html", message = "Kurssin päivitys ei onnistunut.")
        else:
            return render_template("update_course.html", course_id = course_id, course_name = course_name, description = description, errorMessages = errorMessages)

@app.route("/delete_course/<int:course_id>")
def delete_course(course_id):
    user_id = login_service.get_userID()
    user_role = login_service.get_user_role()
    if courses.delete_course(user_id, user_role, course_id):
        return redirect("/homepage")
    else:
        return render_template("error.html")