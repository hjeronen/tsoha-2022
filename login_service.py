import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash


def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, role) VALUES (:name, :password, :role)"
        db.session.execute(sql, {"name":username, "password":hash_value, "role":role})
        db.session.commit()
        return True
    except:
        return False

def login(username, password):
    try:
        sql = "SELECT id, password, role FROM users WHERE username=:username"
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