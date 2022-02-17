from db import db

def get_all_course_exercise_answers(course_id):
    sql = "SELECT student_number, exercises.id, headline, correct FROM (SELECT * FROM course_attendances c, students s WHERE c.student_id=s.user_id AND course_id=:course_id) AS attendees LEFT OUTER JOIN (SELECT exercises.id, headline, user_id, answer, correct FROM exercises LEFT OUTER JOIN answers ON exercises.id=answers.exercise_id WHERE course_id=:course_id) AS exercises ON exercises.user_id=attendees.user_id"
    result = db.session.execute(sql, {"course_id":course_id}).fetchall()
    answers = {}
    for line in result:
        if not line.student_number in answers:
            answers[line.student_number] = {}
        answers[line.student_number][line.headline] = line.correct
    return answers

def get_correct_answers(user_id, course_id):
    sql = "SELECT COUNT(*) FROM answers a, exercises e WHERE e.course_id=:course_id AND a.exercise_id=e.id AND a.user_id=:user_id AND a.correct=TRUE"
    return db.session.execute(sql, {"course_id":course_id, "user_id":user_id}).fetchall()

def get_done_exercises(user_id, course_id):
    sql = "SELECT COUNT(*) FROM answers a, exercises e WHERE e.course_id=:course_id AND a.exercise_id=e.id AND a.user_id=:user_id"
    return db.session.execute(sql, {"course_id":course_id, "user_id":user_id}).fetchall()

def get_answer(user_id, exercise_id):
    sql = "SELECT answer FROM answers WHERE user_id=:user_id AND exercise_id=:exercise_id"
    return db.session.execute(sql, {"user_id":user_id, "exercise_id":exercise_id}).fetchone()

def save_answer(user_id, exercise_id, answer, status):
    try:
        sql = "INSERT INTO answers (user_id, exercise_id, answer, correct) VALUES (:user_id, :exercise_id, :answer, :status)"
        db.session.execute(sql, {"user_id":user_id, "exercise_id":exercise_id, "answer":answer, "status":status})
        db.session.commit()
        return True
    except:
        return False

def get_exercise(exercise_id, type):
    if type == 0:
        sql = "SELECT * FROM exercises_text WHERE exercise_id=:exercise_id"
        return db.session.execute(sql, {"exercise_id": exercise_id}).fetchone()
    elif type == 1:
        sql = "SELECT * FROM exercises_mchoice WHERE exercise_id=:exercise_id"
        return db.session.execute(sql, {"exercise_id": exercise_id}).fetchone()

def get_exercises(course_id):
    sql = "SELECT * FROM exercises WHERE course_id=:course_id"
    return db.session.execute(sql, {"course_id": course_id}).fetchall()

def add_exercise(course_id, exercise):
    type = exercise[0]
    headline = exercise[1]
    try:
        sql = "INSERT INTO exercises (course_id, type, headline, visible) VALUES (:course_id, :type, :headline, TRUE) RETURNING id"
        exercise_id = db.session.execute(sql, {"course_id":course_id, "type":type, "headline":headline}).fetchone()[0]
        db.session.commit()
        
        if type == 0:
            return add_exercise_text(exercise_id, exercise)

        elif type == 1:
            return add_exercise_mchoice(exercise_id, exercise)
        
    except:
        return False

def add_exercise_text(exercise_id, exercise):
    try:
        question = exercise[2]
        answer = exercise[3]
        sql = "INSERT INTO exercises_text (exercise_id, question, correct_answer, visible) VALUES (:exercise_id, :question, :answer, TRUE)"
        db.session.execute(sql, {"exercise_id":exercise_id, "question":question, "answer":answer})
        db.session.commit()
        return True
    except:
        return False

def add_exercise_mchoice(exercise_id, exercise):
    try:
        question = exercise[2]
        answer = exercise[3]
        a = exercise[4]
        b = exercise[5]
        c = exercise[6]

        sql = "INSERT INTO exercises_mchoice (exercise_id, question, correct_answer, option_a, option_b, option_c, visible) VALUES (:exercise_id, :question, :answer, :a, :b, :c, TRUE)"
        db.session.execute(sql, {"exercise_id":exercise_id, "question":question, "answer":answer, "a":a, "b":b, "c":c})
        db.session.commit()
        return True
    except:
        return False