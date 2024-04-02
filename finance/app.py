import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""
    # get user's available cash in DB
    userRow = db.execute(
        "SELECT username, cash FROM users WHERE id = ?", session["user_id"]
    )
    availableCash = userRow[0]["cash"]
    cashBalance = round(availableCash, 2)
    grandTotal = cashBalance
    displayCash = usd(cashBalance)

    rows = db.execute(
        "SELECT user_id, symbol, name, total_shares, 0 as price, 0 as totalPrice FROM stock WHERE user_id = (?) ORDER BY symbol",
        session["user_id"],
    )
    for row in rows:
        symbol = row["symbol"]
        shares = row["total_shares"]
        # get current price
        lookupResult = lookup(symbol)
        currentPrice = lookupResult["price"]
        displayPrice = usd(currentPrice)
        row["price"] = displayPrice
        # calculate total
        total = currentPrice * float(shares)
        roundTotal = round(total, 2)
        grandTotal += roundTotal
        displayTotal = usd(roundTotal)
        row["totalPrice"] = displayTotal

    grandTotalDisplay = usd(grandTotal)
    return render_template(
        "index.html",
        rows=rows,
        displayCash=displayCash,
        grandTotalDisplay=grandTotalDisplay,
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # get user's available cash
    availableCashBalance = db.execute(
        "SELECT id, username, cash FROM users WHERE id = ?", session["user_id"]
    )
    cash = availableCashBalance[0]["cash"]
    cashBalance = round(cash, 2)
    cashDisplay = usd(cashBalance)

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        # check not input symbol
        if not symbol:
            return apology("Symbol is required")
        lookupResult = lookup(symbol)
        # check invalid symbol
        if not lookupResult:
            return apology("Invalid symbold")
        Name = lookupResult["name"]
        currentPrice = lookupResult["price"]
        # check not input shares
        if not shares:
            return apology("Number of shares is required")
        # check input shares is invalid data
        if not shares.isdigit() or int(shares) < 0:
            return apology("Number of shares must be a positive numbers")
        payment = lookupResult["price"] * float(shares)
        stockPayment = round(payment, 2)
        # check cannot affort that amount of stocks
        if stockPayment > cashBalance:
            return apology("Sorry, you cannot afford that amount of stocks")
        else:
            newCashBalance = cashBalance - stockPayment
            # check user already bought that stock before
            alreadyBoughtThatStock = db.execute(
                "SELECT user_id, symbol, total_shares FROM stock WHERE user_id = (?) and symbol = (?)",
                session["user_id"],
                symbol,
            )
            if len(alreadyBoughtThatStock) > 0:
                updateTotalShares = db.execute(
                    "UPDATE stock SET total_shares = total_shares + (?) WHERE user_id = (?) AND symbol = (?)",
                    shares,
                    session["user_id"],
                    symbol,
                )
            else:
                stockBuying = db.execute(
                    "INSERT INTO stock(user_id, symbol, name, total_shares) VALUES (?,?,?,?)",
                    session["user_id"],
                    symbol,
                    Name,
                    shares,
                )
            # update cash reflect the buy
            updatedCash = db.execute(
                "UPDATE users SET cash = (?) WHERE id = (?)",
                newCashBalance,
                session["user_id"],
            )
            # update stock transaction after the buy
            updateStockTransaction_buy = db.execute(
                "INSERT INTO stock_transaction(user_id, transaction_date, symbol, name, numbers_of_share, transaction_price, is_buy) VALUES (?,?,?,?,?,?,?)",
                session["user_id"],
                datetime.now(),
                symbol,
                Name,
                shares,
                currentPrice,
                1,
            )
            return redirect("/")
    else:
        return render_template("buy.html", cashDisplay=cashDisplay)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # get user's available cash in DB
    userRow = db.execute(
        "SELECT username, cash FROM users WHERE id = ?", session["user_id"]
    )
    availableCash = userRow[0]["cash"]
    cashBalance = round(availableCash, 2)
    grandTotal = cashBalance
    displayCash = usd(cashBalance)

    historyRows = db.execute(
        "SELECT transaction_date, symbol, name, is_buy, numbers_of_share, transaction_price FROM stock_transaction WHERE user_id = ? ORDER BY transaction_date",
        session["user_id"],
    )
    return render_template(
        "history.html", historyRows=historyRows, displayCash=displayCash
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symb = request.form.get("symbol")
        # check symbol is required
        if not symb:
            return apology("Symbol is required")
        result = lookup(symb)
        # check invalid symbol
        if not result:
            return apology("Invalid symbol , it does not exist")
        return render_template("quote.html", result=result)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmation")
        # check not input username
        if not username:
            return apology("must provide username", 400)
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
        existingUsers = db.execute("SELECT * FROM users WHERE username = ?", username)
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
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # get user's available cash
    availableCashBalance = db.execute(
        "SELECT id, username, cash FROM users WHERE id = ?", session["user_id"]
    )
    cash = availableCashBalance[0]["cash"]
    cashBalance = round(cash, 2)
    cashDisplay = usd(cashBalance)

    # get stock symbol of the user in DB
    symbolsInDB = db.execute(
        "SELECT symbol FROM stock WHERE user_id = ?", session["user_id"]
    )

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        # check not input symbol
        if not symbol:
            return apology("Symbol is required")
        lookupResult = lookup(symbol)
        Name = lookupResult["name"]
        currentPrice = lookupResult["price"]
        # check user does not own that stock
        stockOwnedAssociatedSymbol = db.execute(
            "SELECT user_id, symbol, total_shares FROM stock WHERE user_id = (?) and symbol = (?)",
            session["user_id"],
            symbol,
        )
        if not stockOwnedAssociatedSymbol:
            return apology("Sorry, you don't own that stock")
        # check not input shares
        if not shares:
            return apology("Number of shares is required")
        # check share must be positive number
        if not shares.isdigit() or int(shares) < 0:
            return apology("Number of shares must be a positive numbers")
        # check user does not own enough shares to sell
        totalSharesOwned = stockOwnedAssociatedSymbol[0]["total_shares"]
        if totalSharesOwned < int(shares):
            return apology("You don't own enough shares of that stock")
        if totalSharesOwned > int(shares):
            updateSell = db.execute(
                "UPDATE stock set total_shares = total_shares - (?) WHERE user_id = ? AND symbol = ?",
                int(shares),
                session["user_id"],
                symbol,
            )
        else:
            sellAllThatStock = db.execute(
                "DELETE FROM stock WHERE user_id = ? AND symbol = ?",
                session["user_id"],
                symbol,
            )
        # update cash reflect the sell
        proceeds = currentPrice * float(shares)
        newCash = cashBalance + proceeds
        updateCash = db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", newCash, session["user_id"]
        )
        # update stock transaction reflect the sell
        updateStockTransaction_sell = db.execute(
            "INSERT INTO stock_transaction(user_id, transaction_date, symbol, name, numbers_of_share, transaction_price, is_buy) VALUES (?,?,?,?,?,?,?)",
            session["user_id"],
            datetime.now(),
            symbol,
            Name,
            shares,
            currentPrice,
            0,
        )
        return redirect("/")
    else:
        return render_template(
            "sell.html", cashDisplay=cashDisplay, symbolsInDB=symbolsInDB
        )


@app.route("/addCash", methods=["GET", "POST"])
@login_required
def addCash():
    """add more cash"""
    availableCashBalance = db.execute(
        "SELECT id, username, cash FROM users WHERE id = ?", session["user_id"]
    )
    cash = availableCashBalance[0]["cash"]
    cashBalance = round(cash, 2)
    cashDisplay = usd(cashBalance)

    if request.method == "POST":
        cashAdded = request.form.get("addCash")
        if not cashAdded:
            return apology("Add cash field is required")
        if not cashAdded.isdigit() or int(cashAdded) <= 0:
            return apology("Amount of cash should be greater than zero")
        newCashBalance = cashBalance + float(cashAdded)
        updatedCash = db.execute(
            "UPDATE users SET cash = ?  WHERE id = ? ",
            newCashBalance,
            session["user_id"],
        )
        return redirect("/success")
    else:
        return render_template("addCash.html", cashDisplay=cashDisplay)


@app.route("/success", methods=["GET", "POST"])
@login_required
def success():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("success.html")
