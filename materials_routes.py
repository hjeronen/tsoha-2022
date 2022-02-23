from app import app
from flask import render_template, request, redirect
import login_service
import courses
import materials

@app.route("/update_material/<int:course_id>/<int:material_id>", methods=["GET", "POST"])
def update_material(course_id, material_id):
    owner = courses.get_course_teacher_id(course_id)
    if owner:
        owner = owner[0]
        user_id = login_service.get_userID()
        if owner != user_id:
            return render_template("error.html", message = "Vain kurssin opettaja voi muokata materiaalia.")
    
    if request.method == "GET":
        content = materials.get_material(material_id)
        return render_template("update_material.html", course_id = course_id, material_id = material_id, defaultHeadline = content.headline, defaultText = content.body)

    if request.method == "POST":
        headline = request.form["headline"]
        text = request.form["body"]
        errorMessages = []

        if len(headline) == 0:
            errorMessages.append("Otsikko ei voi olla tyhjä!")
        if len(text) == 0:
            errorMessages.append("Tekstikenttä ei voi olla tyhjä!")
        
        if len(errorMessages) == 0:
            if materials.update_material(material_id, headline, text):
                return redirect("/course_page/" + str(course_id))
            else:
                return render_template("error.html", message = "Materiaalin päivitys ei onnistunut.")
        return render_template("update_material.html", course_id = course_id, material_id = material_id, errorMessages = errorMessages, defaultHeadline = headline, defaultText = text)
    

@app.route("/delete_material/<int:course_id>/<int:material_id>")
def delete_material(course_id, material_id):
    owner = courses.get_course_teacher_id(course_id)
    if owner:
        owner = owner[0]
        user_id = login_service.get_userID()
        if owner == user_id:
            materials.delete_material(material_id)
            return redirect("/course_page/" + str(course_id))
    return render_template("error.html", message = "Materiaalin poistaminen ei onnistunut.")

@app.route("/course_material/<int:course_id>/<int:material_id>")
def course_material(course_id, material_id):
    course_teacher = courses.get_course_teacher_id(course_id)
    user_id = login_service.get_userID()
    owner = False
    enrolled = courses.check_if_student_is_enrolled(course_id, user_id)
    if course_teacher:
        course_teacher = course_teacher[0]
        if course_teacher == user_id:
            owner = True
    material = materials.get_material(material_id)
    if owner or enrolled:
        return render_template("course_material.html", course_id = course_id, material_id = material_id, owner = owner, headline = material.headline, body = material.body)
    else:
        return render_template("error.html", message = "Vain kurssin oppilaat tai opettajat voivat tarkastella materiaalia.")

@app.route("/add_material/<int:course_id>", methods=["GET", "POST"])
def add_material(course_id):
    user_id = login_service.get_userID()
    teacher = courses.get_course_teacher_id(course_id)
    if teacher:
        teacher = teacher[0]
    if user_id != teacher:
        return render_template("error.html", message = "Vain kurssin opettaja voi lisätä materiaalia.")

    if request.method == "GET":
        return render_template("add_material.html", course_id = course_id)
    
    if request.method == "POST":
        headline = request.form["headline"]
        text = request.form["body"]
        errorMessages = []

        if len(headline) == 0:
            errorMessages.append("Otsikko ei voi olla tyhjä!")
        if len(text) == 0:
            errorMessages.append("Olematonta tekstiä ei lisätä.")
        
        if len(errorMessages) == 0:
            if materials.save_material(course_id, headline, text):
                return redirect("/course_page/" + str(course_id))
            else:
                return render_template("error.html", message = "Materiaalin tallennus ei onnistunut.")
        return render_template("add_material.html", course_id = course_id, errorMessages = errorMessages, defaultHeadline = headline, defaultBody = text)