from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from sqlalchemy import or_

from models import db
from models.user import User
from models.trek import Trek
from models.booking import Booking

participant = Blueprint("participant", __name__)



def login_required():

    if "user_id" not in session:
        flash("Please login first!", "danger")
        return False

    return True



@participant.route("/participant")
def dashboard():

    if not login_required():
        return redirect(url_for("auth.login"))

    total_treks = Trek.query.filter_by(status="Open").count()
    my_bookings = Booking.query.filter_by(
        user_id=session["user_id"]
    ).count()

    return render_template(
        "participant/dashboard.html",
        total_treks=total_treks,
        my_bookings=my_bookings
    )


@participant.route("/treks")
def browse_treks():

    if not login_required():
        return redirect(url_for("auth.login"))

    search = request.args.get("search", "")
    difficulty = request.args.get("difficulty", "")
    status = request.args.get("status", "")
    query = Trek.query

    if search:
        query = query.filter(
            or_(
                Trek.title.ilike(f"%{search}%"),
                Trek.location.ilike(f"%{search}%")
            )
        )

    if difficulty:
        query = query.filter_by(
            difficulty=difficulty
        )

    if status:
        query = query.filter_by(
            status=status
        )

    treks = query.all()

    return render_template(
        "participant/browse_treks.html",
        treks=treks
    )


@participant.route("/trek/<int:trek_id>")
def trek_details(trek_id):

    if not login_required():
        return redirect(url_for("auth.login"))

    trek = Trek.query.get_or_404(trek_id)

    return render_template(
        "participant/trek_details.html",
        trek=trek
    )


@participant.route("/book/<int:trek_id>")
def book_trek(trek_id):

    if not login_required():
        return redirect(url_for("auth.login"))

    trek = Trek.query.get_or_404(trek_id)

    if trek.status != "Open":
        flash(
            "Booking is closed.",
            "danger"
        )

        return redirect(
            url_for(
                "participant.trek_details",
                trek_id=trek.id
            )
        )

    if trek.available_slots <= 0:
        flash(
            "No Slots Available.",
            "danger"
        )

        return redirect(
            url_for(
                "participant.trek_details",
                trek_id=trek.id
            )
        )

    already_booked = Booking.query.filter_by(
        user_id=session["user_id"],
        trek_id=trek.id
    ).first()

    if already_booked:
        flash(
            "You already booked this trek.",
            "warning"
        )
        return redirect(
            url_for(
                "participant.my_bookings"
            )
        )

    booking = Booking(
        user_id=session["user_id"],
        trek_id=trek.id,
        status="Booked"
    )

    db.session.add(booking)
    trek.available_slots -= 1
    db.session.commit()

    flash(
        "Trek Booked Successfully!",
        "success"
    )

    return redirect(
        url_for("participant.my_bookings")
    )



@participant.route("/my-bookings")
def my_bookings():

    if not login_required():
        return redirect(url_for("auth.login"))

    bookings = Booking.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "participant/my_bookings.html",
        bookings=bookings
    )


@participant.route("/cancel-booking/<int:booking_id>")
def cancel_booking(booking_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != session["user_id"]:
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("participant.my_bookings"))

    if booking.status != "Booked":
        flash("Booking cannot be cancelled.", "warning")
        return redirect(url_for("participant.my_bookings"))

    trek = Trek.query.get(booking.trek_id)
    trek.available_slots += 1
    booking.status = "Cancelled"
    db.session.commit()

    flash("Booking Cancelled Successfully!", "success")
    return redirect(url_for("participant.my_bookings"))

@participant.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    return render_template(
        "participant/profile.html",
        user=user
    )

@participant.route("/profile/update", methods=["POST"])
def update_profile():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    user.name = request.form["name"]
    user.phone = request.form["phone"]

    db.session.commit()

    flash(
        "Profile Updated Successfully.",
        "success"
    )

    return redirect(url_for("participant.profile"))

