from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum

db = SQLAlchemy()

def create_default_admin():
    try:
        admin = Admin.query.filter_by(email='admin@gmail.com').first()
        if not admin:
            admin = Admin(
                username='admin',
                email='admin@gmail.com'
            )
            admin.set_password('israel2025')
            admin.password1 = generate_password_hash('israel2025')
            
            db.session.add(admin)
            db.session.commit()
            print("Default admin created successfully!")
            return True
        else:
            print("Admin already exists")
            return False
    except Exception as e:
        db.session.rollback()
        print(f"Error creating default admin: {str(e)}")
        return False

class UserRole(Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"


class User(db.Model):
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches"""
        return check_password_hash(self.password, password)
    
    def has_role(self, role):
        """Check if user has specific role"""
        if isinstance(role, UserRole):
            return self.role == role.value
        return self.role == role
    
    def is_patient(self):
        """Check if user is a patient"""
        return self.role == UserRole.PATIENT.value
    
    def is_doctor(self):
        """Check if user is a doctor"""
        return self.role == UserRole.DOCTOR.value
    
    def is_admin(self):
        """Check if user is an admin"""
        return self.role == UserRole.ADMIN.value


class Doctor(User):
    """Doctor model"""
    __tablename__ = 'register'
    
    full_names = db.Column(db.String(150))
    age = db.Column(db.Integer)
    specialty = db.Column(db.String(100), index=True)
    contact = db.Column(db.String(20))
    day = db.Column(db.String(50))
    time_in = db.Column(db.String(20))
    time_out = db.Column(db.String(20))
    national_id = db.Column(db.String(50), unique=True)
    password1 = db.Column(db.String(255))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = UserRole.DOCTOR.value
    
    def __repr__(self):
        return f'<Doctor {self.full_names}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_names': self.full_names,
            'specialty': self.specialty,
            'contact': self.contact,
            'day': self.day,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active
        }


class Patient(User):
    """Patient model"""
    __tablename__ = 'patient_register'
    
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    contact = db.Column(db.String(20))
    password1 = db.Column(db.String(255))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = UserRole.PATIENT.value
    
    @property
    def full_name(self):
        return f"{self.fname} {self.lname}"
    
    def __repr__(self):
        return f'<Patient {self.full_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'full_name': self.full_name,
            'email': self.email,
            'contact': self.contact,
            'role': self.role,
            'is_active': self.is_active
        }


class Admin(User):
    """Admin model"""
    __tablename__ = 'admin'
    
    password1 = db.Column(db.String(255))
    permissions = db.Column(db.JSON)  # Store specific admin permissions
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = UserRole.ADMIN.value
        if not self.permissions:
            self.permissions = {
                'manage_users': True,
                'manage_appointments': True,
                'view_reports': True,
                'manage_specialties': True
            }
    
    def __repr__(self):
        return f'<Admin {self.username}>'
    
    def has_permission(self, permission):
        """Check if admin has specific permission"""
        return self.permissions.get(permission, False) if self.permissions else False


class SelfDiagnosis(db.Model):
    """Self diagnosis records"""
    __tablename__ = 'self_diagnosis'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    diagnosis = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    symptoms = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<SelfDiagnosis {self.name}: {self.diagnosis}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'diagnosis': self.diagnosis,
            'description': self.description,
            'symptoms': self.symptoms,
            'time': self.time.isoformat() if self.time else None
        }


class DiabetesTest(db.Model):
    """Diabetes test records"""
    __tablename__ = 'diabetes_test'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Float)
    insulin = db.Column(db.Float)
    diab_diagnosis = db.Column(db.String(200))
    doctor = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<DiabetesTest {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'insulin': self.insulin,
            'diab_diagnosis': self.diab_diagnosis,
            'doctor': self.doctor,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class HeartTest(db.Model):
    """Heart disease test records"""
    __tablename__ = 'heart_test'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Float)
    cholestral = db.Column(db.Float)
    heart_diagnosis = db.Column(db.String(200))
    doctor = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<HeartTest {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'cholestral': self.cholestral,
            'heart_diagnosis': self.heart_diagnosis,
            'doctor': self.doctor,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class KidneyTest(db.Model):
    """Kidney disease test records"""
    __tablename__ = 'kidney_test'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Float)
    blood_glucose = db.Column(db.Float)
    kidney_diagnosis = db.Column(db.String(200))
    doctor = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<KidneyTest {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'blood_glucose': self.blood_glucose,
            'kidney_diagnosis': self.kidney_diagnosis,
            'doctor': self.doctor,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Specialty(db.Model):
    """Medical specialties"""
    __tablename__ = 'specialty'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Specialty {self.name}>'


class Appointment(db.Model):
    """Appointment requests"""
    __tablename__ = 'appointment'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    contact = db.Column(db.String(20))
    specialty = db.Column(db.String(100))
    day = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Appointment {self.name} - {self.specialty}>'


class BookedAppointment(db.Model):
    """Confirmed appointments"""
    __tablename__ = 'booked_appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    specialist = db.Column(db.String(100))
    day = db.Column(db.String(50))
    time = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<BookedAppointment {self.patient} - {self.day} {self.time}>'


class Question(db.Model):
    """Help/Support questions"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    contact = db.Column(db.String(20))
    question = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Question {self.names}>'


class Response(db.Model):
    """Responses to questions"""
    __tablename__ = 'responses'
    
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(150))
    question = db.Column(db.Text)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Response to {self.user}>'


class LoginLog(db.Model):
    """Login tracking"""
    __tablename__ = 'login'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), index=True)
    password = db.Column(db.String(255))
    login_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_role = db.Column(db.String(20))  # Track which role logged in
    
    def __repr__(self):
        return f'<LoginLog {self.username} at {self.login_time}>'