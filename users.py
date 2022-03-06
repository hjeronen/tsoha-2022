import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash


def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, role, visible) VALUES (:name, :password, :role, TRUE)"
        db.session.execute(sql, {"name":username, "password":hash_value, "role":role})
        db.session.commit()
        return True
    except:
        return False

def login(username, password):
    try:
        sql = "SELECT id, password, role FROM users WHERE username=:username AND visible=TRUE"
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if not user:
            return False
        hash_value = user.password
        if not check_password_hash(hash_value, password):
            return False
        session["user_id"] = user[0]
        session["user_name"] = username
        session["user_role"] = user[2]
        session["csrf_token"] = os.urandom(16).hex()
        return True
    except:
        return False

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["user_role"]
    return True

def logged_in():
    return session.get("user_id", 0)

def has_userinfo():
    if not logged_in():
        return False
    return get_userinfo()

def delete_account():
    user_id = session["user_id"]
    try:
        sql = "UPDATE users SET visible=FALSE WHERE id=:userid"
        db.session.execute(sql, {"userid":user_id})
        db.session.commit()
        logout()
        return True
    except:
        return False

def save_user_info(firstname, lastname, student_number):
    user_id = session["user_id"]
    if session["user_role"] == 'student':
        try:
            sql = "INSERT INTO students (user_id, firstname, lastname, student_number) " \
                  "VALUES (:user_id, :firstname, :lastname, :student_number)"
            db.session.execute(sql, {"user_id":user_id,
                                     "firstname":firstname,
                                     "lastname":lastname,
                                     "student_number":student_number})
            db.session.commit()
            return True
        except:
            return False
    else:
        try:
            sql = "INSERT INTO teachers (user_id, firstname, lastname) " \
              "VALUES (:user_id, :firstname, :lastname)"
            db.session.execute(sql, {"user_id":user_id,
                                 "firstname":firstname,
                                 "lastname":lastname})
            db.session.commit()
            return True
        except:
            return False

def get_user_id():
    return session.get("user_id", 0)

def get_userinfo():
    user_id = session["user_id"]
    if session["user_role"] == 'student':
        sql = "SELECT S.firstname, S.lastname, S.student_number " \
              "FROM students S WHERE S.user_id=:user_id"
        return db.session.execute(sql, {"user_id":user_id}).fetchall()
    if session["user_role"] == 'teacher':
        sql = "SELECT T.firstname, T.lastname FROM teachers T WHERE T.user_id=:user_id"
        return db.session.execute(sql, {"user_id":user_id}).fetchall()
    return False

def get_user_role():
    return session.get("user_role", "no role")

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
