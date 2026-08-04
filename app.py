from flask import Flask, render_template
from routes.participant import participant
from flask_migrate import Migrate
from routes.auth import auth
from routes.Trek_staff import organizer
from models import db
from werkzeug.security import generate_password_hash
from models.user import User
from models.trek import Trek
from models.booking import Booking
from routes.admin import admin

app = Flask(__name__)
app.secret_key = "code_IIT_prnv"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth)
app.register_blueprint(participant)
app.register_blueprint(organizer)
app.register_blueprint(admin)

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(email="admin@trek.com").first()

    if not admin:

        admin = User(
            name="Admin",
            email="admin@trek.com",
            phone="9999999999",
            password=generate_password_hash("admin123"),
            role="Admin",
            approved=True,
            blacklisted=False
        )

        db.session.add(admin)
        db.session.commit()


@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)