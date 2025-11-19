from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from datetime import datetime
from app.utils.decorators import admin_required
from app.models import db, Appointment, Doctor, BookedAppointment,Question, Response,SelfDiagnosis,KidneyTest,HeartTest,DiabetesTest,Patient,Admin
from app.services.email_service import EmailService, send_email_notification


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/dashboard')
def dashboard():
    try:
        stats = {
            'doctors': Doctor.query.filter_by(is_active=True).count(),
            'patients': Patient.query.filter_by(is_active=True).count(),
            'admins': Admin.query.filter_by(is_active=True).count(),
            'appointments': Appointment.query.count(),
            'booked_appointments': BookedAppointment.query.count(),
            'questions': Question.query.count(),
            'self_diagnosis': SelfDiagnosis.query.count(),
            'diabetes_tests': DiabetesTest.query.count(),
            'heart_tests': HeartTest.query.count(),
            'kidney_tests': KidneyTest.query.count(),
            'total_tests': (
                SelfDiagnosis.query.count() + 
                DiabetesTest.query.count() + 
                HeartTest.query.count() + 
                KidneyTest.query.count()
            )
        }
        
        return render_template('admin/admin.html', stats=stats)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        # Return empty stats if there's an error
        stats = {
            'doctors': 0,
            'patients': 0,
            'admins': 0,
            'appointments': 0,
            'booked_appointments': 0,
            'questions': 0,
            'self_diagnosis': 0,
            'diabetes_tests': 0,
            'heart_tests': 0,
            'kidney_tests': 0,
            'total_tests': 0
        }
        return render_template('admin/admin.html', stats=stats)

@admin.route('/appointments', methods=['GET', 'POST'])
@admin_required
def appointments():
    try:
        # Fetch all appointment requests from patients
        patients = Appointment.query.with_entities(
            Appointment.id,
            Appointment.name,
            Appointment.email,
            Appointment.day,
            Appointment.specialty
        ).all()
        
        # Fetch all doctors with their availability
        doctors = Doctor.query.with_entities(
            Doctor.id,
            Doctor.full_names,
            Doctor.specialty,
            Doctor.day,
            Doctor.time_in,
            Doctor.time_out
        ).all()
        
        if request.method == 'POST':
            patient = request.form.get('patient')
            email = request.form.get('email')
            day = request.form.get('day')
            time = request.form.get('time')
            specialist = request.form.get('specialist')
            
            if not all([patient, email, day, time, specialist]):
                flash('Please fill in all required fields', 'error')
                return render_template('admin/appointment.html', 
                                     patients=patients, 
                                     doctors=doctors)
            
            booked_appointment = BookedAppointment(
                patient=patient,
                email=email,
                specialist=specialist,
                day=day,
                time=time,
                created_at=datetime.utcnow()
            )
            
            db.session.add(booked_appointment)
            
            
            db.session.commit()
            
            #Send email notification
            try:
                email_sent =EmailService.send_appointment_notification(email, patient, day, time)
                if email_sent:
                    flash(f"Appointment booked successfully! Confirmation sent to {email}", "success")
                else:
                    flash("Appointment booked, but email notification failed", "warning")
            except Exception as email_err:
                flash(f"Appointment booked, but email error: {str(email_err)}", "warning")
            
            return redirect(url_for('admin.appointments'))
        
    except Exception as err:
        db.session.rollback()
        flash(f"Error processing appointments: {str(err)}", "error")
        patients = []
        doctors = []
    
    return render_template('admin/appointment.html', patients=patients, doctors=doctors)


@admin.route('/response', methods=['GET', 'POST'])
@admin_required
def response():
    """Admin FAQ/Question response management"""
    try:
        # Fetch all unanswered questions
        questions = Question.query.with_entities(
            Question.id,
            Question.names,
            Question.email,
            Question.contact,
            Question.question,
            Question.created_at
        ).order_by(Question.created_at.desc()).all()
        
        if request.method == 'POST':
            user = request.form.get('user')
            email = request.form.get('email')
            question_text = request.form.get('question')
            response_text = request.form.get('response')
            question_id = request.form.get('question_id')
            
            if not all([user, email, question_text, response_text]):
                flash('Please fill in all required fields', 'error')
                return render_template('admin/response.html', questions=questions)
            
            if not response_text.strip():
                flash('Response cannot be empty', 'error')
                return render_template('admin/response.html', questions=questions)
            
            new_response = Response(
                user=user,
                question=question_text,
                response=response_text,
                created_at=datetime.utcnow()
            )
            
            db.session.add(new_response)
            
            if question_id:
                question = Question.query.get(int(question_id))
                if question:
                    db.session.delete(question)
                    
            db.session.commit()
            
            #Send email notification
            try:
                email_sent = EmailService.send_help(email, user, question_text, response_text)
                if email_sent:
                    flash(f"Response sent successfully! Email notification sent to {email}", "success")
                else:
                    flash("Response saved, but email notification failed", "warning")
            except Exception as email_err:
                flash(f"Response saved, but email error: {str(email_err)}", "warning")
            
            return redirect(url_for('admin.response'))
        
    except Exception as err:
        db.session.rollback()
        flash(f"Error processing response: {str(err)}", "error")
        questions = []
    
    return render_template('admin/response.html', questions=questions)


@admin.route('/a_self_diag_records')
@admin_required
def ASelfDiagBtn():
    
        try:
            records = SelfDiagnosis.query.with_entities(
                SelfDiagnosis.id,
                SelfDiagnosis.name,
                SelfDiagnosis.diagnosis,
                SelfDiagnosis.time,
                SelfDiagnosis.symptoms
            ).order_by(SelfDiagnosis.time.desc()).all()
            
            records_list = []
            for record in records:
                records_list.append({
                    'id': record.id,
                    'name': record.name,
                    'diagnosis': record.diagnosis,
                    'time': record.time.strftime('%Y-%m-%d %H:%M:%S') if record.time else '',
                    'symptoms': record.symptoms
                })
            
            return render_template('admin/adminselfdiagnosisrecords.html', records=records_list)

        except Exception as err:
            flash(f'The following error occurred: {str(err)}', 'error')
            return render_template('admin/adminselfdiagnosisrecords.html', records=[])


@admin.route('/view_records/<int:id>')
@admin_required
def view_records(id):
    try:
        record = SelfDiagnosis.query.get_or_404(id)
        record_data = {
            'id': record.id,
            'name': record.name,
            'email': record.email,
            'diagnosis': record.diagnosis,
            'description': record.description,
            'symptoms': record.symptoms,
            'time': record.time.strftime('%Y-%m-%d %H:%M:%S') if record.time else ''
        }
        return render_template('records/view-selfD.html', record=record_data)
    except Exception as err:
        flash(f'Error fetching record: {str(err)}', 'error')
        return redirect(url_for('admin.view_records'))

@admin.route('/delete_records/<int:id>')
@admin_required
def delete_records(id):
    try:
        record = SelfDiagnosis.query.get_or_404(id)
        db.session.delete(record)
        db.session.commit()
        flash("Record deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting record: {str(e)}", "error")

    return redirect(url_for('admin.ASelfDiagBtn'))   

@admin.route('/edit_records/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_records(id):
    try:
        record = SelfDiagnosis.query.get_or_404(id)
        
        if request.method == 'POST':
            try:
                record.name = request.form['name']
                record.email = request.form['email']
                record.diagnosis = request.form['diagnosis']
                record.description = request.form['description']
                
                db.session.commit()
                flash("Record updated successfully!", "success")
                return redirect(url_for('admin.ASelfDiagBtn'))
                
            except Exception as e:
                db.session.rollback()
                flash(f"Error updating record: {str(e)}", "error")
        
        record_data = {
            'id': record.id,
            'name': record.name,
            'email': record.email,
            'diagnosis': record.diagnosis,
            'description': record.description,
            'symptoms': record.symptoms,
            'time': record.time.strftime('%Y-%m-%d %H:%M:%S') if record.time else ''
        }
        
        return render_template('admin/update.html', record=record_data)
        
    except Exception as err:
        flash(f'Error: {str(err)}', 'error')
        return redirect(url_for('admin.ASelfDiagBtn'))


@admin.route('/a_diabetesresults')
@admin_required
def DiabeResultBtn():
    try:
        records = DiabetesTest.query.order_by(DiabetesTest.created_at.desc()).all()
        records_list = [record.to_dict() for record in records]
        
        print(f"Diabetes records count: {len(records_list)}")  
        return render_template('admin/admindiabetesresults.html', records=records_list)
    except Exception as err:
        print(f"Error: {str(err)}")  
        import traceback
        traceback.print_exc()
        flash(f'Error: {str(err)}', 'error')
        return render_template('admin/admindiabetesresults.html', records=[])

@admin.route('/a_heartresults')
@admin_required
def HeartAResultBtn():
    try:
        records = HeartTest.query.order_by(HeartTest.created_at.desc()).all()
        records_list = [record.to_dict() for record in records]
        
        print(f"Heart records count: {len(records_list)}")  
        return render_template('admin/adminheartresults.html', records=records_list)
    except Exception as err:
        print(f"Error: {str(err)}")  
        import traceback
        traceback.print_exc()
        flash(f'Error: {str(err)}', 'error')
        return render_template('admin/adminheartresults.html', records=[])

@admin.route('/a_kidneyresults')
@admin_required
def KidnResultBtn():
    try:
        records = KidneyTest.query.order_by(KidneyTest.created_at.desc()).all()
        records_list = [record.to_dict() for record in records]
        
        print(f"Kidney records count: {len(records_list)}")  
        return render_template('admin/adminkidneyresults.html', records=records_list)
    except Exception as err:
        print(f"Error: {str(err)}")  
        import traceback
        traceback.print_exc()
        flash(f'Error: {str(err)}', 'error')
        return render_template('admin/adminkidneyresults.html', records=[])
    

@admin.route('/view_doctors')
@admin_required
def ViewDoc():
    try:
        doctors = Doctor.query.filter_by(is_active=True).order_by(Doctor.full_names).all()
        doctors_list = [{
            'id': doctor.id,
            'full_names': doctor.full_names,
            'email': doctor.email,
            'specialty': doctor.specialty,
            'contact': doctor.contact,
            'day': doctor.day,
            'time_in': doctor.time_in,
            'time_out': doctor.time_out,
            'created_at': doctor.created_at.strftime('%Y-%m-%d %H:%M:%S') if doctor.created_at else ''
        } for doctor in doctors]
        return render_template('admin/viewDoctors.html', doctors=doctors_list)
    except Exception as err:
        flash(f'Error fetching doctors: {str(err)}', 'error')
        return render_template('admin/viewDoctors.html', doctors=[])

@admin.route('/view_patients')
@admin_required
def ViewPat():
    try:
        patients = Patient.query.filter_by(is_active=True).order_by(Patient.fname, Patient.lname).all()
        patients_list = [{
            'id': patient.id,
            'fname': patient.fname,
            'lname': patient.lname,
            'full_name': patient.full_name,
            'email': patient.email,
            'contact': patient.contact,
            'created_at': patient.created_at.strftime('%Y-%m-%d %H:%M:%S') if patient.created_at else ''
        } for patient in patients]
        return render_template('admin/viewPatients.html', patients=patients_list)
    except Exception as err:
        flash(f'Error fetching patients: {str(err)}', 'error')
        return render_template('admin/viewPatients.html', patients=[])

@admin.route('/view_admins')
@admin_required
def ViewAdm():
    try:
        admins = Admin.query.filter_by(is_active=True).order_by(Admin.username).all()
        admins_list = [{
            'id': admin.id,
            'username': admin.username,
            'email': admin.email,
            'created_at': admin.created_at.strftime('%Y-%m-%d %H:%M:%S') if admin.created_at else '',
            'permissions': admin.permissions
        } for admin in admins]
        return render_template('admin/viewAdmins.html', admins=admins_list)
    except Exception as err:
        flash(f'Error fetching admins: {str(err)}', 'error')
        return render_template('admin/viewAdmins.html', admins=[])
    


@admin.route('/populate_test_data')
@admin_required
def populate_test_data():
    try:
        #Add Diabetes Test
        diabetes = DiabetesTest(
            name="John Doe",
            age=45.0,
            insulin=85.5,
            diab_diagnosis="Normal - No diabetes detected",
            doctor="Dr. Smith"
        )
        db.session.add(diabetes)
        
        #Add Heart Test
        heart = HeartTest(
            name="Jane Smith",
            age=52.0,
            cholestral=220.0,
            heart_diagnosis="High cholesterol - Monitor levels",
            doctor="Dr. Johnson"
        )
        db.session.add(heart)
        
        #Add Kidney Test
        kidney = KidneyTest(
            name="Bob Wilson",
            age=38.0,
            blood_glucose=95.0,
            kidney_diagnosis="Normal kidney function",
            doctor="Dr. Brown"
        )
        db.session.add(kidney)
        
        db.session.commit()
        flash("Test data added successfully!", "success")
        return redirect(url_for('admin.dashboard'))
        
    except Exception as e:
        db.session.rollback()
        import traceback
        flash(f"Error: {str(e)}", "error")
        return f"<pre>{traceback.format_exc()}</pre>"