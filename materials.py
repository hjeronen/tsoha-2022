from db import db

def update_material(id, headline, body):
    try:
        sql = "UPDATE materials SET (headline, body) = (:headline, :body) WHERE id=:id"
        db.session.execute(sql, {"headline":headline, "body":body, "id":id})
        db.session.commit()
        return True
    except:
        return False

def delete_material(id):
    try:
        sql = "DELETE FROM materials WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    except:
        return False

def get_material(id):
    sql = "SELECT headline, body FROM materials WHERE id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()

def get_course_materials(course_id):
    sql = "SELECT id, headline FROM materials WHERE course_id=:course_id ORDER BY id"
    return db.session.execute(sql, {"course_id":course_id}).fetchall()

def save_material(course_id, headline, body):
    try:
        sql = "INSERT INTO materials (course_id, headline, body) VALUES (:course_id, :headline, :body)"
        db.session.execute(sql, {"course_id":course_id, "headline":headline, "body":body})
        db.session.commit()
        return True
    except:
        return False