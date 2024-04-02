import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
     # TODO: Add the user's entry into the database
    if request.method == "POST":
        Name = request.form.get("name")
        Month = request.form.get("month")
        Day = request.form.get("day")
        errors = []

        if not Name:
            errors.append('Please enter Name')
        if not Month:
            errors.append('Please enter Month')
        if not Day:
            errors.append('Please enter Day')
        if not Month.isdigit() or int(Month) > 12:
            errors.append('Invalid month')
        if not Day.isdigit() or int(Day) > 31:
            errors.append('Invalid Date')
        if errors:
            return render_template('index.html', errors = errors)

        db.execute("INSERT INTO birthdays(name, month, day)VALUES(?,?,?)", Name, Month,  Day)
        return redirect("/")
    else:
        # TODO: Display the entries in the database on index.html
        birthdayRows = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", rows = birthdayRows)


