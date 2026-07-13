from flask import Flask

from models import db
from models.user import User
from models.trek import Trek
from models.booking import Booking

app = Flask(__name__)

app.secret_key = "code_IIT_prnv"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "<h1>🏔 Trekking Management System</h1>"

if __name__ == "__main__":
    app.run(debug=True)