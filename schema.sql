\connect tsoha

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
);

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    firstname TEXT,
    lastname TEXT,
    student_number TEXT
);

CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    firstname TEXT,
    lastname TEXT
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    course_name TEXT,
    teacher_id INTEGER REFERENCES teachers ON DELETE SET NULL,
    description TEXT
);

CREATE TABLE course_attendances (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses ON DELETE RESTRICT,
    student_id INTEGER REFERENCES students ON DELETE CASCADE
);

-- CREATE TABLE exercises (
--     id SERIAL PRIMARY KEY,
--     course_id INTEGER REFERENCES courses ON DELETE CASCADE,
--     question TEXT,
--     type TEXT,
--     right_answer TEXT,
--     points INTEGER
-- );

-- CREATE TABLE answers (
--     id SERIAL PRIMARY KEY,
--     student_id INTEGER REFERENCES students ON DELETE CASCADE,
--     exercise_id INTEGER REFERENCES exercises ON DELETE RESTRICT,
--     answer TEXT,
--     status BOOLEAN
-- );

-- CREATE TABLE materials (
--     id SERIAL PRIMARY KEY,
--     course_id INTEGER REFERENCES courses ON DELETE CASCADE,
--     link TEXT,
-- );
