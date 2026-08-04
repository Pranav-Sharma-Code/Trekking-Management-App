from flask import (Blueprint, render_template, request, redirect,
    url_for, flash, session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models import db
from models.user import User

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        phone = request.form["phone"].strip()
        password = request.form["password"]
        role = request.form["role"]
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for("auth.register"))
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, phone=phone,
            password=hashed_password, role=role
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful! Please Login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")



@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            session["user_id"] = user.id
            session["name"] = user.name
            session["role"] = user.role

            flash(f"Welcome {user.name}!", "success")

            if user.role == "Organizer":
                return redirect(url_for("organizer.dashboard"))

            elif user.role == "Participant":
                return redirect(url_for("participant.dashboard"))

            elif user.role == "Admin":
                return redirect(url_for("admin.dashboard"))

            return redirect(url_for("home"))

        flash("Invalid Email or Password!", "danger")

    return render_template("auth/login.html")



@auth.route("/logout")
def logout():

    session.clear()

    flash("Logged Out Successfully.", "success")

    return redirect(url_for("auth.login"))