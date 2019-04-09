import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import *

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///sparta.db")


@app.route("/")
@login_required
def index():
    """Show a menu of all exercises"""
    return render_template("index.html")

@app.route("/bench", methods=["GET", "POST"])
@login_required
def bench():
    """Show history of lifts"""

    exercise = "bench"
    exercise_goal = exercise + "_goal"

    # Check if the user has made any entries in the sets table
    result = db.execute("SELECT * FROM maxrep WHERE user_id = :user_id", user_id = session["user_id"])

    # Getting the current max rep and the goal
    current = result[0]["bench"]
    goal = result[0]["bench_goal"]
    remaining = goal - current
    if request.method == "POST":
        if current == 0:
            # Inserting first set
            insert_set(exercise, 1, 1, request.form.get("benchORM"))

            # Updating the current bench for the first time
            update_maxrep(exercise, request.form.get("benchORM"))

            # Updating the goal for the first time
            update_maxrep(exercise_goal, request.form.get("goal"))

            bench = float(request.form.get("benchORM"))
            goal = float(request.form.get("goal"))

            return render_template("bench.html", bench = bench, goal = goal, remaining = goal - bench, history = history_of_exercise(exercise))
        else:
            # Recording a new lift
            insert_set(exercise, request.form.get("sets"), request.form.get("reps"), request.form.get("weight"))
            new_record = float(request.form.get("weight"))
            if new_record > current:
                if new_record >= goal:
                    update_maxrep(exercise_goal, new_record + 5)
                update_maxrep(exercise, new_record)
            result = db.execute("SELECT * FROM maxrep WHERE user_id = :user_id", user_id = session['user_id'])
            current = result[0]["bench"]
            goal = result[0]["bench_goal"]
            remaining = goal - current
            return render_template("bench.html", bench = current, goal = goal, remaining = remaining, history = history_of_exercise(exercise))
    else:
        return check_and_render("bench", current, goal, history_of_exercise(exercise))

@app.route("/squat", methods=["GET", "POST"])
@login_required
def squat():
    """Show history of squats"""

    exercise = "squat"
    exercise_goal = exercise + "_goal"

    # Check if the user has made any entries in the sets table
    result = db.execute("SELECT * FROM maxrep WHERE user_id = :user_id", user_id = session["user_id"])

    # Getting the current max rep and the goal
    current = result[0]["squat"]
    goal = result[0]["squat_goal"]
    remaining = goal - current
    if request.method == "POST":
        if current == 0:
            # Inserting first set
            insert_set(exercise, 1, 1, request.form.get("squatORM"))

            # Updating the current squat for the first time
            update_maxrep(exercise, request.form.get("squatORM"))

            # Updating the goal for the first time
            update_maxrep(exercise_goal, request.form.get("goal"))

            squat = float(request.form.get("squatORM"))
            goal = float(request.form.get("goal"))

            return render_template("squat.html", squat = squat, goal = goal, remaining = goal - squat, history = history_of_exercise(exercise))
        else:
            # Recording a new lift
            insert_set(exercise, request.form.get("sets"), request.form.get("reps"), request.form.get("weight"))
            new_record = float(request.form.get("weight"))
            if new_record > current:
                if new_record >= goal:
                    update_maxrep(exercise_goal, new_record + 5)
                update_maxrep(exercise, new_record)
            result = db.execute("SELECT * FROM maxrep WHERE user_id = :user_id", user_id = session['user_id'])
            current = result[0]["squat"]
            goal = result[0]["squat_goal"]
            remaining = goal - current
            return render_template("squat.html", squat = current, goal = goal, remaining = remaining, history = history_of_exercise(exercise))
    else:
        return check_and_render("squat", current, goal, history_of_exercise(exercise))

@app.route("/deadlift", methods=["GET", "POST"])
@login_required
def deadlift():
    """Show history of deadlifts"""

    exercise = "deadlift"
    exercise_goal = exercise + "_goal"

    # Check if the user has made any entries in the sets table
    result = db.execute("SELECT * FROM maxrep WHERE user_id = :user_id", user_id = session["user_id"])

    # Getting the current max rep and the goal
    current = result[0]["deadlift"]
    goal = result[0]["deadlift_goal"]
    remaining = goal - current
    if request.method == "POST":
        if current == 0:
            # Inserting first set
            insert_set(exercise, 1, 1, request.form.get("deadliftORM"))

            # Updating the current deadlift for the first time
            update_maxrep(exercise, request.form.get("deadliftORM"))

            # Updating the goal for the first time
            update_maxrep(exercise_goal, request.form.get("goal"))

            deadlift = float(request.form.get("deadliftORM"))
            goal = float(request.form.get("goal"))

            return render_template("deadlift.html", deadlift = deadlift, goal = goal, remaining = goal - deadlift, history = history_of_exercise(exercise))
        else:
            # Recording a new lift
            insert_set(exercise, request.form.get("sets"), request.form.get("reps"), request.form.get("weight"))
            new_record = float(request.form.get("weight"))
            if new_record > current:
                if new_record >= goal:
                    update_maxrep(exercise_goal, new_record + 5)
                update_maxrep(exercise, new_record)
            result = db.execute("SELECT * FROM maxrep WHERE user_id = :user_id", user_id = session['user_id'])
            current = result[0]["deadlift"]
            goal = result[0]["deadlift_goal"]
            remaining = goal - current
            return render_template("deadlift.html", deadlift = current, goal = goal, remaining = remaining, history = history_of_exercise(exercise))
    else:
        return check_and_render("deadlift", current, goal, history_of_exercise(exercise))

@app.route("/overheadpress", methods=["GET", "POST"])
@login_required
def overheadpress():
    """Show history of overheadpress"""

    exercise = "overheadpress"
    exercise_goal = exercise + "_goal"

    # Check if the user has made any entries in the sets table
    result = db.execute("SELECT * FROM maxrep WHERE user_id = :user_id", user_id = session["user_id"])

    # Getting the current max rep and the goal
    current = result[0]["overheadpress"]
    goal = result[0]["overheadpress_goal"]
    remaining = goal - current
    if request.method == "POST":
        if current == 0:
            # Inserting first set
            insert_set(exercise, 1, 1, request.form.get("overheadpressORM"))

            # Updating the current overheadpress for the first time
            update_maxrep(exercise, request.form.get("overheadpressORM"))

            # Updating the goal for the first time
            update_maxrep(exercise_goal, request.form.get("goal"))

            overheadpress = float(request.form.get("overheadpressORM"))
            goal = float(request.form.get("goal"))

            return render_template("overheadpress.html", overheadpress = overheadpress, goal = goal, remaining = goal - overheadpress, history = history_of_exercise(exercise))
        else:
            # Recording a new lift
            insert_set(exercise, request.form.get("sets"), request.form.get("reps"), request.form.get("weight"))
            new_record = float(request.form.get("weight"))
            if new_record > current:
                if new_record >= goal:
                    update_maxrep(exercise_goal, new_record + 5)
                update_maxrep(exercise, new_record)
            result = db.execute("SELECT * FROM maxrep WHERE user_id = :user_id", user_id = session['user_id'])
            current = result[0]["overheadpress"]
            goal = result[0]["overheadpress_goal"]
            remaining = goal - current
            return render_template("overheadpress.html", overheadpress = current, goal = goal, remaining = remaining, history = history_of_exercise(exercise))
    else:
        return check_and_render("overheadpress", current, goal, history_of_exercise(exercise))

@app.route("/pullups", methods=["GET", "POST"])
@login_required
def pullups():
    """Show history of pullups"""

    exercise = "pullups"
    exercise_goal = exercise + "_goal"

    # Check if the user has made any entries in the sets table
    result = db.execute("SELECT * FROM maxrep WHERE user_id = :user_id", user_id = session["user_id"])

    # Getting the current max rep and the goal
    current = result[0]["pullups"]
    goal = result[0]["pullups_goal"]
    remaining = goal - current
    if request.method == "POST":
        if current == 0:
            # Inserting first set
            insert_set(exercise, 1, request.form.get("pullupsORM"), 0)

            # Updating the current pullups for the first time
            update_maxrep(exercise, request.form.get("pullupsORM"))

            # Updating the goal for the first time
            update_maxrep(exercise_goal, request.form.get("goal"))

            pullups = int(request.form.get("pullupsORM"))
            goal = int(request.form.get("goal"))

            return render_template("pullups.html", pullups = pullups, goal = goal, remaining = goal - pullups, history = history_of_exercise(exercise))
        else:
            # Recording a new lift
            insert_set(exercise, request.form.get("sets"), request.form.get("reps"), 0)
            new_record = int(request.form.get("reps"))
            if new_record > current:
                if new_record >= goal:
                    update_maxrep(exercise_goal, new_record + 5)
                update_maxrep(exercise, new_record)
            result = db.execute("SELECT * FROM maxrep WHERE user_id = :user_id", user_id = session['user_id'])
            current = result[0]["pullups"]
            goal = result[0]["pullups_goal"]
            remaining = int(goal) - int(current)
            return render_template("pullups.html", pullups = current, goal = goal, remaining = remaining, history = history_of_exercise(exercise))
    else:
        return check_and_render("pullups", current, goal, history_of_exercise(exercise))

@app.route("/nutrition", methods=["GET", "POST"])
@login_required
def nutrition():
    caloriesGoal = db.execute("SELECT calories FROM calories WHERE user_id = :user_id", user_id = session["user_id"])
    if caloriesGoal[0]["calories"] == 0:
        return render_template("nutrition.html", caloriesGoal = caloriesGoal[0], dailyCalories = 0)
    if request.method == "POST":
        calorieIntake = request.form.get("calorieIntake")
        food = request.form.get("food")
        checkDate = select_from_calorieintake("user_id")
        if not checkDate:
             db.execute("INSERT INTO calorieintake (user_id, food, calories, date) VALUES (:user_id, :food, :calorieIntake, :date)",
                     user_id = session["user_id"],
                     food = food,
                     calorieIntake = calorieIntake,
                     date = datetime.date.today())
        else:
            calories = select_from_calorieintake("calories")
            recordedFood = select_from_calorieintake("food")
            db.execute ("""UPDATE calorieintake SET calories=:calories WHERE user_id = :user_id AND date = :date""",
                calories = calories[0]['calories'] + int(calorieIntake),
                user_id = session['user_id'],
                date = datetime.date.today())
            db.execute ("""UPDATE calorieintake SET food=:food WHERE user_id = :user_id AND date = :date""",
                food = recordedFood[0]['food'] + food,
                user_id = session['user_id'],
                date = datetime.date.today())

        return render_template("nutrition.html", caloriesGoal = caloriesGoal[0], dailyCalories = calories[0]["calories"] + int(calorieIntake))
    else:
        calories = select_from_calorieintake("calories")
        if not calories:
            return render_template("nutrition.html", caloriesGoal = caloriesGoal[0], dailyCalories = 0)
        return render_template("nutrition.html", caloriesGoal = caloriesGoal[0], dailyCalories = calories[0]["calories"])

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("loginInvalid.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/goals", methods=["GET", "POST"])
@login_required
def goals():
    """Show the current goals of the user"""
    goals = db.execute("SELECT bench_goal, squat_goal, deadlift_goal, overheadpress_goal, pullups_goal FROM maxrep WHERE user_id = :user_id", user_id = session["user_id"])
    return render_template("goals.html", goals = goals)

@app.route("/stats", methods=["GET", "POST"])
@login_required
def stats():
    """Show the current stats of the user."""
    stats = db.execute("SELECT bench, squat, deadlift, overheadpress, pullups FROM maxrep WHERE user_id = :user_id", user_id = session["user_id"])
    return render_template("stats.html", stats = stats)

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """Show history of all lifts"""
    history = db.execute("SELECT exercise, sets, reps, kg, date FROM sets WHERE user_id = :user_id", user_id = session["user_id"])
    return render_template("history.html", history = history)

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Profile page of the user"""
    username = db.execute("SELECT username FROM users WHERE id = :user_id", user_id = session["user_id"])
    posts = db.execute("SELECT post, id FROM posts WHERE user_id = :user_id", user_id = session["user_id"])

    # Reverse the posts so that the newest are on top
    posts.reverse()
    if request.method == "POST":
        post = request.form.get("post")

        # If there is no post, the delete button must be pressed
        if not post:
            return delete_post(username)

        # If there is post, insert it
        return insert_post(username, post)
    else:
        return render_template("profile.html", username = username[0]["username"], posts = posts)

@app.route("/newpass", methods=["GET", "POST"])
@login_required
def newpass():
    """Changes the user's password"""
    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE id = :user_id",
                          user_id = session["user_id"])

        # Ensure password is correct, if not render the error template
        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("newpassInvalid.html")
        else:
            # If it is hash the new pass and update the old value
            hash = generate_password_hash(request.form.get("newpassword"))
            update = db.execute("UPDATE users SET hash=:value WHERE id = :user_id",
                    value = hash,
                    user_id = session['user_id'])
            return index()
    else:
        return render_template("newpass.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # Hashing the password from the form
        hash = generate_password_hash(request.form.get("password"))

        # Username and hash as placeholders to protect from injection attacks
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
        username = request.form.get("username"), hash = hash)

        # If the username is taken render the new template
        if not result:
            return render_template("registerAlreadyExists.html")

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # When a new user is registered create a new entry in the db for their lifts
        db.execute("""INSERT INTO maxrep (user_id, bench, squat, deadlift, overheadpress, pullups,
                    bench_goal, squat_goal, deadlift_goal, overheadpress_goal, pullups_goal)
                    VALUES (:user_id, :bench, :squat, :deadlift, :overheadpress, :pullups, :bench_goal, :squat_goal, :deadlift_goal,
                    :overheadpress_goal, :pullups_goal)""",
                    user_id = session['user_id'],
                    bench = 0, squat = 0, deadlift = 0, overheadpress = 0, pullups = 0,
                    bench_goal = 0, squat_goal = 0, deadlift_goal = 0, overheadpress_goal = 0, pullups_goal = 0)

        # Also create an entry in the db for their calories
        db.execute("""INSERT INTO calories (user_id, calories) VALUES (:user_id, :calories)""",
                            user_id = session['user_id'],
                            calories = 0)

        # Redirect user to home page
        return index()

    else:
        return render_template("register.html")

@app.route("/calories", methods=["GET", "POST"])
@login_required
def calories():
    if request.method == "POST":
        caloriesGoal = request.form.get("caloriesGoal")
        db.execute ("""UPDATE calories SET calories=:calories WHERE user_id = :user_id""",
                calories = caloriesGoal,
                user_id = session['user_id'])
        return render_template("calories.html")
    else:
        return render_template("calories.html")

def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
