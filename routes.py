from app import app
from flask import render_template
import courses

@app.route("/")
def index():
    all_courses = courses.get_all_courses()
    return render_template("index.html", list = all_courses)
