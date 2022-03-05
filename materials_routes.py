from app import app
from flask import render_template, request, redirect
import users
import courses
import materials

@app.route("/update_material/<int:course_id>/<int:material_id>", methods=["GET", "POST"])
def update_material(course_id, material_id):
    user_id = users.get_user_id()
    if not courses.check_if_owner(user_id, course_id):
        return render_template("error.html", message="Vain kurssin opettaja voi muokata materiaalia.")

    if request.method == "GET":
        content = materials.get_material(material_id)
        return render_template("update_material.html", course_id=course_id,
                                                        material_id=material_id,
                                                        default_headline=content.headline,
                                                        default_body=content.body)

    if request.method == "POST":
        users.check_csrf()
        headline = request.form["headline"]
        text = request.form["body"]
        error_messages = []

        if len(headline) < 1 or len(headline) > 20:
            error_messages.append("Otsikon on oltava 1-20 merkkiä pitkä.")
        if len(text) < 1 or len(text) > 50000:
            error_messages.append("Tekstin on oltava 1-50000 merkkiä pitkä.")

        if len(error_messages) == 0:
            if materials.update_material(material_id, headline, text):
                return redirect("/course_material/" + str(course_id) + "/" + str(material_id))
            return render_template("error.html", message="Kurssimateriaalin päivitys ei onnistunut")

        return render_template("update_material.html", error_messages=error_messages,
                                                        course_id=course_id,
                                                        material_id=material_id,
                                                        default_headline=headline,
                                                        default_body=text)

@app.route("/delete_material/<int:course_id>/<int:material_id>")
def delete_material(course_id, material_id):
    user_id = users.get_user_id()
    if not courses.check_if_owner(user_id, course_id):
        return render_template("error.html", message="Vain kurssin opettaja voi poistaa kurssimateriaalia.")

    if materials.delete_material(material_id):
        return redirect("/course_page/" + str(course_id))
    return render_template("error.html", message="Kurssimateriaalin poistaminen ei onnistunut")

@app.route("/course_material/<int:course_id>/<int:material_id>")
def course_material(course_id, material_id):
    user_id = users.get_user_id()
    owner = courses.check_if_owner(user_id, course_id)
    enrolled = courses.check_if_student_is_enrolled(course_id, user_id)

    if not (owner or enrolled):
        return render_template("error.html", message="Vain kurssin oppilaat tai opettaja voivat tarkastella materiaalia.")

    material = materials.get_material(material_id)
    return render_template("course_material.html", course_id=course_id,
                                                    material_id=material_id,
                                                    owner=owner,
                                                    headline=material.headline,
                                                    body=material.body)

@app.route("/add_material/<int:course_id>", methods=["GET", "POST"])
def add_material(course_id):
    user_id = users.get_user_id()
    if not courses.check_if_owner(user_id, course_id):
        return render_template("error.html", message="Vain kurssin opettaja voi lisätä materiaalia.")

    if request.method == "GET":
        return render_template("add_material.html", course_id=course_id)

    if request.method == "POST":
        users.check_csrf()
        headline = request.form["headline"]
        body = request.form["body"]
        error_messages = []

        if len(headline) < 1 or len(headline) > 20:
            error_messages.append("Otsikon on oltava 1-20 merkkiä pitkä.")
        if len(body) < 1 or len(body) > 50000:
            error_messages.append("Tekstin on oltava 1-50000 merkkiä pitkä.")

        if len(error_messages) == 0:
            if materials.save_material(course_id, headline, body):
                return redirect("/course_page/" + str(course_id))
            return render_template("error.html", message="Kurssimateriaalin lisäys ei onnistunut")

        return render_template("add_material.html", error_messages=error_messages,
                                                    course_id=course_id,
                                                    default_headline=headline,
                                                    default_body=body)
