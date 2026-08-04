from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db
from models.trek import Trek
from datetime import datetime

Trek_staff = Blueprint("Trek_staff", __name__)

@Trek_staff.route("/Trek_staff")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Trek_staff":
        return redirect("/")

    total = Trek.query.filter_by(
        Trek_staff_id=session["user_id"]
    ).count()

    return render_template(
        "Trek_staff/dashboard.html", total_treks=total,
        upcoming=0, participants=0, revenue=0
    )

@Trek_staff.route("/create-trek", methods=["GET", "POST"])
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
            Trek_staff_id=session["user_id"]
        )

        db.session.add(trek)
        db.session.commit()
        flash("Trek Created Successfully","success")
        return redirect(url_for("Trek_staff.my_treks"))

    return render_template("Trek_staff/create_trek.html")

@Trek_staff.route("/my-treks")
def my_treks():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    treks=Trek.query.filter_by(Trek_staff_id=session["user_id"]).all()
    return render_template("Trek_staff/my_treks.html", treks=treks)

@Trek_staff.route("/delete-trek/<int:id>")
def delete_trek(id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    trek = Trek.query.get_or_404(id)

    if trek.Trek_staff_id != session["user_id"]:
        flash("Unauthorized", "danger")
        return redirect("/my-treks")

    db.session.delete(trek)
    db.session.commit()
    flash("Trek deleted successfully", "success")

    return redirect("/my-treks")

@Trek_staff.route("/edit-trek/<int:id>", methods=["GET", "POST"])
def edit_trek(id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    trek = Trek.query.get_or_404(id)
    if trek.Trek_staff_id != session["user_id"]:
        flash("Unauthorized Access", "danger")
        return redirect("/my-treks")

    if request.method == "POST":
        trek.title = request.form["title"]
        trek.location = request.form["location"]
        trek.description = request.form["description"]
        trek.difficulty = request.form["difficulty"]
        trek.price = int(request.form["price"])
        trek.capacity = int(request.form["capacity"])
        trek.available_slots = int(request.form["capacity"])
        trek.start_date = datetime.strptime(
            request.form["start_date"],
            "%Y-%m-%d"
        ).date()

        trek.end_date = datetime.strptime(
            request.form["end_date"],
            "%Y-%m-%d"
        ).date()
        db.session.commit()
        flash(
            "Trek Updated Successfully",
            "success"
        )
        return redirect("/my-treks")

    return render_template(
        "Trek_staff/edit_trek.html",
        trek=trek
    )