from flask import Flask, render_template, redirect, url_for
from app.models import db, Patient
from app.forms import PatientForm
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
csrf = CSRFProtect(app)
migrate = Migrate(app, db)

# Initialize the database with the Flask app instance
db.init_app(app)


@app.route('/')
def index():
        # Create the database tables if they don't already exist
    db.create_all()

    # Add a new patient to the database
    #patient = Patient(name='John Doe', age=35, gender='male',
    #              address='123 Main St., Anytown, USA',
    #              phone='555-555-5555')
    #db.session.add(patient)
    #db.session.commit()


    # Query the database for all users
    patients = Patient.query.all()

    # Return a list of user names as a response
    return render_template('layout.html', patients=patients)
    #', '.join([user.name for user in users])

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    patient_form = PatientForm()
    if patient_form.validate_on_submit():
        # Add the new patient to the database
        # Create a new Patient object
        patient = Patient(name=patient_form.name.data,
                          age=patient_form.age.data,
                          gender=patient_form.gender.data,
                          address=patient_form.address.data,
                          phone=patient_form.phone.data)
        # Save the patient to the database
        db.session.add(patient)
        db.session.commit()
        # and redirect to the patient list page
        return redirect(url_for('patient_list'))
    return render_template('add_patient.html', patient_form=patient_form)

@app.route('/patient_list')
def patient_list():
    # Query the database for all patients
    patients = Patient.query.all()
    # Render the patient list template
    return render_template('patient_list.html', patients=patients)

if __name__ == '__main__':
    app.run(debug=True)
