
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
    teacher_id INTEGER REFERENCES users ON DELETE SET NULL,
    description TEXT,
    visible BOOLEAN
);

CREATE TABLE course_attendances (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    student_id INTEGER REFERENCES users ON DELETE CASCADE
);

CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    type INTEGER,
    question TEXT,
    correct_answer TEXT,
    visible BOOLEAN
);

CREATE TABLE exercise_options (
    id SERIAL PRIMARY KEY,
    exercise_id INTEGER REFERENCES exercises,
    option_a TEXT,
    option_b TEXT,
    option_c TEXT,
    visible BOOLEAN
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students ON DELETE CASCADE,
    exercise_id INTEGER REFERENCES exercises,
    answer TEXT
);

-- CREATE TABLE materials (
--     id SERIAL PRIMARY KEY,
--     course_id INTEGER REFERENCES courses ON DELETE CASCADE,
--     link TEXT,
-- );
