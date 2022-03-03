from app import app
from flask import render_template, request, redirect
import login_service
import courses
import exercises

@app.route("/delete_exercise/<int:course_id>/<int:exercise_id>")
def delete_exercise(course_id, exercise_id):
    user_id = login_service.get_userID()
    if not courses.check_if_owner(user_id, course_id):
        return render_template("error.html", message = "Vain kurssin opettaja voi poistaa tehtävän.")
    if exercises.delete_exercise(exercise_id):
        return redirect("/course_page/" + str(course_id))
    return render_template("error.html", message = "Tehtävän poistaminen ei onnistunut.")

@app.route("/update_exercise_mchoice/<int:course_id>/<int:exercise_id>", methods=["GET", "POST"])
def update_exercise_mchoice(course_id, exercise_id):
    user_id = login_service.get_userID()
    if not courses.check_if_owner(user_id, course_id):
        return render_template("error.html", message = "Vain kurssin opettaja voi muokata tehtäviä.")
    exercise = exercises.get_exercise(exercise_id)

    if request.method == "GET":
        return render_template("update_exercise_mchoice.html", course_id = course_id, 
                                                                exercise_id = exercise_id,
                                                                headline = exercise.headline,
                                                                question = exercise.question,
                                                                answer = exercise.correct_answer,
                                                                a = exercise.option_a, 
                                                                b = exercise.option_b, 
                                                                c = exercise.option_c)

    if request.method == "POST":
        login_service.check_csrf()
        new_headline = request.form["headline"]
        question = request.form["question"]
        answer = request.form["answer"]
        error_messages = []

        if len(new_headline) < 1 or len(new_headline) > 20:
            error_messages.append("Otsikon on oltava 1-20 merkkiä.")
        if len(question) < 1 or len(question) > 500:
            error_messages.append("Kysymyksen on oltava 1-500 merkkiä.")

        a = request.form["option_a"]
        b = request.form["option_b"]
        c = request.form["option_c"]

        if answer == "a":
            answer = a
        elif answer == "b":
            answer = b
        elif answer == "c":
            answer = c
            
        min_length = 1
        max_length = 200
        
        if len(a) < min_length or len(a) > max_length or len(b) < min_length or len(b) > max_length or len(c) < min_length or len(c) > max_length:
            error_messages.append("Jokaisen vastausvaihtoehdon on oltava 1-200 merkkiä pitkiä.")
            
        if len(error_messages) != 0:
            return render_template("update_exercise_mchoice.html", course_id = course_id,
                                                                    exercise_id = exercise_id,
                                                                    headline = new_headline, 
                                                                    errorMessages = error_messages,
                                                                    a = a,
                                                                    b = b,
                                                                    c = c)
        if exercises.update_exercise_mchoice(exercise_id, new_headline, question, answer, a, b, c):
            return redirect("/show_exercise/" + str(course_id) + "/" + str(exercise_id))
        
        return render_template("error.html", message = "Tehtävän muokkaus ei onnistunut.")

@app.route("/update_exercise_text/<int:course_id>/<int:exercise_id>", methods=["GET", "POST"])
def update_exercise_text(course_id, exercise_id):
    user_id = login_service.get_userID()
    if not courses.check_if_owner(user_id, course_id):
        return render_template("error.html", message = "Vain kurssin opettaja voi muokata tehtäviä.")
    exercise = exercises.get_exercise(exercise_id)

    if request.method == "GET":
        return render_template("update_exercise_text.html", course_id = course_id, 
                                                                exercise_id = exercise_id,
                                                                headline = exercise.headline,
                                                                question = exercise.question,
                                                                answer = exercise.correct_answer)
    
    if request.method == "POST":
        login_service.check_csrf()
        new_headline = request.form["headline"]
        question = request.form["question"]
        answer = request.form["answer"]
        error_messages = []

        if len(new_headline) < 1 or len(new_headline) > 20:
            error_messages.append("Otsikon on oltava 1-20 merkkiä.")
        if len(question) < 1 or len(question) > 500:
            error_messages.append("Kysymyksen on oltava 1-500 merkkiä.")
        if len(answer) < 1 or len(answer) > 40:
            error_messages.append("Vastauksen on oltava 1-40 merkkiä.")

        if len(error_messages) != 0:
            return render_template("update_exercise_text.html", course_id = course_id, 
                                                                exercise_id = exercise_id,
                                                                headline = new_headline, 
                                                                question = question,
                                                                answer = answer,
                                                                errorMessages = error_messages)

        if exercises.update_exercise_text(exercise_id, new_headline, question, answer):
            return redirect("/show_exercise/" + str(course_id) + "/" + str(exercise_id))
            
        return render_template("error.html", message = "Tehtävän muokkaus ei onnistunut.")

@app.route("/show_exercise/<int:course_id>/<int:exercise_id>", methods=["GET", "POST"])
def show_exercise(course_id, exercise_id):
    exercise = exercises.get_exercise(exercise_id)
    user_id = login_service.get_userID()
    answer = exercises.get_answer(user_id, exercise_id)
    owner = courses.check_if_owner(user_id, course_id)

    if request.method == "GET":
        if not owner and login_service.get_user_role() != "student":
            return render_template("error.html", message = "Vain opiskelijat voivat vastata tehtäviin.")
        if answer:
            answer = answer[0]
            test_answer = answer.lower()
            test_correct = exercise.correct_answer.lower()
            answer_is_correct = (test_answer == test_correct)
            return render_template("show_exercise.html", course_id = course_id,
                                                        exercise_id = exercise_id,
                                                        exercise = exercise,
                                                        answered = True, 
                                                        answer = answer, 
                                                        correct = answer_is_correct,
                                                        owner = owner)
        
        return render_template("show_exercise.html", course_id = course_id,
                                                    exercise_id = exercise_id,
                                                    exercise = exercise,
                                                    answered = False,
                                                    owner = owner)

    if request.method == "POST":
        login_service.check_csrf()
        if login_service.get_user_role() != "student":
            return render_template("error.html", message = "Vain opiskelijat voivat vastata tehtäviin.")
        test_correct = exercise.correct_answer.lower()
        if not answer:
            answer = request.form["answer"]
            if len(answer) == 0:
                answer = "ei vastausta"
            test_answer = answer.lower()
            answer_is_correct = (test_answer == test_correct)
            exercises.save_answer(user_id, exercise_id, answer, answer_is_correct)
        else:
            test_answer = answer.lower()
            answer_is_correct = (test_answer == test_correct)
        return render_template("show_exercise.html", course_id = course_id,
                                                    exercise_id = exercise_id,
                                                    exercise = exercise,
                                                    answered = True, 
                                                    answer = answer, 
                                                    correct_answer = exercise.correct_answer, 
                                                    correct = answer_is_correct)

@app.route("/add_exercise_mchoice/<int:course_id>", methods=["GET", "POST"])
def add_exercise_mchoice(course_id):
    user_id = login_service.get_userID()
    if not courses.check_if_owner(user_id, course_id):
        return render_template("error.html", message = "Vain kurssin opettaja voi lisätä harjoitustehtäviä.")

    if request.method == "GET":
        return render_template("add_exercise_mchoice.html", course_id = course_id)

    if request.method == "POST":
        login_service.check_csrf()
        exercise_type = 1
        headline = request.form["headline"]
        question = request.form["question"]
        answer = request.form["answer"]
        error_messages = []

        if len(headline) < 1 or len(headline) > 20:
            error_messages.append("Otsikon on oltava 1-20 merkkiä.")
        if len(question) < 1 or len(question) > 500:
            error_messages.append("Kysymyksen on oltava 1-500 merkkiä.")

        a = request.form["option_a"]
        b = request.form["option_b"]
        c = request.form["option_c"]

        if answer == "a":
            answer = a
        elif answer == "b":
            answer = b
        elif answer == "c":
            answer = c

        min_length = 1
        max_length = 200
        
        if len(a) < min_length or len(a) > max_length or len(b) < min_length or len(b) > max_length or len(c) < min_length or len(c) > max_length:
            error_messages.append("Jokaisen vastausvaihtoehdon on oltava 1-200 merkkiä pitkiä.")

        if len(error_messages) == 0:
            exercise = (exercise_type, headline, question, answer, a, b, c)
            if exercises.add_exercise(course_id, exercise):
                return redirect("/course_page/" + str(course_id))
            return render_template("error.html", message = "Tehtävän tallennus ei onnistunut.")

        return render_template("add_exercise_mchoice.html", course_id = course_id, errorMessages = error_messages, defaultQuestion = question, defaultAnswer = answer, defaultA = a, defaultB = b, defaultC = c)

@app.route("/add_exercise_text/<int:course_id>", methods=["GET", "POST"])
def add_exercise_text(course_id):
    user_id = login_service.get_userID()
    if not courses.check_if_owner(user_id, course_id):
        return render_template("error.html", message = "Vain kurssin opettaja voi lisätä harjoitustehtäviä.")

    if request.method == "GET":
        return render_template("add_exercise_text.html", course_id = course_id)

    if request.method == "POST":
        login_service.check_csrf()
        exercise_type = 0
        headline = request.form["headline"]
        question = request.form["question"]
        answer = request.form["answer"]
        error_messages = []

        if len(headline) < 1 or len(headline) > 20:
            error_messages.append("Otsikon on oltava 1-20 merkkiä.")
        if len(question) < 1 or len(question) > 500:
            error_messages.append("Kysymyksen on oltava 1-500 merkkiä.")
        if len(answer) < 1 or len(answer) > 40:
            error_messages.append("Vastauksen on oltava 1-40 merkkiä.")

        if len(error_messages) == 0:
            exercise = (exercise_type, headline, question, answer)
            if exercises.add_exercise(course_id, exercise):
                return redirect("/course_page/" + str(course_id))
            else:
                return render_template("error.html", message = "Tehtävän tallennus ei onnistunut.")

        return render_template("add_exercise_text.html", course_id = course_id, errorMessages = error_messages, defaultHeadline = headline, defaultQuestion = question, defaultAnswer = answer)

@app.route("/choose_exercise_type/<int:course_id>", methods=["GET", "POST"])
def choose_exercise_type(course_id):
    user_id = login_service.get_userID()
    if not courses.check_if_owner(user_id, course_id):
        return render_template("error.html", message = "Vain kurssin opettaja voi lisätä harjoitustehtäviä.")

    if request.method == "GET":
        return render_template("choose_exercise_type.html", course_id = course_id)
    
    if request.method == "POST":
        login_service.check_csrf()
        exercise_type = int(request.form["exercise_type"])
        if exercise_type == 0:
            return redirect("/add_exercise_text/" + str(course_id))
        elif exercise_type == 1:
            return redirect("/add_exercise_mchoice/" + str(course_id))
        else:
            return render_template("error.html", message = "Jotain meni pieleen.")