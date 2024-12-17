from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Email(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(120), unique = True, nullable = False)

    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
        }


class Payment(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    amount = db.Column(db.Float, nullable = False)
    stripe_id = db.Column(db.String(120), nullable = False)
    time_of_transaction = db.Column(db.DateTime, default = db.func.now())

    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "amount":self.amount,
            "stripeId":self.stripe_id,
            "timeOfTransaction":self.time_of_transaction,
        }


