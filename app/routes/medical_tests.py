from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from app.ml_models.predictor import get_prediction,helper
from app.models import db, SelfDiagnosis, DiabetesTest, HeartTest, KidneyTest, SelfDiagnosis
from app.services.email_service import EmailService,send_help_notification, send_diagnosis_notification
from app.utils.formatters import format_symptom
from app.utils.decorators import patient_required

tests = Blueprint('medical_test', __name__, url_prefix='/medical_test')




@tests.route('/dashboard')
def index():
    return render_template('general/home.html')

@tests.route('/predict', methods=['POST', 'GET']) 
def predict():
    predicted_disease = ""
    descr = ''
    my_prec = []
    med = []
    die = []
    work = []

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            symptoms = request.form.get('symptoms')
            
            print(f"DEBUG - Name: {name}")
            print(f"DEBUG - Email: {email}")
            print(f"DEBUG - Raw Symptoms: {symptoms}")
            
            # Validate the form inputs 
            if not name or not email or not symptoms:
                flash("Please fill all fields", "error")
                return render_template(
                    'patient/AIDOC.html', 
                    predicted_disease=predicted_disease,
                    dis_descr=descr,
                    dis_prec=my_prec,
                    dis_med=med,
                    dis_diet=die, 
                    dis_work=work
                )
            
            #Format the symptoms
            user_symptoms = [format_symptom(s.strip()) for s in symptoms.split(',')]
            user_symptoms = [sym.strip("[]' ") for sym in user_symptoms if sym.strip()]
            
            print(f"DEBUG - Formatted Symptoms: {user_symptoms}")
            
            #Check if the symptoms are valid
            if not user_symptoms:
                flash("No valid symptoms provided", "error")
                return render_template(
                    'patient/AIDOC.html', 
                    predicted_disease=predicted_disease,
                    dis_descr=descr,
                    dis_prec=my_prec,
                    dis_med=med,
                    dis_diet=die, 
                    dis_work=work
                )
            
            #Make the prediction with:
            print("DEBUG - Calling get_prediction...")
            predicted_disease = get_prediction(user_symptoms)
            print(f"DEBUG - Predicted Disease: {predicted_disease}")
            
            # Get the predicted disease information
            print("DEBUG - Calling helper...")
            descr, prec, med, die, work = helper(predicted_disease)
            print(f"DEBUG - Description: {descr[:100]}...")
            print(f"DEBUG - Precautions: {prec}")
            
            #Format  the precautions to fit a list
            my_prec = []
            if prec and len(prec) > 0:
                for i in prec[0]:
                    if i:
                        my_prec.append(i)
            
            print(f"DEBUG - Formatted Precautions: {my_prec}")

            if predicted_disease:
                flash("Diagnosis was successful!", "success")

                try:
                    diagnosis = SelfDiagnosis(
                        name=name,
                        email=email,
                        diagnosis=predicted_disease,
                        description=descr,
                        symptoms=symptoms
                    )
                    db.session.add(diagnosis)
                    db.session.commit()
            
                    flash("Test Result saved Successfully!", "success")
                    
                except Exception as db_err:
                    print(f"DEBUG - Database Error: {str(db_err)}")
                    flash(f"Database Error: {str(db_err)}", "error")

                
            else:
                flash("Prediction returned empty result", "error")
        
        except KeyError as ke:
            error_msg = f"Symptom not found: {str(ke)}"
            print(f"DEBUG - KeyError: {error_msg}")
            flash(error_msg, "error")
            
        except Exception as err:
            error_msg = f'Error: {str(err)}'
            print(f"DEBUG - Exception: {error_msg}")
            import traceback
            traceback.print_exc() 
            flash(error_msg, 'error')
                     
    return render_template(
        'patient/AIDOC.html', 
        predicted_disease=predicted_disease,
        dis_descr=descr,
        dis_prec=my_prec,
        dis_med=med,
        dis_diet=die, 
        dis_work=work
    )


@tests.route('/mine')
def Mine():
    diagnoses = []
    try:
        username = session.get('username')
        email = session.get('email')
        
        print(f"Session username: {username}")
        print(f"Session email: {email}")
        
        if not username:
            flash('Please login to view your diagnosis', 'warning')
            return redirect(url_for('auth.login'))
        
        # Get ALL diagnoses by email OR by name
        from sqlalchemy import or_
        
        diagnoses = SelfDiagnosis.query.filter(
            or_(
                SelfDiagnosis.email == email,
                SelfDiagnosis.name == username
            )
        ).order_by(SelfDiagnosis.time.desc()).all()
        
        print(f"Found {len(diagnoses)} diagnosis records")
        
        if diagnoses:
            for diag in diagnoses:
                print(f"  - {diag.name} | {diag.email} | {diag.diagnosis}")
        else:
            print("No diagnosis records found")
            flash('No diagnosis records found. Complete a self-diagnosis to see results here.', 'info')
            
    except Exception as err:
        import traceback
        print(f"Error occurred: {str(err)}")
        traceback.print_exc()
        flash(f'Error: {str(err)}', 'error')

    return render_template('patient/diagPrint.html', diagnoses=diagnoses)
