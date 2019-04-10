import requests
import datetime
import psycopg2

from flask import redirect, render_template, request, session
from functools import wraps
from random import randint
from cs50 import SQL

db = SQL("postgres://njniejknyhtyxb:0efce18ce29dff8371f186ff15d5b5870945be5bb2a743a87ab4f706a6a929b3@ec2-54-246-92-116.eu-west-1.compute.amazonaws.com:5432/dd4jcgtmu8vngd")
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def check_and_render(exercise, dbCheck, goal, history):
    """
    Checks whether a user has previosly set a goal
    if he has, the function returns his stats
    otherwise it renders the goal template
    """
    if int(dbCheck) == 0:
        return render_template(exercise+"FirstTime.html")
    else:
        # if it is not zero, the dbCheck is the max current value
        if exercise == "bench":
            return render_template(exercise+".html", bench = dbCheck, goal = goal, remaining = goal - dbCheck, history = history)
        elif exercise == "squat":
            return render_template(exercise+".html", squat = dbCheck, goal = goal, remaining = goal - dbCheck, history = history)
        elif exercise == "deadlift":
            return render_template(exercise+".html", deadlift = dbCheck, goal = goal, remaining = goal - dbCheck, history = history)
        elif exercise == "pullups":
            return render_template(exercise+".html", pullups = dbCheck, goal = goal, remaining = goal - dbCheck, history = history)
        elif exercise == "overheadpress":
            return render_template(exercise+".html", overheadpress = dbCheck, goal = goal, remaining = goal - dbCheck, history = history)
# Shows history of an exercise
def history_of_exercise(exercise):
    """Gets the history of the user's exercise activity"""
    if exercise == "pullups":
        # There are no kg in the pullups
        history = db.execute("SELECT sets, reps, date FROM sets WHERE user_id = :user_id AND exercise = :exercise", user_id = session["user_id"], exercise = exercise)

    else:
        history = db.execute("SELECT sets, reps, kg, date FROM sets WHERE user_id = :user_id AND exercise = :exercise", user_id = session["user_id"], exercise = exercise)

    history.reverse()
    return history

def update_maxrep(exercise, goalOrCurrent):
    """Updates the goal or the current maxrep"""
    db.execute("UPDATE maxrep SET {}=:value WHERE user_id = :user_id".format(exercise),
                    value = goalOrCurrent,
                    user_id = session['user_id'])

def select_from_calorieintake(variable):
    return db.execute("SELECT {} FROM calorieIntake WHERE user_id = :user_id AND date = :date".format(variable),
                    user_id = session["user_id"],
                    date = datetime.date.today())


def insert_set(exercise, sets, reps, kg):
    """Insers sets and reps in the database"""
    db.execute("""INSERT INTO sets (user_id, exercise, sets, reps, kg, date)
                    VALUES (:user_id, :exercise, :sets, :reps, :kg, :date)""",
                    user_id = session['user_id'],
                    exercise = exercise,
                    sets = sets,
                    reps = reps,
                    kg = kg,
                    date = datetime.datetime.now())

def delete_post(username):
    delete_post = request.form.get("current_post")
    id_post = request.form.get("current_id")
    deletion = db.execute("DELETE FROM posts WHERE post = :post AND id = :id", post = delete_post, id = id_post)
    posts = db.execute("SELECT post, id FROM posts WHERE user_id = :user_id", user_id = session["user_id"])
    posts.reverse()
    return render_template("profile.html", username = username[0]["username"], posts = posts)

def insert_post(username, post):
    insertion = db.execute("INSERT INTO posts (user_id, post) VALUES (:user_id, :post)", user_id = session["user_id"], post = post)
    posts = db.execute("SELECT post, id FROM posts WHERE user_id = :user_id", user_id = session["user_id"])
    posts.reverse()
    return render_template("profile.html", username = username[0]["username"], posts = posts)

