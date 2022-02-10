from db import db

def add_exercise(course_id, exercise):
    type = exercise[0]
    question = exercise[1]
    answer = exercise[2]
    try:
        sql = "INSERT INTO exercises (course_id, type, question, correct_answer, visible) VALUES (:course_id, :type, :question, :answer, TRUE) RETURNING id"
        exercise_id = db.session.execute(sql, {"course_id":course_id, "type":type, "question":question, "answer":answer}).fetchone()[0]
        db.session.commit()

        if type == 1:
            a = exercise[3]
            b = exercise[4]
            c = exercise[5]
            return add_multiple_choice_options(exercise_id, a, b, c)
        return True
    except:
        return False
    
        

def add_multiple_choice_options(exercise_id, a, b, c):
    try:
        sql = "INSERT INTO exercise_options (exercise_id, option_a, option_b, option_c, visible) VALUES (:exercise_id, :a, :b, :c, TRUE)"
        db.session.execute(sql, {"exercise_id":exercise_id, "a":a, "b":b, "c":c})
        db.session.commit()
        return True
    except:
        return False