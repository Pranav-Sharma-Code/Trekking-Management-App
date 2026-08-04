from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.user import User
from models.trek import Trek
from models.booking import Booking

admin = Blueprint("admin", __name__)

def admin_required():
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return False

    if session.get("role") != "Admin":
        flash("Access Denied!", "danger")
        return False

    return True

@admin.route("/admin/dashboard")
def dashboard():
    if not admin_required():
        return redirect(url_for("auth.login"))

    total_treks = Trek.query.count()

    total_users = User.query.filter_by(role="Participant").count()
    total_staff = User.query.filter_by(role="Organizer").count()
    total_bookings = Booking.query.count()

    return render_template(
        "admin/dashboard.html",
        total_treks=total_treks,
        total_users=total_users,
        total_staff=total_staff,
        total_bookings=total_bookings
    )

@admin.route("/admin/treks")
def manage_treks():
    if not admin_required():
        return redirect(url_for("auth.login"))

    treks = Trek.query.all()

    return render_template(
        "admin/manage_trek.html",
        treks=treks
    )

@admin.route("/admin/staff")
def staff_requests():
    if not admin_required():
        return redirect(url_for("auth.login"))

    staff=User.query.filter_by(role="Organizer").all()

    return render_template(
        "admin/approve_staff.html",
        staff=staff
    )

@admin.route("/admin/users")
def users():
    if not admin_required():
        return redirect(url_for("auth.login"))

    users=User.query.filter_by(role="Participant").all()

    return render_template(
        "admin/approve_users.html",
        users=users
    )

@admin.route("/admin/bookings")
def bookings():
    if not admin_required():
        return redirect(url_for("auth.login"))

    bookings = Booking.query.all()

    return render_template(
        "admin/bookings.html",
        bookings=bookings
    )



