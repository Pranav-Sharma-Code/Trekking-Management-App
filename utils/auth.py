from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first", "warning")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper


def organizer_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("role") != "Organizer":
            flash("Access Denied", "danger")
            return redirect(url_for("home"))
        return func(*args, **kwargs)
    return wrapper