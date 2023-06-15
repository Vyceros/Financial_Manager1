from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    trans_type = db.Column(db.String(10), nullable=False)
    trans_cat = db.Column(db.String(50), nullable=False)

    # def __repr__(self):
    #     return f"Transaction(id={self.id}, value={self.value}, type={self.trans_type}, category={self.trans_cat})"

    def to_dict(self):
        return {
            "id": self.id,
            "value": self.value,
            "trans_type": self.trans_type,
            "trans_cat": self.trans_cat
        }
