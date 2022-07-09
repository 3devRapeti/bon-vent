from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists
from forms import DataEntryForm, LoginForm

import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Kadapa Rajyam lo Kamma Reddylu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['LOG_TO_STDOUT'] = os.environ.get('LOG_TO_STDOUT')
 
db = SQLAlchemy(app)

basedir = os.path.abspath(os.path.dirname(__file__))

class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    train = db.Column(db.String(5), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    whatsapp = db.Column(db.String(10), nullable=False)
    roll = db.Column(db.String(9), unique=True, nullable=False)
    status = db.Column(db.Boolean)

@app.route("/")
@app.route("/home")
def home():
  return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
  form = DataEntryForm()
  if form.validate_on_submit():
    exists = db.session.query(db.exists().where( form.roll.data.upper() == Passenger.roll)).scalar()
    if not exists:
      p = Passenger (train = form.train_number.data, date = form.date.data, name=form.name.data, whatsapp = form.phone.data, roll=form.roll.data.upper(), status = True)
      db.session.add(p)
      db.session.commit()
      konni = Passenger.query.filter_by(train=form.train_number.data).all()
      return render_template('list.html',tuples = konni, req_date = form.date.data) 
    else:
      flash('Roll Number Already Exists', 'danger')
      return render_template('register.html', form=form)
  return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
  form=LoginForm()
  if form.validate_on_submit():
    exists = db.session.query(db.exists().where(Passenger.roll == form.rollnumber.data.upper())).scalar()
    if exists:  
      vadidhi = Passenger.query.filter_by(roll=form.rollnumber.data.upper()).first()
      konni = Passenger.query.filter_by(train=vadidhi.train).all()
      return render_template('list.html',tuples = konni, req_date = vadidhi.date)
    else:
       flash('Your roll number needs to be registered before you check the list', 'warning')
       return render_template('login.html',form=form)
  return render_template('login.html',form=form)    

@app.route("/list")
def list():
  return render_template('list.html') 

@app.route("/ayyagaru")
def ayyagaru():
  everything = Passenger.query.all()
  return render_template('adminlist.html', tuples = everything)

@app.route("/kosai/<required>", methods=['POST'])
def kosai(required):
  vadidhi = Passenger.query.get(required)
  vadidhi.status = False
  db.session.commit()
  everything = Passenger.query.all()
  return render_template('adminlist.html', tuples = everything)

@app.route("/malli_pettu/<required>", methods=['POST'])
def malli_pettu(required):
  vadidhi = Passenger.query.get(required)
  vadidhi.status = True
  db.session.commit()
  everything = Passenger.query.all()
  return render_template('adminlist.html', tuples = everything)

if __name__=='__main__':
  app.run(debug=True)