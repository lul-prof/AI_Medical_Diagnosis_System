from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
import os

mail = Mail()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    #Load configurations
    from app.config import config
    app.config.from_object(config[config_name])
    
    #Initialize extensions
    from app.models import db
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    
    #Create all database tables
    with app.app_context():
        db.create_all()
        app.logger.info("Database tables created")

        #Create a default admin user
        from app.models import create_default_admin
        create_default_admin()
        app.logger.info(" created default admin user")
    
    # Setup logging
    setup_logging(app)
    
    
    #Register blueprints
    register_blueprints(app)
    
    app.logger.info(f"Application started in {config_name} mode")
    
    return app


def setup_logging(app):
    """Setup application logging"""
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'],
            maxBytes=10240000,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        app.logger.addHandler(file_handler)
        app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))




def register_blueprints(app):  
    # Register blueprints
    from app.routes import auth, patient, doctor, admin, diagnosis, medical_tests, general
    app.register_blueprint(auth.auth)
    app.register_blueprint(patient.patient)
    app.register_blueprint(doctor.doctor)
    app.register_blueprint(admin.admin)
    app.register_blueprint(diagnosis.records)
    app.register_blueprint(medical_tests.tests)
    app.register_blueprint(general.main)
    
    
    return app