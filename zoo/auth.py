import email
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Message
from . import db, bcrypt, mail
from . import model
import flask_login
from random import choice
from string import ascii_letters

bp = Blueprint("auth", __name__)

def create_user_code() -> str:
    string = ""

    for _ in range(0, model.DEFAULT_CODE_SIZE):
        string += choice(ascii_letters)

    return string;

def send_email_to_verify_code(user: model.User):
    message = Message("Please verify your email", recipients=[user.email])
    message.body = f"Please verify your email clicking this link\nLink:\n{url_for('auth.verify_user', code=user.code, _external=True)}"
    mail.send(message)

@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("fragments/modal_signup.html")

    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")
    last_name = request.form.get("last_name")
    
    # Check that passwords are equal
    if password != request.form.get("password_repeat"):
        return "error", 405
    
    # Check if the email is already at the database
    user = model.User.query.filter_by(email=email).first()
    if user:
        return "error", 406

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = model.User(email=email, name=name, last_name=last_name, password_hash=password_hash, code=create_user_code())
    db.session.add(new_user)
    db.session.commit()

    send_email_to_verify_code(new_user)
    
    return "success", 200

@bp.route("/verify_user/<string:code>")
def verify_user(code):
    user = model.User.query.filter_by(code=code).first()
    if user:
        user.code = None
        db.session.commit()
        return render_template("pages/verify_user.html")
    
    return render_template("pages/error.html")

@bp.route("/login")
def login():
    return render_template("fragments/modal_login.html")

@bp.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = model.User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password_hash, password) and not user.code:
        flask_login.login_user(user)

        return "success", 200

    return "error", 400

@bp.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect(url_for("main.index"))
