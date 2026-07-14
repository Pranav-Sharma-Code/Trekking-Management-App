from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.auth import login_required, organizer_required
from models import db
from models.trek import Trek
from datetime import datetime

organizer = Blueprint("organizer", __name__)

@organizer.route("/organizer")
@login_required
@organizer_required
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Organizer":
        return redirect("/")

    total = Trek.query.filter_by(
        organizer_id=session["user_id"]
    ).count()

    return render_template(
        "organizer/dashboard.html", total_treks=total,
        upcoming=0, participants=0, revenue=0
    )

@organizer.route("/create-trek", methods=["GET", "POST"])
@login_required
@organizer_required
def create_trek():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method=="POST":
        trek=Trek(
            title=request.form["title"],
            location=request.form["location"],
            description=request.form["description"],
            difficulty=request.form["difficulty"],
            start_date=datetime.strptime(request.form["start_date"], "%Y-%m-%d"),
            end_date=datetime.strptime(request.form["end_date"], "%Y-%m-%d"),
            capacity=int(request.form["capacity"]),
            available_slots=int(request.form["capacity"]),
            price=int(request.form["price"]),
            organizer_id=session["user_id"]
        )

        db.session.add(trek)
        db.session.commit()
        flash("Trek Created Successfully","success")
        return redirect(url_for("organizer.my_treks"))

    return render_template("organizer/create_trek.html")

@organizer.route("/my-treks")
@login_required
@organizer_required
def my_treks():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    treks=Trek.query.filter_by(organizer_id=session["user_id"]).all()
    return render_template("organizer/my_treks.html", treks=treks)