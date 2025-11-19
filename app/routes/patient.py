from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from app.models import db, SelfDiagnosis, DiabetesTest, HeartTest, KidneyTest,Patient,BookedAppointment
from app.services.email_service import EmailService,send_help_notification, send_diagnosis_notification
from app.utils.decorators import doctor_required,patient_required


patient = Blueprint('patient', __name__, url_prefix='/patient')

@patient.route('/dashboard')
def index():
    return render_template('patient/AIDOC.html')




@patient.route('/patient_appointment')
@patient_required
def PatientAppointments():
    try:
        if 'username' not in session:
            flash('Login or Register to access more features!', 'warning')
            return render_template('admin/contacts.html')
        
        username = session['username']
        
        patient = Patient.query.filter_by(username=username).first()
        
        if not patient:
            flash("Kindly register to access more features!", "error")
            return render_template('admin/contacts.html')
        
  
        appointments = BookedAppointment.query.filter_by(email=patient.email).order_by(BookedAppointment.day).all()
        
        # Convert to list of dictionaries for templates
        appointments_list = []
        for appointment in appointments:
            appointments_list.append({
                'id': appointment.id,
                'patient': appointment.patient,
                'email': appointment.email,
                'specialist': appointment.specialist,
                'day': appointment.day,
                'time': appointment.time
            })
        
        if not appointments_list:
            flash("No appointments booked yet.", "info")
        else:
            flash(f'Appointments fetched successfully {username}', "success")
            return render_template('admin/contacts.html', 
                                 appointment=appointments_list, 
                                 username=username)
                
    except Exception as err:
        flash(f"Error: {str(err)}", "error")
    
    return render_template('general/contacts.html')
