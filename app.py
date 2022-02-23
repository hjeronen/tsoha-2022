from os import getenv
from flask import Flask

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes
import user_routes
import courses_routes
import exercises_routes
import materials_routes