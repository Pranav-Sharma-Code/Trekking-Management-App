from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
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

@admin.route("/admin")
def dashboard():
    if not admin_required():
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("auth.login"))

    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role="Participant").count()
    total_staff = User.query.filter_by(role="Organizer").count()
    pending_organizers = User.query.filter_by(role="Organizer", approved=False).count()
    total_bookings = Booking.query.count()

    return render_template(
        "admin/dashboard.html",

        total_treks=total_treks,
        total_users=total_users,
        total_staff=total_staff,
        total_organizers=total_organizers,
        pending_organizers=pending_organizers,
        total_bookings=total_bookings,
        recent_treks=recent_treks,
        recent_bookings=recent_bookings
    )

@admin.route("/admin/treks")
def manage_treks():
    if not admin_required():
        return redirect(url_for("auth.login"))

    treks = Trek.query.order_by(Trek.id.desc()).all()

    return render_template(
        "admin/manage_trek.html",
        treks=treks
    )

@admin.route("/admin/staff")
def staff_requests():
    if not admin_required():
        return redirect(url_for("auth.login"))

    staff=User.query.filter_by(role="staff").all()

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

    bookings = Booking.query.order_by(Booking.id.desc()).all()

    return render_template(
        "admin/bookings.html",
        bookings=bookings
    )

@admin.route("/admin/create-trek", methods=["GET", "POST"])
def create_trek():

    if not admin_required():
        return redirect(url_for("auth.login"))

    staff = User.query.filter_by(role="Organizer", approved=True).all()

    if request.method == "POST":

        trek = Trek(
            title=request.form["title"],
            state=request.form["state"],
            location=request.form["location"],
            difficulty=request.form["difficulty"],
            duration=request.form["duration"],
            altitude=request.form["altitude"],
            registration_deadline=request.form["registration_deadline"],
            description=request.form["description"],
            start_date=request.form["start_date"],
            end_date=request.form["end_date"],
            capacity=request.form["capacity"],
            available_slots=request.form["capacity"],
            price=request.form["price"],
            organizer_id=request.form["organizer_id"],
            status=request.form["status"]
        )

        db.session.add(trek)
        db.session.commit()

        flash(
            "Trek Created Successfully!",
            "success"
        )
        return redirect(url_for("admin.manage_treks"))

    return render_template(
        "admin/create_trek.html",
        staff=staff
    )


@admin.route("/admin/edit-trek/<int:trek_id>", methods=["GET","POST"])
def edit_trek(trek_id):

    if not admin_required():
        return redirect(url_for("auth.login"))

    trek = Trek.query.get_or_404(trek_id)
    staff = User.query.filter_by(role="Organizer", approved=True).all()

    if request.method == "POST":

        trek.title=request.form["title"]
        trek.state=request.form["state"]
        trek.location=request.form["location"]
        trek.difficulty=request.form["difficulty"]
        trek.duration=request.form["duration"]
        trek.altitude=request.form["altitude"]
        trek.registration_deadline=request.form["registration_deadline"]
        trek.description=request.form["description"]
        trek.start_date=request.form["start_date"]
        trek.end_date=request.form["end_date"]
        trek.capacity=request.form["capacity"]
        trek.price=request.form["price"]
        trek.organizer_id=request.form["organizer_id"]
        trek.status=request.form["status"]

        db.session.commit()

        flash("Trek Updated Successfully.", "success")

        return redirect(url_for("admin.manage_treks"))

    return render_template(
        "admin/edit_trek.html",
        trek=trek, staff=staff
    )

@admin.route("/admin/delete-trek/<int:trek_id>")
def delete_trek(trek_id):

    if not admin_required():
        return redirect(url_for("auth.login"))

    trek = Trek.query.get_or_404(trek_id)

    db.session.delete(trek)
    db.session.commit()

    flash("Trek Deleted Successfully.", "success")
    return redirect(url_for("admin.manage_treks"))


