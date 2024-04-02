import os
import json

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta


from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///pets.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/")
@login_required
def index():
    """Show portfolio of pets"""
    rows = db.execute("SELECT name, type, date_of_birth, sex, 0 as age, notes FROM pets JOIN pet_types ON pets.pet_type_id = pet_types.id WHERE pets.user_id = ? ORDER BY name", session["user_id"])
    # define function calculate age of pet
    for row in rows:
        birthDate = row["date_of_birth"]
        def calculateAge(birthDate):
            today= date.today()
            age = relativedelta(today, datetime.strptime(birthDate, '%Y-%m-%d'))
            row["age"] = age.years
            return age.years
    # Call calculateAge function
        calculateAge(birthDate)
    return render_template("Index.html", rows = rows)



@app.route("/addPetType", methods=["GET", "POST"])
@login_required
def addPetType():
    """Add Pet Type"""
    defaultPetType = db.execute("SELECT user_id, type FROM pet_types WHERE user_id = ?", session["user_id"])
    # Add pet type
    if request.method == "POST":
        petType = request.form.get("petType")
        # check pet type is required
        if not petType:
            return apology("Pet Type is required field")
        # check pet type already existed in DB
        existedPetType = db.execute("SELECT * FROM pet_types WHERE user_id =? and UPPER(type) =?", session["user_id"], petType.upper())
        if len(existedPetType) > 0:
            return apology("Pet type already existed")
        db.execute("INSERT INTO pet_types(user_id, type) VALUES(?,?)", session["user_id"], petType)
        return render_template("success.html")
    else:
        return render_template("petType.html", defaultPetType=defaultPetType)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

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



@app.route("/addPet", methods=["GET", "POST"])
@login_required
def addPet():
    availablePetTypesInDB = db.execute("SELECT * FROM pet_types WHERE user_id = ?", session["user_id"], )
    """Add pet."""
    if request.method == "POST":
        petType = request.form.get("petType")
        petName = request.form.get("petName")
        dateOfBirth = request.form.get("dob")
        sex = request.form.get("sex")
        note = request.form.get("addNote")
        if not petType:
            return apology("Pet Type is required")
        if not petName:
            return apology("Pet Name is required")
        if not dateOfBirth:
            return apology("Date of Birth is required")
        petTypeId = db.execute("SELECT id FROM pet_types WHERE user_id = ? and type = ?", session["user_id"], petType)
        petType_Id = petTypeId[0]["id"]
        existedNameInDB = db.execute("SELECT name FROM pets WHERE user_id = ? and UPPER(name) = ?", session["user_id"], petName.upper())
        if len(existedNameInDB) > 0:
            return apology("Pet Name already existed")
        AddedPets = db.execute("INSERT INTO pets(user_id, pet_type_id, name, date_of_birth, sex, notes) VALUES(?,?,?,?,?,?)", session["user_id"], petType_Id, petName, dateOfBirth, sex, note)
        return render_template("success.html")
    else:
        return render_template("addPet.html", availablePetTypesInDB=availablePetTypesInDB)



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword = request.form.get("passwordConfirmation")
        # check not input username
        if not username:
            return apology("must provide username", 400)
        # check max length of username
        if len(username) > 50:
            return apology("max length of username is 50 characters")
        # check not input password
        if not password:
            return apology("must provide password", 400)
        # check not input confirm password
        if not confirmPassword:
            return apology("must provide password confirmation", 400)
        # check password and confirm password does not match
        if confirmPassword != password:
            return apology("password and confirm password do not match", 400)
        # check username already existed in DB
        existingUsers = db.execute("SELECT * FROM users WHERE UPPER(username) = ?", username.upper())
        if len(existingUsers) > 0:
            return apology(
                "username already existed, please enter another username", 400
            )
        # generate password hash
        hashedPassword = generate_password_hash(
            password, method="pbkdf2", salt_length=16
        )
        # insert user to DB, and log user in, and redirect user to porfolio page
        userId = db.execute(
            "INSERT INTO users(username, hash) VALUES(?,?)", username, hashedPassword
        )
        session["user_id"] = userId
        # registered user has these pet types by default
        db.execute("INSERT INTO pet_types(user_id, type) VALUES(?, 'Cat')", session["user_id"])
        db.execute("INSERT INTO pet_types(user_id, type) VALUES(?, 'Dog')", session["user_id"])

        # regstered user has these pet service types & categories by default
        serviceTypeId = db.execute("INSERT INTO service_types(user_id, type) VALUES(?, 'Food')", session["user_id"])
        db.execute("INSERT INTO categories(user_id, service_type_id, category) VALUES(?, ?, 'Dry food')", session["user_id"], serviceTypeId)
        db.execute("INSERT INTO categories(user_id, service_type_id, category) VALUES(?, ?, 'Canned food')", session["user_id"], serviceTypeId)
        db.execute("INSERT INTO categories(user_id, service_type_id, category) VALUES(?, ?, 'Semi-moist food')", session["user_id"], serviceTypeId)
        db.execute("INSERT INTO categories(user_id, service_type_id, category) VALUES(?, ?, 'Fresh pet food')", session["user_id"], serviceTypeId)

        serviceTypeId = db.execute("INSERT INTO service_types(user_id, type) VALUES(?, 'Treats')", session["user_id"])
        db.execute("INSERT INTO categories(user_id, service_type_id, category) VALUES(?, ?, 'Dog treats')", session["user_id"], serviceTypeId)
        db.execute("INSERT INTO categories(user_id, service_type_id, category) VALUES(?, ?, 'Cat treats')", session["user_id"], serviceTypeId)
        db.execute("INSERT INTO categories(user_id, service_type_id, category) VALUES(?, ?, 'Dental treats')", session["user_id"], serviceTypeId)
        db.execute("INSERT INTO categories(user_id, service_type_id, category) VALUES(?, ?, 'Bird treats')", session["user_id"], serviceTypeId)

        serviceTypeId = db.execute("INSERT INTO service_types(user_id, type) VALUES(?, 'Pet supplies')", session["user_id"])
        db.execute("INSERT INTO categories(user_id, service_type_id, category) VALUES(?, ?, 'Beds')", session["user_id"], serviceTypeId)
        db.execute("INSERT INTO categories(user_id, service_type_id, category) VALUES(?, ?, 'Feeder')", session["user_id"], serviceTypeId)
        db.execute("INSERT INTO categories(user_id, service_type_id, category) VALUES(?, ?, 'Cleaning supplies')", session["user_id"], serviceTypeId)

        serviceTypeId = db.execute("INSERT INTO service_types(user_id, type) VALUES(?, 'Pet services')", session["user_id"])
        db.execute("INSERT INTO categories(user_id, service_type_id, category) VALUES(?, ?, 'Veterinary care')", session["user_id"], serviceTypeId)
        db.execute("INSERT INTO categories(user_id, service_type_id, category) VALUES(?, ?, 'Grooming')", session["user_id"], serviceTypeId)
        db.execute("INSERT INTO categories(user_id, service_type_id, category) VALUES(?, ?, 'Training classes')", session["user_id"], serviceTypeId)
        db.execute("INSERT INTO categories(user_id, service_type_id, category) VALUES(?, ?, 'Petshotel Boarding')", session["user_id"], serviceTypeId)
        db.execute("INSERT INTO categories(user_id, service_type_id, category) VALUES(?, ?, 'Doggie day camp')", session["user_id"], serviceTypeId)

        return redirect("/login")
    else:
        return render_template("register.html")



@app.route("/addServiceType", methods=["GET", "POST"])
@login_required
def addServiceType():
    """Add Pet Service Type"""
    defaultServiceTypes = db.execute("SELECT type FROM service_types WHERE user_id = ?", session["user_id"])
    if request.method == "POST":
        serviceType_forPet = request.form.get("petServiceType")
        # check pet service type is required
        if not serviceType_forPet:
            return apology("Pet Service Type is required field")
        # check pet service type already existed
        existedPetServiceTypeInDB = db.execute("SELECT type FROM service_types WHERE user_id = ? and UPPER(type) = ?", session["user_id"], serviceType_forPet.upper())
        if len(existedPetServiceTypeInDB) > 0:
            return apology("Service Type already existed")
        db.execute("INSERT INTO service_types(user_id, type) VALUES(?, ?)", session["user_id"], serviceType_forPet)
        return render_template("success.html")
    else:
        return render_template("serviceType.html", defaultServiceTypes = defaultServiceTypes )



@app.route("/addCategory", methods=["GET", "POST"])
@login_required
def addCategory():
    """Add Pet Category"""
    serviceTypes = db.execute("SELECT id, type FROM service_types WHERE user_id = ?", session["user_id"])
    categories = db.execute("SELECT id, service_type_id, category FROM categories WHERE user_id = ?", session["user_id"])
    if request.method == "POST":
        selectedPetServicetype = request.form.get("serviceType")
        petCategory = request.form.get("petCategory")
        # check must select pet service type before adding pet category
        if not selectedPetServicetype:
            return apology("Pet service type is required before adding pet category")
        # check pet category is required
        if not petCategory:
            return apology("pet Category input field is required")

        existedPetCategoryInDB = db.execute("SELECT user_id, service_type_id, category FROM categories WHERE user_id=? and service_type_id=? and UPPER(category) =?", session["user_id"], selectedPetServicetype, petCategory.upper())
        if len(existedPetCategoryInDB) > 0:
            return apology('Pet category already existed')
        db.execute("INSERT INTO categories(user_id, service_type_id, category) VALUES(?,?,?)", session["user_id"], selectedPetServicetype, petCategory)
        return render_template("success.html")
    else:
        return render_template("category.html", serviceTypes = serviceTypes, categories = categories)



@app.route("/addExpense", methods=["GET", "POST"])
@login_required
def addExpense():
    """Expenses"""
    serviceTypesInDB = db.execute("SELECT id, type FROM service_types WHERE user_id=?", session["user_id"])
    categories = db.execute("SELECT id, service_type_id, category FROM categories WHERE user_id=?", session["user_id"])
    availablePetsInDB = db.execute("SELECT id, name FROM pets WHERE user_id =?", session["user_id"])
    if request.method == "POST":
        petServiceType = request.form.get("serviceType")
        petCategory = request.form.get("category")
        petId = request.form.get("petName")
        description = request.form.get("description")
        amount = request.form.get("amount")
        date = request.form.get("date")
        today = datetime.now().date()
        # check pet service type is required
        if not petServiceType:
            return apology("Pet service type is required")
        # check description is required
        if not description:
            return apology("description is required")
        # check amount is required
        if not amount:
            return apology("amount is required")
        # check amount is positive number
        if not is_number(amount) or float(amount) < 0:
            return apology("amount must be positive number")
        # check date is required
        if not date:
            return apology("date is required")
        # check input date not in the future
        userDateInput = datetime.strptime(date, '%Y-%m-%d').date()
        if userDateInput > today:
            return apology("date should not be future date")

        db.execute("INSERT INTO expenses(user_id, service_type_id, category_id, pet_id, amount, description, expense_date) VALUES(?,?,?,?,?,?,?)", session["user_id"], petServiceType, petCategory, petId, amount, description, date)
        return render_template("success.html")
    else:
        return render_template("addExpense.html", serviceTypesInDB=serviceTypesInDB, categories=categories, availablePetsInDB=availablePetsInDB)



@app.route("/expenseHistory")
@login_required
def expenseHistory():
    """Show history of expense for pets"""
    rows = db.execute(
        "SELECT expense_date, type, category, name, description, amount " +
        "FROM expenses " +
        "JOIN service_types ON expenses.service_type_id = service_types.id " +
        "JOIN categories ON expenses.category_id = categories.id " +
        "LEFT JOIN pets ON expenses.pet_id = pets.id " +
        "WHERE expenses.user_id = ? " +
        "ORDER BY expense_date ",
        session["user_id"]
        )

    print(rows)
    total = 0
    for row in rows:
        amount = row["amount"]
        amountRound = round(amount,2)
        amountDisplay = usd(amountRound)
        row["amount"] = amountDisplay
        total += amount

    totalRound = round(total,2)
    totalDisplay = usd(totalRound)

    return render_template("expenseHistory.html", rows=rows, totalDisplay=totalDisplay  )



@app.route("/success", methods=["GET", "POST"])
@login_required
def success():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("success.html")



def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
