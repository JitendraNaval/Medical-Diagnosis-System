from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from form import MedicalDiagnosisRegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medical_diagnosis.db'  # Database file
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Database Model for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    medical_condition = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.age}', '{self.gender}')"

# Home Page
@app.route("/")
def home():
    return render_template('home.html')

# About Page
@app.route("/about")
def about():
    return render_template('about.html', title='About')

# Register Page
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = MedicalDiagnosisRegistrationForm()
    if form.validate_on_submit():
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # Create user object
        user = User(username=form.username.data, email=form.email.data, age=form.age.data,
                    gender=form.gender.data, medical_condition=form.medical_condition.data, password=hashed_password)
        
        # Save to database
        db.session.add(user)
        db.session.commit()

        flash(f'Account created successfully for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

# Login Page
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates database tables if they don't exist
    app.run(debug=True)
