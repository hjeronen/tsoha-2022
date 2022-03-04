from db import db

def check_if_owner(user_id, course_id):
    course_teacher_id = get_course_teacher_id(course_id)
    if not course_teacher_id:
        return False
    return user_id == course_teacher_id[0]

def get_course_teacher_id(course_id):
    sql = "SELECT teacher_id FROM courses WHERE id=:course_id"
    return db.session.execute(sql, {"course_id":course_id}).fetchone()

def add_course(user_id, course_name, description):
    try:
        sql = "INSERT INTO courses (course_name, teacher_id, description, visible) " \
              "VALUES (:course_name, :teacher_id, :description, TRUE)"
        db.session.execute(sql, {"course_name":course_name,
                                 "teacher_id":user_id,
                                 "description":description})
        db.session.commit()
        return True
    except:
        return False

def update_course(user_id, course_id, course_name, description):
    try:
        sql = "UPDATE courses SET (course_name, description) = (:course_name, :description) " \
              "WHERE id=:course_id AND teacher_id=:user_id"
        db.session.execute(sql, {"course_name":course_name,
                                 "description":description,
                                 "course_id":course_id,
                                 "user_id":user_id})
        db.session.commit()
        return True
    except:
        return False

def delete_course(user_id, course_id):
    try:
        sql = "UPDATE courses SET visible=FALSE WHERE id=:course_id AND teacher_id=:user_id"
        db.session.execute(sql, {"course_id":course_id, "user_id":user_id})
        db.session.commit()
        return True
    except:
        return False

def check_if_student_is_enrolled(course_id, student_id):
    sql = "SELECT course_id, student_id FROM course_attendances " \
          "WHERE course_id=:course_id AND student_id=:student_id"
    result = db.session.execute(sql, {"course_id":course_id, "student_id":student_id}).fetchone()
    return result

def enroll_on_course(course_id, student_id):
    try:
        sql = "INSERT INTO course_attendances (course_id, student_id) VALUES (:course_id, :student_id)"
        db.session.execute(sql, {"course_id":course_id, "student_id":student_id})
        db.session.commit()
        return True
    except:
        return False

def get_users_courses(user_id, user_role):
    if user_role == 'student':
        sql = "SELECT C.id, C.course_name FROM courses C, course_attendances A " \
              "WHERE A.student_id=:id AND A.course_id=C.id AND C.visible=TRUE ORDER BY C.id"
        return db.session.execute(sql, {"id":user_id}).fetchall()

    if user_role == 'teacher':
        sql = "SELECT id, course_name FROM courses WHERE teacher_id=:id AND visible=TRUE ORDER BY id"
        return db.session.execute(sql, {"id":user_id}).fetchall()

    return False

def get_course(course_id):
    sql = "SELECT C.id, C.course_name, C.description, C.teacher_id, T.firstname, T.lastname " \
          "FROM courses C, teachers T " \
          "WHERE C.id=:course_id AND C.teacher_id=T.user_id"
    return db.session.execute(sql, {"course_id":course_id}).fetchone()

def get_all_courses():
    sql = "SELECT id, course_name FROM courses WHERE visible=true ORDER BY id"
    return db.session.execute(sql).fetchall()
