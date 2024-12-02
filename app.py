import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads/xray_documents'  # Folder to store uploaded X-ray files
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for flash messages
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit for uploads

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'W7301@jqir#'
app.config['MYSQL_DB'] = 'healthcare_management'

mysql = MySQL(app)

def create_app():
    return app
from app import create_app, mysql  # Import the app and mysql from app.py

app = create_app()  # Initialize the app



def get_db_connection():
    try:
        # Use the global MySQL instance created with flask_mysqldb
        connection = mysql.connection
        if connection:
            return connection
    except Exception as e:
        print(f"Error: {e}")
        return None

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'W7301@jqir#'
app.config['MYSQL_DB'] = 'healthcare_management'

mysql = MySQL(app)
@app.route('/patient/details/<int:patient_id>', methods=['GET'])
def patient_details(patient_id):
    # Fetch patient data
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM patients WHERE id = %s', (patient_id,))
    patient = cursor.fetchone()
    
    # Fetch visit dates for calendar
    cursor.execute('SELECT visit_date FROM patient_visits WHERE patient_id = %s', (patient_id,))
    visit_dates = [visit['visit_date'].strftime('%Y-%m-%d') for visit in cursor.fetchall()]
    
    cursor.close()
    
    return render_template('patient_details.html', patient=patient, visit_dates=visit_dates)
@app.route('/patient/contact_details/<int:patient_id>', methods=['GET'])


@app.route('/patient/contact_details/<int:patient_id>', methods=['GET'])
def contact_details(patient_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT phone_number, contact_details FROM patients WHERE id = %s', (patient_id,))
    contact_details = cursor.fetchone()
    cursor.close()

    if contact_details:
        
        details_split = contact_details['contact_details'].split(", ")
        email = details_split[0] if len(details_split) > 0 else "Not Available"
        emergency_contact = details_split[1] if len(details_split) > 1 else "Not Available"
        contact_details['email'] = email
        contact_details['emergency_contact'] = emergency_contact

        return render_template('contact_details.html', contact_details=contact_details)
    else:
        flash('Contact details not found!', 'error')
        return redirect(url_for('patient_dashboard'))

@app.route('/patient/doctors_visited/<int:patient_id>', methods=['GET'])
def doctors_visited(patient_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT doctors_visited FROM patients WHERE id = %s', (patient_id,))
    doctors_visited = cursor.fetchone()
    cursor.close()
    
    return render_template('doctors_visited.html', doctors_visited=doctors_visited)

@app.route('/patient/prescriptions/<int:patient_id>', methods=['GET'])
def prescriptions(patient_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT prescriptions FROM patients WHERE id = %s', (patient_id,))
    prescriptions = cursor.fetchone()
    cursor.close()
    
    return render_template('prescriptions.html', prescriptions=prescriptions)

@app.route('/patient/xray_scans/<int:patient_id>', methods=['GET'])
def xray_scans(patient_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT xray_scans FROM patients WHERE id = %s', (patient_id,))
    xray_scans = cursor.fetchone()
    cursor.close()
    
    return render_template('xray_scans.html', xray_scans=xray_scans)

@app.route('/patient/mri_scans/<int:patient_id>', methods=['GET'])
def mri_scans(patient_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT mri_scans FROM patients WHERE id = %s', (patient_id,))
    mri_scans = cursor.fetchone()
    cursor.close()
    
    return render_template('mri_scans.html', mri_scans=mri_scans)

@app.route('/patient/reports/<int:patient_id>', methods=['GET'])
def reports(patient_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT reports FROM patients WHERE id = %s', (patient_id,))
    reports = cursor.fetchone()
    cursor.close()
    
    return render_template('reports.html', reports=reports)

@app.route('/patient/medical_bills/<int:patient_id>', methods=['GET'])
def medical_bills(patient_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT medical_bills FROM patients WHERE id = %s', (patient_id,))
    medical_bills = cursor.fetchone()
    cursor.close()
    
    return render_template('medical_bills.html', medical_bills=medical_bills)

@app.route('/patient/appointments/<int:patient_id>', methods=['GET'])
def appointments(patient_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT appointments FROM patients WHERE id = %s', (patient_id,))
    appointments = cursor.fetchone()
    cursor.close()
    
    return render_template('appointments.html', appointments=appointments)

# @app.route('/patient/other_documents/<int:patient_id>', methods=['GET'])
# def other_documents(patient_id):
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute('SELECT other_documents FROM patients WHERE id = %s', (patient_id,))
#     other_documents = cursor.fetchone()
#     cursor.close()
    
#     return render_template('other_documents.html', other_documents=other_documents)
@app.route('/other_documents/<int:patient_id>', methods=['GET'])
def other_documents(patient_id):
    # Use DictCursor to fetch results as a dictionary
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Query to fetch other documents for the patient
    cursor.execute("SELECT other_documents FROM patients WHERE id = %s", (patient_id,))
    result = cursor.fetchone()  # Fetch a single row
    cursor.close()

    # Extract the 'other_documents' field or handle if no result is found
    other_documents = result['other_documents'] if result else "No documents available."

    # Render the template with the patient ID and document data
    return render_template('other_documents.html', other_documents=other_documents, patient_id=patient_id)

@app.route('/')
def select_role():
    return render_template('select_role.html')


@app.route('/patient', methods=['GET', 'POST'])
def patient_page():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        password = request.form['password']
        
        # Use a dictionary cursor
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            # Validate user credentials
            cursor.execute("SELECT * FROM patients WHERE phone_number = %s AND password = %s", 
                           (phone_number, password))
            patient = cursor.fetchone()
            if patient:
                # Redirect to patient details page with patient data
                return render_template('patient_details_forpt.html', patient=patient)
            else:
                flash('Invalid phone number or password. Please try again.', 'error')
        finally:
            cursor.close()
    
    return render_template('patient_login.html')

@app.route('/doctor', methods=['GET', 'POST'])
def doctor_page():
    if request.method == 'POST':
        unique_id = request.form['unique_id']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM patients WHERE unique_id = %s AND password = %s', (unique_id, password))
        patient = cursor.fetchone()
        
        if patient:
            # Retrieve patient visit dates for calendar
            cursor.execute('SELECT visit_date FROM patient_visits WHERE patient_id = %s', (patient['id'],))
            visit_dates = [visit['visit_date'].strftime('%Y-%m-%d') for visit in cursor.fetchall()]
            
            # Close cursor after fetching all data
            cursor.close()
            
            # Pass visit dates to template
            return render_template('patient_details.html', patient=patient, visit_dates=visit_dates)
        else:
            flash('Invalid unique ID or password.', 'error')
            cursor.close()

    return render_template('doctor_login.html')
@app.route('/patient/signup', methods=['GET', 'POST'])
def patient_signup():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        unique_id = request.form['unique_id']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        try:
            # Insert new patient data into the database
            cursor.execute('INSERT INTO patients (name, phone_number, unique_id, password) VALUES (%s, %s, %s, %s)', 
                           (name, phone_number, unique_id, password))
            mysql.connection.commit()
            flash('Account created successfully!', 'success')
            return redirect('/patient')
        except Exception as e:
            flash('Error: Could not create account. Please try again.', 'error')
        finally:
            cursor.close()
    
    return render_template('patient_signup.html')

@app.route('/patient/update_details/<int:patient_id>', methods=['GET', 'POST'])
def update_details(patient_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        # Get form data
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        
        # Update the database
        cursor.execute("""
            UPDATE patients
            SET phone_number = %s, contact_details = %s
            WHERE id = %s
        """, (phone_number, email, patient_id))
        mysql.connection.commit()
        cursor.close()
        
        flash("Details updated successfully!", "success")
        return redirect(url_for('contact_details', patient_id=patient_id))
    
    # For GET requests, fetch the current patient details
    cursor.execute('SELECT * FROM patients WHERE id = %s', (patient_id,))
    patient = cursor.fetchone()
    cursor.close()
    
    return render_template('update_details.html', patient=patient)
@app.route('/update_doctors_visited/<int:patient_id>', methods=['GET', 'POST'])
def update_doctors_visited(patient_id):
    # Use the global MySQL connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch patient data
    cursor.execute('SELECT * FROM patients WHERE id = %s', (patient_id,))
    patient = cursor.fetchone()

    if not patient:
        cursor.close()
        return "Patient not found", 404

    if request.method == 'POST':
        doctors_visited = request.form['doctors_visited']
        cursor.execute(
            'UPDATE patients SET doctors_visited = %s WHERE id = %s',
            (doctors_visited, patient_id)
        )
        mysql.connection.commit()
        cursor.close()
        flash("Doctors visited updated successfully!", "success")
        return redirect(url_for('doctors_visited', patient_id=patient_id))

    cursor.close()
    return render_template('update_doctors_visited.html', patient=patient)
@app.route('/update_prescriptions/<int:patient_id>', methods=['GET', 'POST'])
def update_prescriptions(patient_id):
    # Use the global MySQL connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch patient data
    cursor.execute('SELECT * FROM patients WHERE id = %s', (patient_id,))
    patient = cursor.fetchone()

    if not patient:
        cursor.close()
        return "Patient not found", 404

    if request.method == 'POST':
        # Get updated prescriptions from the form
        prescriptions = request.form['prescriptions']
        
        # Update prescriptions in the database
        cursor.execute(
            'UPDATE patients SET prescriptions = %s WHERE id = %s',
            (prescriptions, patient_id)
        )
        mysql.connection.commit()
        cursor.close()
        flash("Prescriptions updated successfully!", "success")
        return redirect(url_for('prescriptions', patient_id=patient_id))

    cursor.close()
    return render_template('update_prescriptions.html', patient=patient)
# Example route for uploading x-ray
@app.route('/patient/upload_xray/<int:patient_id>', methods=['GET', 'POST'])
def upload_xray(patient_id):
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'xray_file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)

        file = request.files['xray_file']
        
        # If the user does not select a file, the browser might submit an empty part without a filename
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        # If file is valid, save it
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Save the file to the specified folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Now store the file path in the database for the patient
            cursor = mysql.connection.cursor()
            try:
                cursor.execute(
                    "UPDATE patients SET xray_scans = %s WHERE id = %s", 
                    (file_path, patient_id)
                )
                mysql.connection.commit()
                flash('X-ray uploaded successfully!', 'success')
            except Exception as e:
                flash(f'Error: {e}', 'error')
            finally:
                cursor.close()

            return redirect(url_for('patient_details', patient_id=patient_id))

    return render_template('upload_xray.html', patient_id=patient_id)

if __name__ == '__main__':
    app.run(debug=True)
