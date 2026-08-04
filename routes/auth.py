from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.user import User

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        role = request.form["role"]
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for("auth.register"))
        
        hashed_password = generate_password_hash(password)

        approved = False if role == "Trek_staff" else True
        new_user = User(name=name, 
                        email=email, 
                        password=hashed_password, 
                        phone=phone, 
                        role=role,
                        approved=approved,
                        blacklisted=False
                    )

        db.session.add(new_user)
        db.session.commit()

        if role == "Trek_staff":
            flash(
                "Registration successful! Please wait for Admin approval.",
                "warning"
            )
        else:
            flash(
               "Registration successful! Please login.",
                "success" 
            )


        flash("Registration Successful! Please Login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Invalid Email or Password", "danger")
            return redirect(url_for("auth.login"))

        if not check_password_hash(user.password, password):
            flash("Invalid Email or Password", "danger")
            return redirect(url_for("auth.login"))  

        if user.blacklisted:
            flash("Your account has been blacklisted.", "danger")
            return redirect(url_for("auth.login"))

        if user.role == "Trek_staff" and not user.approved:
            flash("Waiting for Admin Approval.", "warning")
            return redirect(url_for("auth.login"))

        session["user_id"] = user.id
        session["name"] = user.name
        session["role"] = user.role

        flash(f"Welcome {user.name}!", "success")

        if user.role == "Admin":
            return redirect(url_for("admin.dashboard"))

        elif user.role == "Organizer":
            return redirect(url_for("Trek_staff.dashboard"))

        elif user.role == "Participant":
            return redirect(url_for("participant.dashboard"))

        
        flash("Invalid Email or Password", "danger")
        return redirect(url_for("home"))

    return render_template("auth/login.html")

@auth.route("/logout")
def logout():
    session.clear()
    flash("Logged Out Successfully", "success")

    return redirect(url_for("auth.login"))

