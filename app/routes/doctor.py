from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.utils.decorators import doctor_required
from app.utils.formatters import sex_to_binary, yes_no_into_binary
from app.models import db, DiabetesTest, HeartTest, KidneyTest, Doctor, BookedAppointment, SelfDiagnosis
from app.services.email_service import EmailService
from app.ml_models.loader import classifier, model, kidney_model, diabetes_remedies, heart_remedies, kidney_remedies


doctor = Blueprint('doctor', __name__, url_prefix='/doctor')


@doctor.route('/')
def dashboard():
    return render_template('doctor/Doc.html')


@doctor.route('/diabetesTest', methods=['POST', 'GET'])
@doctor_required
def TestDiabetes():
    diab_prediction = ''
    diab_diagnosis = ''

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            user_input = [
                float(request.form.get('pregnancy')),
                float(request.form.get('gluc')),
                float(request.form.get('bp')),
                float(request.form.get('skt')),
                float(request.form.get('insulin')),
                float(request.form.get('bmi')),
                float(request.form.get('pedigree')),
                float(request.form.get('age'))
            ]
            
            diab_prediction = classifier.predict([user_input])

            if diab_prediction[0] == 0:
                diab_diagnosis = 'The Person is Not Diabetic'
            else:
                diab_diagnosis = 'The person is diabetic'

            try:
                diabetes_test = DiabetesTest(
                    name=name,
                    age=user_input[7],
                    insulin=user_input[4],
                    diab_diagnosis=diab_diagnosis,
                    doctor=session.get('username', 'Unknown') 
                )
                
                db.session.add(diabetes_test)
                db.session.commit()
                
                flash("Test Result saved Successfully!", "success")
                
            except Exception as db_err:
                db.session.rollback()
                flash(f"Database Error: {str(db_err)}", "error")

        except Exception as err2:
            flash(f'Check:{str(err2)}', 'error')

    return render_template('doctor/diabetes.html', diab_diagnosis=diab_diagnosis, remedies=diabetes_remedies)


@doctor.route('/HeartTest', methods=['POST', 'GET'])
@doctor_required
def TestHeart():
    heart_diagnosis = ''
    heart_prediction = ''
   
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            age = request.form.get('age')
            sex = sex_to_binary(request.form.get('sex', "male"))
            cp = request.form.get('cp')
            trestbps = request.form.get('rbp')
            chol = request.form.get('chol')
            fbs = request.form.get('fbs')
            restecg = request.form.get('rer')
            thalach = request.form.get('mhr')
            exang = request.form.get('eia')
            oldpeak = request.form.get('st')
            slope = request.form.get('slope')
            ca = request.form.get('vessels')
            thal = request.form.get('defects')

            user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
            user_input = [float(x) for x in user_input]
            
            heart_prediction = model.predict([user_input])

            if heart_prediction[0] == 1:
                heart_diagnosis = 'The person is having heart disease'
            else:
                heart_diagnosis = 'The person does not have any heart disease'
            
            heart_test = HeartTest(
                name=name,
                age=float(age),
                cholestral=float(chol),
                heart_diagnosis=heart_diagnosis,
                doctor=session.get('username', 'Unknown')
            )
            
            db.session.add(heart_test)
            db.session.commit()
            
            flash("Test Result saved Successfully!", "success")

    except Exception as err2:
        db.session.rollback()
        flash(f'Check:{str(err2)}', 'error')

    return render_template('doctor/heart.html', heart_diagnosis=heart_diagnosis, remedies=heart_remedies)


@doctor.route('/KidneyTest', methods=['POST', 'GET'])
@doctor_required
def TestKidney():
    kidney_diagnosis = ''
    kidney_prediction = ''

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            user_input = [
                float(request.form.get('age') or 0),
                float(request.form.get('blood_pressure') or 0),
                float(request.form.get('specific_gravity') or 0),
                float(request.form.get('albumin') or 0),
                float(request.form.get('sugar') or 0),
                float(request.form.get('blood_glucose') or 0),
                float(request.form.get('blood_urea')),
                float(request.form.get('serum_creatinine') or 0),
                float(request.form.get('sodium') or 0),
                float(request.form.get('potassium') or 0),
                float(request.form.get('hemoglobin')),
                float(request.form.get('packed_cell_volume') or 0),
                float(request.form.get('white_bc') or 0),
                float(request.form.get('red_bc') or 0),
                float(request.form.get('rbc') or 0),
                float(yes_no_into_binary(request.form.get('pus_cells_normal', "no")) or 0),
                float(yes_no_into_binary(request.form.get('puss_cell_clumps_present', "no")) or 0),
                float(yes_no_into_binary(request.form.get('Bacteria_present', "no")) or 0),
                float(yes_no_into_binary(request.form.get('hypertension', "no")) or 0),
                float(yes_no_into_binary(request.form.get('diabetes_mellitus', "no")) or 0),
                float(yes_no_into_binary(request.form.get('coronary_artery_disease', "no")) or 0),
                float(yes_no_into_binary(request.form.get('appetite', "no")) or 0),
                float(yes_no_into_binary(request.form.get('radal_edema', "no")) or 0),
                float(yes_no_into_binary(request.form.get('anaemia', "no")) or 0)
            ]

            kidney_prediction = kidney_model.predict([user_input])

            if kidney_prediction[0] == 0:
                kidney_diagnosis = 'The Person does not have kidney issues'
            else:
                kidney_diagnosis = 'The person has kidney issues'
            
            kidney_test = KidneyTest(
                name=name,
                age=user_input[0],
                blood_glucose=user_input[5],
                kidney_diagnosis=kidney_diagnosis,
                doctor=session.get('username', 'Unknown')
            )
            
            db.session.add(kidney_test)
            db.session.commit()
            
            flash("Test Result saved Successfully!", "success")

        except Exception as err:
            db.session.rollback()
            flash(f'Check:{str(err)}', 'error')

    return render_template('doctor/kidney.html', kidney_diagnosis=kidney_diagnosis, remedies=kidney_remedies)


@doctor.route('/self_diag_records')
def SelfDiagBtn():
    try:
        records = SelfDiagnosis.query.order_by(SelfDiagnosis.time.desc()).all()
    except Exception as err:
        flash(f"Error fetching records: {str(err)}", "error")
        records = []
    
    return render_template('records/selfdiagnosisrecords.html', records=records)


@doctor.route('/doc_appointment')
@doctor_required
def DocAppointments():
    if 'username' not in session:
        flash('Login To Continue!!!', 'warning')
        return redirect(url_for('auth.Login')) 
    
    try:
        username = session['username']
        
        doctor_user = Doctor.query.filter_by(username=username).first()
        
        if not doctor_user:
            flash("Doctor not found!", "danger")
            return redirect(url_for('auth.Login'))
        
        specialty = doctor_user.specialty
        
        appointments = BookedAppointment.query.filter_by(specialist=specialty).all()

        if not appointments:
            flash("No appointments booked yet.", "info")
        else:
            flash('Appointments Fetched Successfully', "success")
                
    except Exception as err:
        flash(f"Error: {str(err)}", "error")
        appointments = []

    return render_template('doctor/doc_appointments.html', appointments=appointments, username=username)


@doctor.route('/heartresults')
@doctor_required
def HeartResultBtn():
    if 'username' not in session:
        flash("Login First", "warning")
        return redirect(url_for('auth.Login'))
    
    try:
        records = HeartTest.query.order_by(HeartTest.created_at.desc()).all()
    except Exception as err:
        flash(f"Error fetching records: {str(err)}", "error")
        records = []
    
    return render_template('records/heartresults.html', records=records)


@doctor.route('/kidneyresults')
@doctor_required
def KidResultBtn():
    if 'username' not in session:
        flash("Login First", "warning")
        return redirect(url_for('auth.Login'))
    
    try:
        records = KidneyTest.query.order_by(KidneyTest.created_at.desc()).all()
    except Exception as err:
        flash(f"Error fetching records: {str(err)}", "error")
        records = []
    
    return render_template('records/kidneyresults.html', records=records)


@doctor.route('/diabetesresults')
@doctor_required
def DiabResultBtn():
    if 'username' not in session:
        flash("Login First", "warning")
        return redirect(url_for('auth.Login'))
    
    try:
        records = DiabetesTest.query.order_by(DiabetesTest.created_at.desc()).all()
    except Exception as err:
        flash(f"Error fetching records: {str(err)}", "error")
        records = []
    
    return render_template('records/diabetesresults.html', records=records)


@doctor.route('/view_records/<int:id>')
@doctor_required
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
        return redirect(url_for('doctor.view_records'))
    

'''
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

'''
    

@doctor.route('/edit_records/<int:id>', methods=['GET', 'POST'])
@doctor_required
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
        
        return render_template('doctor/update.html', record=record_data)
        
    except Exception as err:
        flash(f'Error: {str(err)}', 'error')
        return redirect(url_for('admin.ASelfDiagBtn'))

@doctor.route('/delete_records/<int:id>')
@doctor_required
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
