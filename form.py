from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Length,EqualTo,Email


class MedicalDiagnosisRegistrationForm(FlaskForm):
    username=StringField(
        'Full Name',validators=[DataRequired(),Length(min=2,max=20)])
    
    email=StringField('Email',validators=[DataRequired(), Email()])

    age=IntegerField('Age',validators=[DataRequired()])

    gender=SelectField('Gender',choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],validators=[DataRequired()])

    medical_condition=TextAreaField('Describe Your Medical Condition',validators=[DataRequired(),Length(min=5)])

    password=PasswordField('Password',validators=[DataRequired()])

    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])

    submit=SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(), Email()])

    password=PasswordField('Password',validators=[DataRequired()])
        
    remember=BooleanField('Remember Me')

    submit=SubmitField('Login')

    