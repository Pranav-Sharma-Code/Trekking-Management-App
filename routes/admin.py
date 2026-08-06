from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.user import User
from models.trek import Trek
from datetime import datetime
from models.booking import Booking
from sqlalchemy import or_

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
    approved_staff = User.query.filter_by(role="Trek_staff", approved=True).count()
    pending_Trek_staffs = User.query.filter_by(role="Trek_staff", approved=False).count()
    total_bookings = Booking.query.count()
    recent_treks = Trek.query.order_by(Trek.id.desc() ).limit(5).all()
    recent_bookings = Booking.query.order_by(Booking.id.desc() ).limit(5).all()
    
    return render_template(
        "admin/dashboard.html",
        total_treks=total_treks,
        total_users=total_users,
        approved_staff=approved_staff,
        pending_Trek_staffs=pending_Trek_staffs,
        total_bookings=total_bookings,
        recent_treks=recent_treks,
        recent_bookings=recent_bookings
    )

@admin.route("/admin/treks")
def manage_treks():
    if not admin_required():
        return redirect(url_for("auth.login"))

    search = request.args.get("search", "")

    query = Trek.query

    if search:
        query = query.filter(
            or_(
                Trek.title.ilike(f"%{search}%"),
                Trek.location.ilike(f"%{search}%")
            )
        )
    treks = query.order_by(Trek.id.desc()).all()

    return render_template("admin/manage_trek.html", treks=treks)
    
@admin.route("/admin/staff")
def staff_requests():
    if not admin_required():
        return redirect(url_for("auth.login"))

    staff=User.query.filter_by(role="Trek_staff", approved=True).all()

    return render_template(
        "admin/approve_staff.html",
        staff=staff
    )


@admin.route("/admin/create-trek", methods=["GET", "POST"])
def create_trek():

    if not admin_required():
        return redirect(url_for("auth.login"))

    search = request.args.get("search", "")

    query = User.query.filter_by(role="Trek_staff", approved=True, blacklisted=False)

    if search:
        query = query.filter(User.name.ilike(f"%{search}%"))

    staff = query.all()
    if request.method == "POST":
        trek = Trek(
            title=request.form["title"],
            image=request.form["image"],
            state=request.form["state"],
            location=request.form["location"],
            difficulty=request.form["difficulty"],
            duration=int(request.form["duration"]),
            altitude=int(request.form["altitude"]) if request.form["altitude"] else None,
            registration_deadline=datetime.strptime(request.form["registration_deadline"], "%Y-%m-%d").date(),
            description=request.form["description"],
            start_date=datetime.strptime(request.form["start_date"], "%Y-%m-%d").date(),
            end_date=datetime.strptime(request.form["end_date"], "%Y-%m-%d").date(),
            capacity=int(request.form["capacity"]),
            available_slots=int(request.form["capacity"]),
            price=int(request.form["price"]),
            Trek_staff_id=int(request.form["staff_id"]),
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
    staff = User.query.filter_by(role="Trek_staff", approved=True).all()

    if request.method == "POST":

        trek.title = request.form["title"]
        trek.image = request.form["image"]
        trek.state = request.form["state"]
        trek.location = request.form["location"]
        trek.difficulty = request.form["difficulty"]
        trek.duration = int(request.form["duration"])
        trek.altitude = int(request.form["altitude"]) if request.form["altitude"] else None
        trek.registration_deadline = datetime.strptime(request.form["registration_deadline"], "%Y-%m-%d").date()
        trek.description = request.form["description"]
        trek.start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        trek.end_date = datetime.strptime(request.form["end_date"],"%Y-%m-%d").date()
        trek.capacity = int(request.form["capacity"])
        trek.price = int(request.form["price"])
        trek.Trek_staff_id = int(request.form["staff_id"])
        trek.status = request.form["status"]

        db.session.commit()

        flash("Trek Updated Successfully.", "success")

        return redirect(url_for("admin.manage_treks"))
    return render_template("admin/edit_trek.html", trek=trek, staff=staff)

@admin.route("/admin/delete-trek/<int:trek_id>")
def delete_trek(trek_id):

    if not admin_required():
        return redirect(url_for("auth.login"))

    trek = Trek.query.get_or_404(trek_id)
    db.session.delete(trek)
    db.session.commit()

    flash("Trek Deleted Successfully.", "success")
    return redirect(url_for("admin.manage_treks"))


@admin.route("/admin/approve-staff")
def approve_staff():

    if not admin_required():
        return redirect(url_for("auth.login"))

    pending_staff = User.query.filter_by(
        role="Trek_staff",
        approved=False,
        blacklisted=False
    ).all()

    approved_staff = User.query.filter_by(
        role="Trek_staff",
        approved=True,
        blacklisted=False
    ).all()

    return render_template(
        "admin/approve_staff.html",
        pending_staff=pending_staff,
        approved_staff=approved_staff
    )

@admin.route("/admin/approve/<int:user_id>")
def approve(user_id):
    if not admin_required():
        return redirect(url_for("auth.login"))

    user = User.query.get_or_404(user_id)
    user.approved = True
    db.session.commit()

    flash("Staff Approved Successfully!", "success")
    return redirect(url_for("admin.approve_staff"))

@admin.route("/admin/blacklist/<int:user_id>")
def blacklist(user_id):

    if not admin_required():
        return redirect(url_for("auth.login"))

    user = User.query.get_or_404(user_id)
    user.blacklisted = True
    db.session.commit()

    flash("Staff Blacklisted Successfully!", "warning")
    return redirect(url_for("admin.approve_staff"))

@admin.route("/admin/assign-staff", methods=["GET", "POST"])
def assign_staff():
    if not admin_required():
        return redirect(url_for("auth.login"))

    treks = Trek.query.all()
    staff = User.query.filter_by(role="Trek_staff", approved=True, blacklisted=False).all()

    if request.method == "POST":
        trek = Trek.query.get(request.form["trek_id"])
        trek.Trek_staff_id = request.form["staff_id"]
        db.session.commit()
        flash("Staff Assigned Successfully!", "success")

        return redirect(url_for("admin.assign_staff"))
    return render_template("admin/assign_staff.html", treks=treks, staff=staff)

@admin.route("/admin/manage-users")
def manage_users():

    if not admin_required():
        return redirect(url_for("auth.login"))

    search = request.args.get("search")

    if search:
        users = User.query.filter(
        User.role == "Participant",
        or_(
            User.name.ilike(f"%{search}%"),
            User.email.ilike(f"%{search}%")
        )).all()
    else:
        users = User.query.filter_by(role="Participant").all()

    return render_template("admin/manage_users.html", users=users)

@admin.route("/admin/blacklist-user/<int:user_id>")
def blacklist_user(user_id):

    if not admin_required():
        return redirect(url_for("auth.login"))

    user = User.query.get_or_404(user_id)
    user.blacklisted = True
    db.session.commit()

    flash("User Blacklisted Successfully.", "warning")
    return redirect(url_for("admin.manage_users"))

@admin.route("/admin/bookings")
def bookings():

    if not admin_required():
        return redirect(url_for("auth.login"))

    search = request.args.get("search", "")
    query = Booking.query

    if search:
        query = query.join(User).join(Trek).filter(

            or_(
                User.name.ilike(f"%{search}%"),
                Trek.title.ilike(f"%{search}%")
            )
        )

    bookings = query.order_by(
        Booking.id.desc()
    ).all()

    return render_template("admin/bookings.html", bookings=bookings)