from urllib import response
from flask import Flask, redirect, render_template, request, session
from cs50 import SQL
import json
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

app = Flask(__name__)

app.secret_key = 'argentina'
app.config["SESSION_TYPE"] = "filesystem"


db = SQL("sqlite:///app.db")

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return render_template("login.html", errorL="Input must not be empty")

        rows = db.execute("SELECT * FROM users WHERE email = ?", email)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template("login.html", errorL="Invalid email and/or password")

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    email = request.form.get("email")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if not firstName or not lastName or not email or not password or not confirmation:
        return render_template("login.html", errorR="Input must not be empty")

    if password != confirmation:
        return render_template("login.html", errorR="Passwords do not match")

    user_id = db.execute("INSERT INTO users (first_name, last_name, email, hash) VALUES(?, ?, ?, ?)",
    firstName, lastName, email, generate_password_hash(password))

    session["user_id"] = user_id

    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# APIs

@app.route("/card", methods=["GET", "POST", "PATCH", "DELETE"])
@login_required
def card():
    card_name = request.form.get("card_name")
    link = request.form.get("link")
    section_id = request.form.get("section_id")
    link_id = request.form.get("card_id")

    if request.method == "POST":
        if not card_name or not link or not section_id:
            return {'error': 'Data missing'}

        db.execute("INSERT INTO links (name, link, section_id) VALUES(?, ?, ?)",
        card_name, link, section_id)
        return {'msg': 'created'}

    if request.method == "DELETE":
        if not link_id:
            return {'error': 'Data missing'}

        owner = db.execute("SELECT user_id FROM sections WHERE id = ?", section_id)[0]['user_id']
        if owner == session["user_id"]:
            db.execute("DELETE FROM links WHERE id = ?", link_id)
            return {'deleted': link_id}
        return {'error': 'You are not the owner of this link'}

    section_id = request.args.get('id')
    links = db.execute("SELECT * FROM links WHERE section_id = ?", section_id)
    section = db.execute("SELECT * FROM sections WHERE id = ?", section_id)[0]
    response = {
        'emoji': section['emoji'],
        'name': section['name'],
        'links': links
    }
    response = json.dumps(response)
    return response


@app.route("/section", methods=["GET", "POST", "DELETE"])
@login_required
def section():
    emoji = request.form.get("emoji")
    section_name = request.form.get("section_name")
    section_id = request.form.get("section_id")

    if request.method == "POST":
        if not emoji or not section_name:
            return {'error': 'Data missing'}

        db.execute("INSERT INTO sections (emoji, name, user_id) VALUES(?, ?, ?)",
        emoji, section_name, session["user_id"])

    if request.method == "DELETE":
        if not section_id:
            return {'error': 'Data missing'}

        deltedSectionId = db.execute("SELECT id FROM sections WHERE id = ? AND user_id = ?", section_id, session["user_id"])[0]['id']
        db.execute("DELETE FROM links WHERE section_id = ?", deltedSectionId)
        db.execute("DELETE FROM sections WHERE id = ? AND user_id = ?", deltedSectionId, session["user_id"])

    sections = db.execute("SELECT * FROM sections WHERE user_id = ?", session["user_id"])
    return json.dumps(sections)
