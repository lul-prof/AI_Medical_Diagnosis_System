from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from app.models import db, Doctor, Patient, Admin, LoginLog,UserRole
from app.services.email_service import EmailService
from app.utils.decorators import admin_required

auth = Blueprint('auth', __name__, url_prefix='/auth')



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login to access this page', 'warning')
                return redirect(url_for('auth.login'))
            
            if 'user_role' not in session or session['user_role'] not in roles:
                flash('You do not have permission to access this page', 'danger')
                return redirect(url_for('main.index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type', 'patient') 
        
        if not email or not password:
            flash('Please provide both email and password', 'error')
            return render_template('auth/login.html')
        
        try:
            user = None
            role = None
            
            if user_type == 'doctor':
                user = Doctor.query.filter_by(email=email).first()
                role = 'doctor'
            elif user_type == 'admin':
                user = Admin.query.filter_by(email=email).first()
                role = 'admin'
            else: 
                user = Patient.query.filter_by(email=email).first()
                role = 'patient'
            
            if user and user.check_password(password):
                #session variables
                session['user_id'] = user.id
                session['username'] = user.username
                session['email'] = user.email
                session['user_role'] = role
                
                #patient-specific session data
                if role == 'patient':
                    session['fname'] = user.fname
                    session['lname'] = user.lname
                    session['name'] = user.full_name
                elif role == 'doctor':
                    session['name'] = user.full_names
                    session['specialty'] = user.specialty
                
                # Log the login
                log_entry = LoginLog(
                    username=user.username,
                    email=user.email,
                    #Do not log the actual password
                    password='***'  
                )
                db.session.add(log_entry)
                db.session.commit()
                
                flash(f'Welcome back, {user.username}!', 'success')
                
                #Redirect to other pages based on User role
                if role == 'doctor':
                    try:
                        EmailService.send_login_notification(email, email)
                        flash("Message sent to your email successfully", "success")
                    
                    except Exception as email_err:
                        print(f"DEBUG - Email Error: {str(email_err)}")
                        flash(f"Email Error: {str(email_err)}", "warning")
                
                    return redirect(url_for('doctor.dashboard'))
                

                elif role == 'admin':
                    try:
                        EmailService.send_login_notification(email, email)
                        flash("Message sent to your email successfully", "success")
                    
                    except Exception as email_err:
                        print(f"DEBUG - Email Error: {str(email_err)}")
                        flash(f"Email Error: {str(email_err)}", "warning")

                    return redirect(url_for('admin.dashboard'))
                


                else:
                    try:
                        EmailService.send_login_notification(email, email)
                        flash("Message sent to your email successfully", "success")
                    
                    except Exception as email_err:
                        print(f"DEBUG - Email Error: {str(email_err)}")
                        flash(f"Email Error: {str(email_err)}", "warning")

                    return redirect(url_for('patient.index'))
                


            
            else:
                flash('Invalid email or password', 'error')
        
        except Exception as err:
            flash(f'Login error: {str(err)}', 'error')
    
    return render_template('auth/login.html')



@auth.route('/register/patient', methods=['GET', 'POST'])
def register_patient():
    #Patient registration
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            contact = request.form.get('contact')
            password = request.form.get('password')
            password_confirm = request.form.get('password_confirm')
            
            #Validate inputs
            if not all([username, email, fname, lname, password]):
                flash('Please fill in all required fields', 'error')
                return render_template('auth/register_patient.html')
            
            if password != password_confirm:
                flash('Passwords do not match', 'error')
                return render_template('auth/register_patient.html')
            
            #Check if the user tryig to register exists
            if Patient.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
                return render_template('auth/register_patient.html')
            
            if Patient.query.filter_by(username=username).first():
                flash('Username already taken', 'error')
                return render_template('auth/register_patient.html')
            
            #Create a new patient
            patient = Patient(
                username=username,
                email=email,
                fname=fname,
                lname=lname,
                contact=contact
            )
            patient.set_password(password)
            patient.password1 = generate_password_hash(password) 
            
            db.session.add(patient)
            db.session.commit()

            try:
                EmailService.send_registration_notification(email, username)

                flash("Message sent to your email successfully", "success")
                    
            except Exception as email_err:
                    print(f"DEBUG - Email Error: {str(email_err)}")
                    flash(f"Email Error: {str(email_err)}", "warning")
            
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        
        except Exception as err:
            db.session.rollback()
            flash(f'Registration error: {str(err)}', 'error')
    
    return render_template('auth/register_patient.html')


@auth.route('/register/doctor', methods=['GET', 'POST'])
def register_doctor():
    if UserRole != 'admin':
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('auth.login'))
    
    #Doctor registration
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            full_names = request.form.get('full_names')
            age = request.form.get('age')
            specialty = request.form.get('specialty')
            contact = request.form.get('contact')
            day = request.form.get('day')
            time_in = request.form.get('time_in')
            time_out = request.form.get('time_out')
            national_id = request.form.get('national_id')
            password = request.form.get('password')
            password_confirm = request.form.get('password_confirm')
            
            if not all([username, email, full_names, specialty, password, national_id]):
                flash('Please fill in all required fields', 'error')
                return render_template('auth/register_doctor.html')
            
            if password != password_confirm:
                flash('Passwords do not match', 'error')
                return render_template('auth/register_doctor.html')
            
          
            if Doctor.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
                return render_template('auth/register_doctor.html')
            
            if Doctor.query.filter_by(national_id=national_id).first():
                flash('National ID already registered', 'error')
                return render_template('auth/register_doctor.html')
            
            # Create a new doctor if successful 
            doctor = Doctor(
                username=username,
                email=email,
                full_names=full_names,
                age=int(age) if age else None,
                specialty=specialty,
                contact=contact,
                day=day,
                time_in=time_in,
                time_out=time_out,
                national_id=national_id
            )
            doctor.set_password(password)
            doctor.password1 = generate_password_hash(password)
            
            db.session.add(doctor)
            db.session.commit()

            
            try:
                EmailService.send_registration_notification(email, username)
                
                flash("Message sent to your email successfully", "success")

                    
            except Exception as email_err:
                    print(f"DEBUG - Email Error: {str(email_err)}")
                    flash(f"Email Error: {str(email_err)}", "warning")

            
            flash('Doctor registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        
        
        except Exception as err:
            db.session.rollback()
            flash(f'Registration error: {str(err)}', 'error')
    
    return render_template('auth/register_doctor.html')


@auth.route('/register/admin', methods=['GET', 'POST'])
@role_required('admin')
def register_admin():
    #Admin registration=>restricted
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            password_confirm = request.form.get('password_confirm')
            
            if not all([username, email, password]):
                flash('Please fill in all required fields', 'error')
                return render_template('auth/register_admin.html')
            
            if password != password_confirm:
                flash('Passwords do not match', 'error')
                return render_template('auth/register_admin.html')
            
            if Admin.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
                return render_template('auth/register_admin.html')
            
            admin = Admin(
                username=username,
                email=email
            )
            admin.set_password(password)
            admin.password1 = generate_password_hash(password)
            
            db.session.add(admin)
            db.session.commit()

            try:
                EmailService.send_registration_notification(email, username)
                
                flash("Message sent to your email successfully", "success")
                    
            except Exception as email_err:
                    print(f"DEBUG - Email Error: {str(email_err)}")
                    flash(f"Email Error: {str(email_err)}", "warning")
                                
            flash('Admin created successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
        
        except Exception as err:
            db.session.rollback()
            flash(f'Registration error: {str(err)}', 'error')
    
    return render_template('auth/register_admin.html')


#Logout 
@auth.route('/logout')
def logout():
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out.', 'info')
    return redirect(url_for('auth.login'))



@auth.route('/profile')
@login_required
def profile():
    user_id = session.get('user_id')
    role = session.get('user_role')
    
    user = None
    if role == 'doctor':
        user = Doctor.query.get(user_id)
    elif role == 'patient':
        user = Patient.query.get(user_id)
    elif role == 'admin':
        user = Admin.query.get(user_id)
    
    return render_template('auth/profile.html', user=user, role=role)


@auth.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_id = session.get('user_id')
    role = session.get('user_role')
    
    if role == 'patient':
        user = Patient.query.get(user_id)
        
        if request.method == 'POST':
            try:
                user.fname = request.form.get('fname')
                user.lname = request.form.get('lname')
                user.contact = request.form.get('contact')
                
                db.session.commit()
                
                # Update session
                session['fname'] = user.fname
                session['lname'] = user.lname
                session['name'] = user.full_name
                
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('auth.profile'))
            
            except Exception as err:
                db.session.rollback()
                flash(f'Update error: {str(err)}', 'error')
    
    elif role == 'doctor':
        user = Doctor.query.get(user_id)
        
        if request.method == 'POST':
            try:
                user.full_names = request.form.get('full_names')
                user.contact = request.form.get('contact')
                user.specialty = request.form.get('specialty')
                user.day = request.form.get('day')
                user.time_in = request.form.get('time_in')
                user.time_out = request.form.get('time_out')
                
                db.session.commit()
                
                #Update session
                session['name'] = user.full_names
                session['specialty'] = user.specialty
                
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('auth.profile'))
            
            except Exception as err:
                db.session.rollback()
                flash(f'Update error: {str(err)}', 'error')
    
    return render_template('auth/edit_profile.html', user=user, role=role)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        user_id = session.get('user_id')
        role = session.get('user_role')
        
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([current_password, new_password, confirm_password]):
            flash('Please fill in all fields', 'error')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return render_template('auth/change_password.html')
        
        try:
            # Get user based on their role
            if role == 'doctor':
                user = Doctor.query.get(user_id)
            elif role == 'patient':
                user = Patient.query.get(user_id)
            elif role == 'admin':
                user = Admin.query.get(user_id)
            else:
                flash('Invalid user role', 'error')
                return redirect(url_for('auth.logout'))
            
            #Verify the current password
            if not user.check_password(current_password):
                flash('Current password is incorrect', 'error')
                return render_template('auth/change_password.html')
            
            #Update  the password
            user.set_password(new_password)
            user.password1 = generate_password_hash(new_password)
            
            db.session.commit()
            
            flash('Password changed successfully!', 'success')
            return redirect(url_for('auth.profile'))
        
        except Exception as err:
            db.session.rollback()
            flash(f'Error changing password: {str(err)}', 'error')
    
    return render_template('auth/change_password.html')



@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        # Check all user types
        user = (Patient.query.filter_by(email=email).first() or
                Doctor.query.filter_by(email=email).first() or
                Admin.query.filter_by(email=email).first())
        
        if user:
            #Send password reset email method 
            flash('Password reset instructions sent to your email', 'info')
        else:
            # Do not reveal if email exists or not =>security purposes
            flash('If that email exists, reset instructions have been sent', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html')