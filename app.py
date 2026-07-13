from flask import Flask, render_template

from routes.auth import auth

from models import db
from models.user import User
from models.trek import Trek
from models.booking import Booking

app = Flask(__name__)

app.secret_key = "code_IIT_prnv"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(auth)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)