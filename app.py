import redis
import json
from os import environ

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from functools import wraps
from helper import TransCalc, EnergyCalc, HousingCalc, consumeCalc, emission

app = Flask(__name__)
app.secret_key = "13080dWOd01"
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        print(session.get("user_id"))
        return f(*args, **kwargs)
    return decorated_function

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


app.config["SESSION_PERMANENT"] = True
app.permanent_session_lifetime = timedelta(minutes=50)
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = redis.from_url("redis://127.0.0.1:6379")
# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///footprint.db")


@app.route("/")
@login_required
def index():
    try:
        history = db.execute(
            "SELECT * from history where id=:id ORDER BY Date DESC", id=session["user_id"])
        if not history:
            raise Exception("No data found for user")

        all_emissions = emission(history)
    except:
        return render_template("index.html", nodata=True)
    print(db.execute(
            "SELECT * from history where id=:id ORDER BY Date DESC", id=session["user_id"]))
    total_emm = all_emissions.emmSum()
    kwargs = all_emissions.emmGraph()
    ratftprint = all_emissions.ftprint()
    return render_template("index.html", nodata=False, total_emm=total_emm, plot=kwargs,ratftprint=ratftprint)

@app.route("/about")
def about():
    return render_template("about.html")

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

        correct = 0
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["pwd"], request.form.get("password")):
            correct = 1
            return render_template("login.html", correct=correct)

        # Remember which user has logged in
        session["user_id"] = rows[0]["idx"]

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


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = str(request.form.get("username"))
        p_hash = str(generate_password_hash(request.form.get("password")))
        security = str(request.form.get("security"))
        user_exists = db.execute(
            "SELECT * FROM users WHERE username = :username", username=username)
        if user_exists:
            return render_template("register.html", user_exists=user_exists)
        else:
            db.execute("INSERT INTO users (username, pwd, secretkey) VALUES(:username, :hash, :security)",
                       username=username, hash=p_hash, security=security)
            return render_template("login.html")


@app.route("/reset", methods=["GET", "POST"])
def forgot():
    if request.method == "GET":
        return render_template("reset.html")
    else:
        security = str(request.form.get("security"))
        new_pass = str(generate_password_hash(request.form.get("password")))
        sec_passed = db.execute(
            "SELECT * from users WHERE secretkey=:security", security=security)
        if sec_passed == []:
            e = f"Incorrect response to security. Please try again"
            return render_template("reset.html", error=True, e=e)
        else:
            db.execute("UPDATE users SET pwd=:new_pass WHERE secretkey=:security",
                       new_pass=new_pass, security=security)
            return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        emission_type = request.form.get("emission-sel")
        date = request.form.get("date")
        if emission_type == "Transport":
            trans_type = request.form.get("trans-sel")
            trans_dist = float(request.form.get("trans-dist"))
            emission = "{:.3g}".format(TransCalc(trans_type, trans_dist))
        elif emission_type == "Food":
            meat = float(request.form.get("meat"))
            dairy = float(request.form.get("dairy"))
            bread = float(request.form.get("bread"))
            veggies = float(request.form.get("veggies"))
            snacks = float(request.form.get("snacks"))
            emission = "{:.3g}".format(
                143.9*meat+3.4*dairy+1.6*bread+2*veggies+2.5*snacks)
        elif emission_type == "Energy":
            energy_type = request.form.get("energy-sel")
            energy_use = float(request.form.get("energy-use"))
            emission = "{:.3g}".format(EnergyCalc(energy_type, energy_use))
        elif emission_type == "Water":
            water_use = float(request.form.get("water-use"))
            emission = "{:.3g}".format(0.03*water_use)
        elif emission_type == "Housing":
            house_sel = request.form.get("house-sel")
            peep_no = float(request.form.get("peep-no"))
            emission = "{:.3g}".format(HousingCalc(house_sel, peep_no))
        elif emission_type == "Consumer Goods":
            consume_sel = request.form.get("consume-sel")
            emission = "{:.3g}".format(consumeCalc(consume_sel))
        else:
            print("Error: Emission type invalid")
        db.execute("INSERT into history (id, Date, Type, COe) VALUES (:id, :date, :Type, :COe)",
                   id=session["user_id"], date=date, Type=emission_type, COe=emission)
        return redirect("/")


if __name__ == '__main__':
    app.run()
