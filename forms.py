from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class DataEntryForm(FlaskForm):
	train_number = StringField("Train Number",
				validators=[DataRequired(message="Enter a valid train number")])
	date = StringField("Date of Arrival",
				validators=[DataRequired()])
	name = StringField('Name',
				validators=[DataRequired(), Length(max=20)])
	phone = StringField("Whatsapp Number",
				validators=[DataRequired(message="It is mandatory to enter the Whatsapp number"),Length(min=10, max=10,message="Enter your 10 digit Whatsapp Number only")])
	roll = StringField('Institute Roll Number',
				validators=[DataRequired(), Length(min=9, max=9,message="Enter valid institute roll number")])
	submit = SubmitField('Check Co-Passengers')		

class LoginForm(FlaskForm):
	rollnumber = StringField("Institute Roll Number",
								validators=[Length(min=9, max=9,message="Enter valid institute roll number")])	
	submit = SubmitField('Check Co-Passengers')

