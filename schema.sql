
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT,
    visible BOOLEAN
);

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE NO ACTION,
    firstname TEXT,
    lastname TEXT,
    student_number TEXT
);

CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE NO ACTION,
    firstname TEXT,
    lastname TEXT
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    course_name TEXT,
    teacher_id INTEGER REFERENCES users ON DELETE NO ACTION,
    description TEXT,
    visible BOOLEAN
);

CREATE TABLE course_attendances (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    student_id INTEGER REFERENCES users ON DELETE NO ACTION
);

CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    type INTEGER,
    headline TEXT,
    visible BOOLEAN
);

CREATE TABLE exercises_text (
    id SERIAL PRIMARY KEY,
    exercise_id INTEGER REFERENCES exercises,
    question TEXT,
    correct_answer TEXT
);

CREATE TABLE exercises_mchoice (
    id SERIAL PRIMARY KEY,
    exercise_id INTEGER REFERENCES exercises,
    question TEXT,
    correct_answer TEXT,
    option_a TEXT,
    option_b TEXT,
    option_c TEXT
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE NO ACTION,
    exercise_id INTEGER REFERENCES exercises,
    answer TEXT,
    correct BOOLEAN
);

CREATE TABLE materials (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    headline TEXT,
    body TEXT
);
