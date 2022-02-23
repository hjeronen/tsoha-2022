from app import app
from flask import render_template, request, redirect
import login_service
import courses
import exercises
import materials

@app.route("/")
def index():
    all_courses = courses.get_all_courses()
    return render_template("index.html", list = all_courses)

@app.route("/homepage")
def homepage():
    # if not login_service.check_csrf():
    #     return render_template("error.html")
    user_id = login_service.get_userID()
    users_courses = courses.get_users_courses(user_id, login_service.get_user_role())
    user_info = login_service.get_userinfo()
    return render_template("homepage.html", courses=users_courses, info=user_info)

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

@app.route("/delete_exercise/<int:course_id>/<int:exercise_id>")
def delete_exercise(course_id, exercise_id):
    user_id = login_service.get_userID()
    teacher = courses.get_course_teacher_id(course_id)
    if teacher:
        teacher = teacher[0]
    if user_id != teacher:
        return render_template("error.html", message = "Vain kurssin opettaja voi poistaa tehtävän.")
    if exercises.delete_exercise(exercise_id):
        return redirect("/course_page/" + str(course_id))
    return render_template("error.html", message = "Tehtävän poistaminen ei onnistunut.")

@app.route("/update_exercise/<int:course_id>/<int:exercise_id>/<int:exercise_type>/<headline>", methods=["GET", "POST"])
def update_exercise(course_id, exercise_id, exercise_type, headline):
    user_id = login_service.get_userID()
    teacher = courses.get_course_teacher_id(course_id)
    if teacher:
        teacher = teacher[0]
    if user_id != teacher:
        return render_template("error.html", message = "Vain kurssin opettaja voi muokata tehtäviä.")
    exercise = exercises.get_exercise(exercise_id, exercise_type)

    if request.method == "GET":
        if exercise_type == 0:
            return render_template("update_exercise_text.html", course_id = course_id, 
                                                                exercise_id = exercise_id, 
                                                                exercise_type = exercise_type, 
                                                                exercise = exercise, 
                                                                headline = headline,
                                                                question = exercise.question,
                                                                answer = exercise.correct_answer)
        elif exercise_type == 1:
            return render_template("update_exercise_mchoice.html", course_id = course_id, 
                                                                    exercise_id = exercise_id, 
                                                                    exercise_type = exercise_type, 
                                                                    exercise = exercise, 
                                                                    headline = headline, 
                                                                    question = exercise.question,
                                                                    answer = exercise.correct_answer,
                                                                    a = exercise.option_a, 
                                                                    b = exercise.option_b, 
                                                                    c = exercise.option_c)

    if request.method == "POST":
        new_headline = request.form["headline"]
        question = request.form["question"]
        answer = request.form["answer"]
        errorMessages = []

        if len(new_headline) == 0:
            errorMessages.append("Otsikko ei voi olla tyhjä!")
        if len(question) == 0:
            errorMessages.append("Kysymys ei voi olla tyhjä!")
        if len(answer) == 0:
            errorMessages.append("Vastaus ei voi olla tyhjä!")

        if exercise_type == 0:
            if len(errorMessages) != 0:
                return render_template("update_exercise_text.html", course_id = course_id, 
                                                                    exercise_id = exercise_id, 
                                                                    exercise_type = exercise_type, 
                                                                    exercise = exercise, 
                                                                    headline = new_headline, 
                                                                    question = question,
                                                                    answer = answer,
                                                                    errorMessages = errorMessages)
            if exercises.update_exercise_text(exercise_id, new_headline, question, answer):
                return redirect("/show_exercise/" + str(course_id) + "/" + str(exercise_id) + "/" + str(exercise_type) + "/" + headline)

        if exercise_type == 1:
            a = request.form["option_a"]
            b = request.form["option_b"]
            c = request.form["option_c"]

            if answer == "a":
                answer = a
            elif answer == "b":
                answer = b
            elif answer == "c":
                answer = c
            
            if len(a) == 0 or len(b) == 0 or len(c) == 0:
                errorMessages.append("Mikään vastausvaihtoehto ei voi olla tyhjä!")
            
            if len(errorMessages) != 0:
                return render_template("update_exercise_mchoice.html", course_id = course_id, 
                                                                    exercise_id = exercise_id, 
                                                                    exercise_type = exercise_type, 
                                                                    exercise = exercise, 
                                                                    headline = headline, 
                                                                    errorMessages = errorMessages,
                                                                    a = a,
                                                                    b = b,
                                                                    c = c)
            if exercises.update_exercise_mchoice(exercise_id, headline, question, answer, a, b, c):
                return redirect("/show_exercise/" + str(course_id) + "/" + str(exercise_id) + "/" + str(exercise_type) + "/" + headline)
        
        return render_template("error.html", message = "Tehtävän muokkaus ei onnistunut.")

            

@app.route("/show_exercise/<int:course_id>/<int:exercise_id>/<int:exercise_type>/<headline>", methods=["GET", "POST"])
def show_exercise(course_id, exercise_id, exercise_type, headline):
    exercise = exercises.get_exercise(exercise_id, exercise_type)
    user_id = login_service.get_userID()
    answer = exercises.get_answer(user_id, exercise_id)
    owner = False
    if login_service.get_user_role() == "teacher":
        teacher = courses.get_course_teacher_id(course_id)[0]
        if teacher == user_id:
            owner = True

    if request.method == "GET":
        if answer:
            answer = answer[0]
            test_answer = answer.lower()
            test_correct = exercise.correct_answer.lower()
            answer_is_correct = (test_answer == test_correct)
            return render_template("show_exercise.html", course_id = course_id,
                                                        exercise_id = exercise_id,
                                                        exercise_type = exercise_type, 
                                                        exercise = exercise, 
                                                        headline = headline, 
                                                        answered = True, 
                                                        answer = answer, 
                                                        correct = answer_is_correct,
                                                        owner = owner)
        
        return render_template("show_exercise.html", course_id = course_id,
                                                    exercise_id = exercise_id, 
                                                    exercise_type = exercise_type, 
                                                    exercise = exercise, 
                                                    headline = headline, 
                                                    answered = False,
                                                    owner = owner)

    if request.method == "POST":
        if login_service.get_user_role() == "teacher":
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
                                                    exercise_type = exercise_type, 
                                                    exercise = exercise, 
                                                    headline = headline, 
                                                    answered = True, 
                                                    answer = answer, 
                                                    correct_answer = exercise.correct_answer, 
                                                    correct = answer_is_correct)

@app.route("/add_exercise_mchoice/<int:course_id>", methods=["GET", "POST"])
def add_exercise_mchoice(course_id):
    if request.method == "GET":
        user_id = login_service.get_userID()
        course_teacher_id = courses.get_course(course_id)[3]
        if user_id != course_teacher_id:
            return render_template("error.html", message = "Vain kurssin opettaja voi lisätä harjoitustehtäviä.")
        return render_template("add_exercise_mchoice.html", course_id = course_id)

    if request.method == "POST":
        exercise_type = 1
        headline = request.form["headline"]
        question = request.form["question"]
        answer = request.form["answer"]
        errorMessages = []

        if len(question) == 0:
            errorMessages.append("Kysymys ei voi olla tyhjä!")

        a = request.form["option_a"]
        b = request.form["option_b"]
        c = request.form["option_c"]

        if answer == "a":
            answer = a
        elif answer == "b":
            answer = b
        elif answer == "c":
            answer = c

        if len(headline) == 0:
            errorMessages.append("Otsikko ei voi olla tyhjä!")
        if len(a) == 0 or len(b) == 0 or len(c) == 0:
            errorMessages.append("Mikään vastausvaihtoehto ei voi olla tyhjä!")

        if len(errorMessages) == 0:
            exercise = (exercise_type, headline, question, answer, a, b, c)
            if exercises.add_exercise(course_id, exercise):
                return redirect("/course_page/" + str(course_id))
            return render_template("error.html", message = "Tehtävän tallennus ei onnistunut.")

        return render_template("add_exercise_mchoice.html", course_id = course_id, errorMessages = errorMessages, defaultQuestion = question, defaultAnswer = answer, defaultA = a, defaultB = b, defaultC = c)

@app.route("/add_exercise_text/<int:course_id>", methods=["GET", "POST"])
def add_exercise_text(course_id):
    if request.method == "GET":
        user_id = login_service.get_userID()
        course_teacher_id = courses.get_course(course_id)[3]
        if user_id != course_teacher_id:
            return render_template("error.html", message = "Vain kurssin opettaja voi lisätä harjoitustehtäviä.")
        return render_template("add_exercise_text.html", course_id = course_id)

    if request.method == "POST":
        exercise_type = 0
        headline = request.form["headline"]
        question = request.form["question"]
        answer = request.form["answer"]
        errorMessages = []

        if len(headline) == 0:
            errorMessages.append("Otsikko ei voi olla tyhjä!")
        if len(question) == 0:
            errorMessages.append("Kysymys ei voi olla tyhjä!")
        if len(answer) == 0:
            errorMessages.append("Vastaus ei voi olla tyhjä!")

        if len(errorMessages) == 0:
            exercise = (exercise_type, headline, question, answer)
            if exercises.add_exercise(course_id, exercise):
                return redirect("/course_page/" + str(course_id))
            else:
                return render_template("error.html", message = "Tehtävän tallennus ei onnistunut.")

        return render_template("add_exercise_text.html", course_id = course_id, errorMessages = errorMessages, defaultHeadline = headline, defaultQuestion = question, defaultAnswer = answer)

@app.route("/choose_exercise_type/<int:course_id>", methods=["GET", "POST"])
def choose_exercise_type(course_id):
    if request.method == "GET":
        user_id = login_service.get_userID()
        course_teacher_id = courses.get_course(course_id)[3]
        if user_id != course_teacher_id:
            return render_template("error.html", message = "Vain kurssin opettaja voi lisätä harjoitustehtäviä.")
        return render_template("choose_exercise_type.html", course_id = course_id)
    
    if request.method == "POST":
        exercise_type = int(request.form["exercise_type"])
        if exercise_type == 0:
            return redirect("/add_exercise_text/" + str(course_id))
        elif exercise_type == 1:
            return redirect("/add_exercise_mchoice/" + str(course_id))
        else:
            return render_template("error.html", message = "Jotain meni pieleen.")

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
        role = request.form["role"]
        errorMessages = []
        if len(username) < 3 or len(username) > 10:
            errorMessages.append("Käyttäjätunnuksen on oltava 3-10 merkkiä pitkä.")
        if len(password) < 8:
            errorMessages.append("Salasanan on oltava vähintään 8 merkkiä pitkä.")
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
