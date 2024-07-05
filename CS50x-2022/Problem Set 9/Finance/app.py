import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as shares FROM stocks WHERE user_id = ? GROUP BY symbol HAVING (SUM(shares)) > 0", session["user_id"])
    cash = round(db.execute(
        "SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"], 2)
    totalStock = 0

    for stock in stocks:
        r = lookup(stock["symbol"])
        stock["name"] = r["name"]
        stock["price"] = r["price"]
        totalStock += stock["price"] * stock["shares"]

    return render_template("index.html", stocks=stocks, cash=cash, totalStock=totalStock)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        stock = lookup(symbol)

        try:
            shares = int(shares)
            if not shares > 1:
                return apology("THE INPUT IS NOT A POSITIVE INTEGER")
        except ValueError:
            return apology("THE INPUT IS NOT A POSITIVE INTEGER")

        if not stock:
            return apology("THE INPUT IS BLANK OR THE SYMBOL DOES NOT EXIST")

        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        price = stock["price"] * shares

        if cash < price:
            return apology("INSUFFICIENT CASH")

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", price, session["user_id"])

        db.execute("INSERT INTO stocks (user_id, symbol, price, shares, operation, date) VALUES (?, ?, ?, ?, ?, ?)",
                   session["user_id"], symbol.upper(), price, shares, "buy", datetime.now())

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    stocks = db.execute("SELECT * FROM stocks WHERE user_id = ?", session["user_id"])
    return render_template("history.html", stocks=stocks)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
        symbol = request.form.get("symbol")
        response = lookup(symbol)
        if not response:
            return apology("INVALID SYMBOL")

        return render_template("quoted.html", response=response)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("USERNAME CAN'T BE EMPTY")

        if db.execute("SELECT * FROM users WHERE username = ?", username):
            return apology("USERNAME ALREADY EXIST")

        if not password:
            return apology("PASSWORD CAN'T BE EMPTY")

        if password != confirmation:
            return apology("PASSWORD DON'T MATCH")

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        stock_shares = db.execute("SELECT SUM(shares) as shares FROM stocks WHERE symbol = ? AND user_id = ?",
                                  symbol, session["user_id"])[0]["shares"]

        if not stock_shares or not stock_shares > 0:
            return apology("YOU DO'T HAVE ANY SHARES OF THAT STOCK")

        if not shares > 0:
            return apology("THE INPUT IS NOT A POSITIVE NUMBER")

        if shares > stock_shares:
            return apology("YOU DON'T OWN THAT MANY SHARES OF THE STOCK")

        price = lookup(symbol)["price"] * shares

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", price, session["user_id"])
        db.execute("INSERT INTO stocks (user_id, symbol, price, shares, operation, date) VALUES (?, ?, ?, ?, ?, ?)",
                   session["user_id"], symbol.upper(), price, -shares, "sell", datetime.now())

        return redirect("/")

    stocks = db.execute("SELECT symbol FROM stocks WHERE user_id = ? GROUP BY symbol HAVING (SUM(shares)) > 0", session["user_id"])

    return render_template("sell.html", stocks=stocks)
