from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime

from models import db
from models.trek import Trek
from models.booking import Booking

Trek_staff = Blueprint("Trek_staff", __name__)


def staff_required():

    if "user_id" not in session:
        flash("Please Login First!", "danger")
        return False

    if session.get("role") != "Trek_staff":
        flash("Access Denied!", "danger")
        return False

    return True


@Trek_staff.route("/Trek_staff")
def dashboard():

    if not staff_required():
        return redirect(url_for("auth.login"))

    treks = Trek.query.filter_by(Trek_staff_id=session["user_id"]).all()
    total_treks = len(treks)
    open_treks = Trek.query.filter_by(Trek_staff_id=session["user_id"], status="Open").count()
    completed_treks = Trek.query.filter_by(Trek_staff_id=session["user_id"], status="Completed").count()
    total_participants = 0

    for trek in treks:
        total_participants += Booking.query.filter_by(trek_id=trek.id, status="Booked").count()

    return render_template(
        "Trek_staff/dashboard.html",
        treks=treks,
        total_treks=total_treks,
        open_treks=open_treks,
        completed_treks=completed_treks,
        total_participants=total_participants
    )


@Trek_staff.route("/my-treks")
def my_treks():

    if not staff_required():
        return redirect(url_for("auth.login"))

    treks = Trek.query.filter_by(Trek_staff_id=session["user_id"]).all()

    return render_template("Trek_staff/my_treks.html", mtreks=treks)


@Trek_staff.route("/participants/<int:trek_id>")
def participants(trek_id):

    if not staff_required():
        return redirect(url_for("auth.login"))

    trek = Trek.query.get_or_404(trek_id)

    if trek.Trek_staff_id != session["user_id"]:
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("Trek_staff.my_treks"))

    bookings = Booking.query.filter_by(trek_id=trek.id).all()

    return render_template("Trek_staff/participants.html", trek=trek, bookings=bookings)


@Trek_staff.route("/edit-trek/<int:id>", methods=["GET", "POST"])
def edit_trek(id):

    if not staff_required():
        return redirect(url_for("auth.login"))

    trek = Trek.query.get_or_404(id)

    if trek.Trek_staff_id != session["user_id"]:
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("Trek_staff.my_treks"))

    if request.method == "POST":

        trek.title = request.form["title"]
        trek.image = request.form["image"]
        trek.state = request.form["state"]
        trek.location = request.form["location"]
        trek.description = request.form["description"]
        trek.difficulty = request.form["difficulty"]
        trek.duration = int(request.form["duration"])
        trek.altitude = int(request.form["altitude"]) if request.form["altitude"] else None
        trek.registration_deadline = datetime.strptime(request.form["registration_deadline"], "%Y-%m-%d").date()
        trek.start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        trek.end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()
        trek.capacity = int(request.form["capacity"])
        trek.available_slots = int(request.form["capacity"])
        trek.price = int(request.form["price"])
        trek.status = request.form["status"]

        db.session.commit()
        flash("Trek Updated Successfully!", "success")

        return redirect(url_for("Trek_staff.my_treks"))

    return render_template(
        "Trek_staff/edit_trek.html",
        trek=trek
    )


@Trek_staff.route("/delete-trek/<int:id>")
def delete_trek(id):

    if not staff_required():
        return redirect(url_for("auth.login"))

    trek = Trek.query.get_or_404(id)

    if trek.Trek_staff_id != session["user_id"]:
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("Trek_staff.my_treks"))

    db.session.delete(trek)
    db.session.commit()

    flash("Trek Deleted Successfully!", "success")

    return redirect(url_for("Trek_staff.my_treks"))