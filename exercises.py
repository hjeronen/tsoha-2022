from db import db

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