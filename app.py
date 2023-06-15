from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
import models

app = Flask(__name__)
data_transaction = models.Transaction

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'supersecretkey'

db = SQLAlchemy(app)
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
    new_transaction = models.Transaction(value=value, trans_type=trans_type, trans_cat=trans_cat)
    db.session.add(new_transaction)
    db.session.commit()
    transactions = data_transaction.query.all()

    return render_template('database.html', transactions=transactions)


with app.app_context():
    db.create_all()
    app.run()
