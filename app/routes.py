from flask import Blueprint, render_template, url_for, flash, redirect, request, session
from werkzeug.security import generate_password_hash
from app import db, bcrypt
from flask_bcrypt import Bcrypt
from app.models import User
from app.forms import MedicalDiagnosisRegistrationForm, LoginForm
from app.diagnosis_helper import get_predicted_value, helper, symptoms_dict

main = Blueprint('main', __name__)

# Home Page
@main.route("/")
def home():
    return render_template('home.html')

# About Page
@main.route("/about")
def about():
    return render_template('about.html', title='About')

bcrypt = Bcrypt()

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = MedicalDiagnosisRegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        age = form.age.data
        gender = form.gender.data
        medical_condition = form.medical_condition.data
        password = form.password.data

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("User already exists. Please log in instead.", "danger")
            return redirect(url_for('main.login'))

        # Hash the password correctly
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user
        new_user = User(
            username=username,
            email=email,
            age=age,
            gender=gender,
            medical_condition=medical_condition,
            password=hashed_password
        )

        # Save the user to the database
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('main.login'))  # Redirect to login page

    return render_template('register.html', form=form)  # Render form if validation fails


# Login Page
@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            try:
                # Check if the stored password hash is valid
                if bcrypt.check_password_hash(user.password, form.password.data):
                    session["user_id"] = user.id
                    session["username"] = user.username
                    session["email"] = user.email
                    flash('You have been logged in!', 'success')
                    return redirect(url_for('main.Prediction'))
                else:
                    flash('Invalid email or password. Please try again.', 'danger')
            except ValueError as e:
                flash("Password hash is invalid. Try resetting your password.", "danger")
                print(f"Error: {e}")  # Logs the error in the console
        else:
            flash('User does not exist. Please register first.', 'danger')

    return render_template('login.html', title='Login', form=form)


# Dashboard - Shows user details and allows symptom input
@main.route("/Prediction", methods=['GET', 'POST'])
def Prediction():
    if "user_id" not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for("main.login"))

    user = User.query.get(session.get("user_id"))

    predicted_disease = None
    disease_description = None
    precautions = []
    medications = []
    workout = []
    diet = []
    message = None

    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        print("User entered symptoms:", symptoms)

        if not symptoms or symptoms.strip().lower() == "symptoms":
            message = "Please either write symptoms or you have written misspelled symptoms."
        else:
            try:
                # Split and clean the input symptoms
                user_symptoms = [s.strip("[]' ").lower() for s in symptoms.split(',')]

                # Log unrecognized symptoms
                unrecognized_symptoms = [sym for sym in user_symptoms if sym not in symptoms_dict]
                if unrecognized_symptoms:
                    print(f"Warning: Unrecognized symptoms - {unrecognized_symptoms}")

                # Predict disease and get relevant details
                predicted_disease = get_predicted_value(user_symptoms)
                disease_description, precautions, medications, diet, workout = helper(predicted_disease)

                # Handle cases where no data is returned
                precautions = precautions[0] if precautions else []
                medications = medications if medications else []
                diet = diet if diet else []
                workout = workout if workout else []

            except Exception as e:
                print(f"🔥 Full Error Traceback: {str(e)}")  # Debugging print statement
                message = f"Error: {str(e)}"

    return render_template("Prediction.html", 
                           user=user, 
                           predicted_disease=predicted_disease, 
                           disease_description=disease_description,
                           precautions=precautions, 
                           medications=medications, 
                           diet=diet,
                           workout=workout,
                           message=message)

# Logout
@main.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))

# Users List
@main.route("/users")
def users():
    users = User.query.all()
    return render_template('users.html', users=users)
