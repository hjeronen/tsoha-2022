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
        sql = "SELECT c.id, c.course_name FROM courses c, course_attendances a " \
              "WHERE a.student_id=:id AND a.course_id=c.id AND c.visible=TRUE ORDER BY c.id"
        return db.session.execute(sql, {"id":user_id}).fetchall()

    if user_role == 'teacher':
        sql = "SELECT id, course_name FROM courses WHERE teacher_id=:id AND visible=TRUE ORDER BY id"
        return db.session.execute(sql, {"id":user_id}).fetchall()

    return False

def get_course(course_id):
    sql = "SELECT c.id, c.course_name, c.description, c.teacher_id, t.firstname, t.lastname " \
          "FROM courses c, teachers t " \
          "WHERE c.id=:course_id AND c.teacher_id=t.user_id AND c.visible=TRUE"
    return db.session.execute(sql, {"course_id":course_id}).fetchone()

def get_all_courses():
    sql = "SELECT id, course_name FROM courses WHERE visible=TRUE ORDER BY id"
    return db.session.execute(sql).fetchall()
