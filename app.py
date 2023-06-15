from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'supersecretkey'

db = SQLAlchemy(app)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    trans_type = db.Column(db.String(10), nullable=False)
    trans_cat = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "value": self.value,
            "trans_type": self.trans_type,
            "trans_cat": self.trans_cat
        }


app.debug = True


class Form(FlaskForm):
    value = StringField('name', validators=[validators.DataRequired()])
    trans_type = StringField('description', validators=[validators.DataRequired()])
    trans_cat = StringField('author', validators=[validators.DataRequired()])


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/main', methods=['POST', 'GET'])
def main():
    form = Form()
    return render_template('main.html', form=form)


@app.route('/result', methods=['POST', 'GET'])
def insert_transaction():
    value = request.form.get('value')
    trans_type = request.form.get('type')
    trans_cat = request.form.get('category')
    new_transaction = Transaction(value=value, trans_type=trans_type, trans_cat=trans_cat)
    db.session.add(new_transaction)
    db.session.commit()

    transactions = [transi.to_dict() for transi in Transaction.query.all()]
    return render_template('index.html', transactions=transactions)


@app.route('/transactions', methods=['POST', 'GET'])
def show_transactions():
    transactions = [trans.to_dict() for trans in Transaction.query.all()]
    return render_template('database.html', transactions=transactions)


with app.app_context():
    db.create_all()
    app.run()
