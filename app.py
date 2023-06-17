from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'supersecretkey'

db = SQLAlchemy(app)
ma = Marshmallow(app)


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


class TransactionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'value', 'trans_type', 'trans_cat')


transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
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

    transactions = [trans.to_dict() for trans in Transaction.query.all()]
    return render_template('index.html', transactions=transactions)


@app.route('/transactions', methods=['POST', 'GET'])
def show_transactions():
    transactions = [trans.to_dict() for trans in Transaction.query.all()]
    return render_template('database.html', transactions=transactions)


@app.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    form = Form(obj=transaction)

    if request.method == 'POST' and form.validate_on_submit():
        transaction.value = form.value.data
        transaction.trans_type = form.trans_type.data
        transaction.trans_cat = form.trans_cat.data
        db.session.commit()
        return redirect(url_for('show_transactions'))

    return render_template('edit.html', form=form, transaction=transaction)


@app.route('/delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('show_transactions'))


@app.route('/filter', methods=['POST', 'GET'])
def filter_transactions():
    form = Form()  # Create an instance of the Form
    transactions = []

    if request.method == 'POST' and form.validate_on_submit():
        trans_type = form.trans_type.data
        trans_cat = form.trans_cat.data
        transactions = Transaction.query.filter_by(trans_type=trans_type, trans_cat=trans_cat).all()

    return render_template('filter.html', form=form, transactions=transactions)


@app.route('/transaction/<int:transaction_id>')
def view_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    return render_template('transaction.html', transaction=transaction)


@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    result = transactions_schema.dump(transactions)
    return jsonify(result)


@app.route('/about')
def about():
    form = Form()
    return render_template('about.html', form=form)

with app.app_context():
    db.create_all()
    app.run()