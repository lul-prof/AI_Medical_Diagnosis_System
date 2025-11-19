#Handles all email notifications for the medical diagnosis system => Email Service Module
from flask_mail import Message
from flask import current_app, flash
from app import mail
from typing import Optional, List
import logging


class EmailService:
    #Service class for handling all email notifications
    @staticmethod
    def send_email(subject: str, recipient: str, body: str, 
                   html: Optional[str] = None) -> bool:
        try:
            msg = Message(
                subject=subject,
                recipients=[recipient],
                body=body,
                html=html
            )
            mail.send(msg)
            current_app.logger.info(f"Email sent successfully to {recipient}")
            return True
        except Exception as e:
            current_app.logger.error(f"Email sending error to {recipient}: {str(e)}")
            flash(f"Email Sending Error: {str(e)}", "error")
            return False
    
    @staticmethod
    def send_bulk_email(subject: str, recipients: List[str], 
                       body: str, html: Optional[str] = None) -> bool:
        try:
            msg = Message(
                subject=subject,
                recipients=recipients,
                body=body,
                html=html
            )
            mail.send(msg)
            current_app.logger.info(f"Bulk email sent to {len(recipients)} recipients")
            return True
        except Exception as e:
            current_app.logger.error(f"Bulk email error: {str(e)}")
            flash(f"Email Sending Error: {str(e)}", "error")
            return False
    
    #<--------------- Authentication Emails ------------->
    
    @staticmethod
    def send_registration_notification(email: str, name: str) -> bool:

        subject = "Welcome to Medical Diagnosis System - Account Created Successfully"
        
        body = f"""Hello {name},

Welcome to the Medical Diagnosis System!

Your account has been created successfully. You can now log in and access all features of our platform.

Key Features:
- AI-powered disease diagnosis
- Medical test management
- Appointment booking
- Health records tracking

If you didn't create this account, please contact our support team immediately.

Best regards,
Medical Diagnosis System Team
"""
        
        html = f"""
        <html>
        <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2 style="color: #2c3e50;">Welcome to Medical Diagnosis System! 🏥</h2>
                    
                    <p>Hello <strong>{name}</strong>,</p>
                    
                    <p>Your account has been created successfully! We're excited to have you on board.</p>
                    
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #2c3e50;">Key Features:</h3>
                        <ul>
                            <li><i class="fa-solid fa-magnifying-glass"></i>AI-powered disease diagnosis</li>
                            <li><i class="fa-solid fa-stethoscope"></i>Medical test management</li>
                            <li><i class="fa-solid fa-calendar"></i> Appointment booking</li>
                            <li><i class="fa-solid fa-chart-simple"></i> Health records tracking</li>
                        </ul>
                    </div>
                    
                    <p style="color: #e74c3c; font-size: 0.9em;">
                        <strong>Security Notice:</strong> If you didn't create this account, please contact our support team immediately.
                    </p>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <p style="font-size: 0.9em; color: #7f8c8d;">
                        Best regards,<br>
                        <strong>Medical Diagnosis System Team</strong>
                    </p>
                </div>
            </body>
        </html>
        """
        
        return EmailService.send_email(subject, email, body, html)
    
    @staticmethod
    def send_login_notification(email: str, username: str) -> bool:
   
        subject = "Login Notification - Medical Diagnosis System"
        
        body = f"""Hello {username},

Your account was successfully logged in to the Medical Diagnosis System.

Time: Just now
Location: Based on your IP address

If this wasn't you, please secure your account immediately by:
1. Changing your password
2. Contacting our support team

Stay safe,
Medical Diagnosis System Team
"""
        
        html = f"""
        <html>
        <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2 style="color: #2c3e50;">Login Notification <i class="fa-solid fa-user-lock"></i></h2>
                    
                    <p>Hello <strong>{username}</strong>,</p>
                    
                    <p>Your account was successfully logged in to the Medical Diagnosis System.</p>
                    
                    <div style="background-color: #e8f5e9; padding: 15px; border-left: 4px solid #4caf50; margin: 20px 0;">
                        <p style="margin: 0;"><strong>Login Time:</strong> Just now</p>
                        <p style="margin: 5px 0 0 0;"><strong>Status:</strong> <span style="color: #4caf50;">Successful</span></p>
                    </div>
                    
                    <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
                        <p style="margin: 0; font-weight: bold;"><i class="fa-solid fa-biohazard"></i> If this wasn't you:</p>
                        <ol style="margin: 10px 0 0 0;">
                            <li>Change your password immediately</li>
                            <li>Contact our support team</li>
                            <li>Review your recent account activity</li>
                        </ol>
                    </div>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <p style="font-size: 0.9em; color: #7f8c8d;">
                        Stay safe,<br>
                        <strong>Medical Diagnosis System Team</strong>
                    </p>
                </div>
            </body>
        </html>
        """
        
        return EmailService.send_email(subject, email, body, html)
    
    # ==================== Diagnosis Emails ====================
    
    @staticmethod
    def send_diagnosis_notification(email: str, name: str, 
                                    diagnosis: str, description: str) -> bool:
  
        subject = f"Medical Diagnosis Report - {diagnosis}"
        
        body = f"""Hello {name},

AI-Predicted Diagnosis Report
===================================

Diagnosis: {diagnosis}

Description:
{description}

IMPORTANT DISCLAIMER:
This is an AI-assisted preliminary diagnosis. The results might not be 100% accurate.
Please consult with a qualified healthcare professional for proper evaluation and treatment.

If you're experiencing severe symptoms, seek immediate medical attention.

Thank you for using our system.

Best regards,
Medical Diagnosis System Team
"""
        
        html = f"""
        <html>
            <head>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
            </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2 style="color: #2c3e50;">Medical Diagnosis Report <i class="fa-solid fa-clipboard-user"></i></h2>
                    
                    <p>Hello <strong>{name}</strong>,</p>
                    
                    <div style="background-color: #e3f2fd; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #1976d2;">AI-Predicted Diagnosis</h3>
                        <p style="font-size: 1.2em; margin: 10px 0;"><strong>{diagnosis}</strong></p>
                        
                        <h4 style="color: #1976d2; margin-top: 20px;">Description:</h4>
                        <p style="margin: 10px 0;">{description}</p>
                    </div>
                    
                    <div style="background-color: #ffebee; padding: 15px; border-left: 4px solid #f44336; margin: 20px 0;">
                        <h4 style="margin-top: 0; color: #c62828;"><i class="fa-solid fa-triangle-exclamation" style="color: #FFD43B;"></i> IMPORTANT DISCLAIMER</h4>
                        <ul style="margin: 10px 0;">
                            <li>This is an <strong>AI-assisted preliminary diagnosis</strong></li>
                            <li>Results might <strong>not be 100% accurate</strong></li>
                            <li><strong>Consult a qualified healthcare professional</strong> for proper evaluation</li>
                            <li>Seek <strong>immediate medical attention</strong> for severe symptoms</li>
                        </ul>
                    </div>
                    
                    <div style="background-color: #f1f8e9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h4 style="margin-top: 0; color: #558b2f;">Next Steps:</h4>
                        <ol>
                            <li>Review the diagnosis and description carefully</li>
                            <li>Schedule an appointment with a healthcare provider</li>
                            <li>Monitor your symptoms</li>
                            <li>Follow recommended precautions</li>
                        </ol>
                    </div>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <p style="font-size: 0.9em; color: #7f8c8d;">
                        Thank you for using our system.<br>
                        <strong>Medical Diagnosis System Team</strong>
                    </p>
                </div>
            </body>
        </html>
        """
        
        return EmailService.send_email(subject, email, body, html)
    
    # ==================== Appointment Emails ====================
    
    @staticmethod
    def send_appointment_notification(email: str, name: str, 
                                     day: str, time: str, 
                                     specialist: Optional[str] = None) -> bool:
  
        subject = "Appointment Confirmation - Medical Diagnosis System"
        
        specialist_info = f"\nSpecialist: {specialist}" if specialist else ""
        
        body = f"""Hello {name},

Your appointment has been successfully booked!

Appointment Details:
====================
Date: {day}
Time: {time}{specialist_info}

Please arrive 15 minutes before your scheduled time.

Important Reminders:
- Bring a valid ID
- Bring any relevant medical records
- Bring your insurance card (if applicable)
- Inform us if you need to reschedule at least 24 hours in advance

If you have any questions, please contact our support team.

Thank you for choosing our services.

Best regards,
Medical Diagnosis System Team
"""
        
        html = f"""
        <html>
         <head>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
            </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2 style="color: #2c3e50;">Appointment Confirmed! <i class="fa-thumbprint fa-light fa-check" style="--fa-primary-color: #63E6BE; --fa-secondary-color: #63E6BE;"></i></h2>
                    
                    <p>Hello <strong>{name}</strong>,</p>
                    
                    <p>Your appointment has been successfully booked!</p>
                    
                    <div style="background-color: #e8f5e9; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #2e7d32;"><i class="fa-duotone fa-solid fa-calendar-days" style="--fa-primary-color: #FFD43B; --fa-secondary-color: #3d91ff;"></i> Appointment Details</h3>
                        <table style="width: 100%;">
                            <tr>
                                <td style="padding: 8px 0;"><strong>Date:</strong></td>
                                <td style="padding: 8px 0;">{day}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0;"><strong>Time:</strong></td>
                                <td style="padding: 8px 0;">{time}</td>
                            </tr>
                            {f'<tr><td style="padding: 8px 0;"><strong>Specialist:</strong></td><td style="padding: 8px 0;">{specialist}</td></tr>' if specialist else ''}
                        </table>
                    </div>
                    
                    <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
                        <h4 style="margin-top: 0; color: #856404;"><i class="fa-thin fa-file-medical" style="color: #FFD43B;"></i> Important Reminders</h4>
                        <ul style="margin: 10px 0;">
                            <li>Arrive <strong>15 minutes early</strong></li>
                            <li>Bring a valid <strong>ID</strong></li>
                            <li>Bring relevant <strong>medical records</strong></li>
                            <li>Bring your <strong>insurance card</strong> (if applicable)</li>
                            <li>Reschedule at least <strong>24 hours in advance</strong> if needed</li>
                        </ul>
                    </div>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <p style="font-size: 0.9em; color: #7f8c8d;">
                        Thank you for choosing our services.<br>
                        <strong>Medical Diagnosis System Team</strong>
                    </p>
                </div>
            </body>
        </html>
        """
        
        return EmailService.send_email(subject, email, body, html)
    
    # ==================== Doctor/Staff Emails ====================
    
    @staticmethod
    def send_doctor_notification(email: str, name: str, specialty: str, 
                                 day: str, password: str) -> bool:
    
        subject = "Employment Confirmation - Medical Diagnosis System"
        
        body = f"""Hello Dr. {name},

Welcome to the Medical Diagnosis System team!

Your employment as a doctor specializing in {specialty} has been confirmed.

Account Details:
================
Email: {email}
Temporary Password: {password}
Specialty: {specialty}
Working Day: {day}

IMPORTANT: Please change your password immediately after your first login.

You are expected to report to work every {day}. Please review your schedule and responsibilities in the staff portal.

If you have any questions, please contact the HR department.

Welcome aboard!

Best regards,
Medical Diagnosis System Administration
"""
        
        html = f"""
        <html>
            <head>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
            </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2 style="color: #2c3e50;">Welcome to Our Team!<i class="fa-thin fa-handshake" style="color: #74C0FC;"></i> </h2>
                    
                    <p>Hello <strong>Dr. {name}</strong>,</p>
                    
                    <p>Welcome to the Medical Diagnosis System team!</p>
                    
                    <div style="background-color: #e3f2fd; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #1976d2;"><i class="fa-thin fa-circle-info fa-lg" style="color: #FFD43B;"></i> Account Details</h3>
                        <table style="width: 100%;">
                            <tr>
                                <td style="padding: 8px 0;"><strong>Email:</strong></td>
                                <td style="padding: 8px 0;">{email}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0;"><strong>Specialty:</strong></td>
                                <td style="padding: 8px 0;">{specialty}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0;"><strong>Working Day:</strong></td>
                                <td style="padding: 8px 0;">{day}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <div style="background-color: #ffebee; padding: 15px; border-left: 4px solid #f44336; margin: 20px 0;">
                        <h4 style="margin-top: 0; color: #c62828;"><i class="fa-solid fa-user-lock" style="color: #FFD43B;"></i> Temporary Password</h4>
                        <p style="font-size: 1.2em; font-family: monospace; background: #fff; padding: 10px; border-radius: 3px;">
                            {password}
                        </p>
                        <p style="color: #c62828; margin: 10px 0 0 0;">
                            <strong><i class="fa-solid fa-triangle-exclamation" style="color: #FFD43B;"></i> IMPORTANT:</strong> Change this password immediately after your first login!
                        </p>
                    </div>
                    
                    <div style="background-color: #f1f8e9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h4 style="margin-top: 0; color: #558b2f;">Next Steps:</h4>
                        <ol>
                            <li>Log in to the system</li>
                            <li>Change your password</li>
                            <li>Complete your profile</li>
                            <li>Review your schedule</li>
                            <li>Familiarize yourself with the platform</li>
                        </ol>
                    </div>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <p style="font-size: 0.9em; color: #7f8c8d;">
                        Welcome aboard!<br>
                        <strong>Medical Diagnosis System Administration</strong>
                    </p>
                </div>
            </body>
        </html>
        """
        
        return EmailService.send_email(subject, email, body, html)
    
    # ==================== Support Emails ====================
    
    @staticmethod
    def send_help_notification(email: str, name: str) -> bool:

        subject = "Help Request Received - Medical Diagnosis System"
        
        body = f"""Hello {name},

Thank you for contacting us!

Your question has been received successfully. Our support team will review your inquiry and respond within 48 hours.

Reference Number: #{hash(email) % 100000:05d}

If your issue is urgent, please call our support hotline.

Thank you for your patience.

Best regards,
Medical Diagnosis System Support Team
"""
        
        html = f"""
        <html>
            <head>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
            </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2 style="color: #2c3e50;">Help Request Received <i class="fa-light fa-message" style="color: #74C0FC;"></i></h2>
                    
                    <p>Hello <strong>{name}</strong>,</p>
                    
                    <p>Thank you for contacting us!</p>
                    
                    <div style="background-color: #e8f5e9; padding: 20px; border-radius: 5px; margin: 20px 0; text-align: center;">
                        <h3 style="margin-top: 0; color: #2e7d32;"><i class="fa-solid fa-check" style="color: #3eb41d;"></i> Request Confirmed</h3>
                        <p style="font-size: 0.9em; margin: 10px 0;">Reference Number:</p>
                        <p style="font-size: 1.5em; font-weight: bold; margin: 5px 0; color: #2e7d32;">
                            #{hash(email) % 100000:05d}
                        </p>
                        <p style="font-size: 0.9em; margin: 10px 0;">
                            Response time: <strong>Within 48 hours</strong>
                        </p>
                    </div>
                    
                    <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
                        <h4 style="margin-top: 0; color: #856404;">What happens next?</h4>
                        <ol style="margin: 10px 0;">
                            <li>Our support team will review your inquiry</li>
                            <li>We'll investigate and prepare a response</li>
                            <li>You'll receive an email with our answer</li>
                        </ol>
                        <p style="margin: 10px 0 0 0;">
                            <strong>Urgent issue?</strong> Call our support hotline for immediate assistance.
                        </p>
                    </div>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <p style="font-size: 0.9em; color: #7f8c8d;">
                        Thank you for your patience.<br>
                        <strong>Medical Diagnosis System Support Team</strong>
                    </p>
                </div>
            </body>
        </html>
        """
        
        return EmailService.send_email(subject, email, body, html)
    
    @staticmethod
    def send_help_reply_notification(email: str, name: str, 
                                     question: str, response: str) -> bool:
  
        subject = "Your Question Has Been Answered - Medical Diagnosis System"
        
        body = f"""Hello {name},

Thank you for your patience!

Your Question:
{question}

Our Response:
{response}

If you have any follow-up questions or if this didn't fully address your concern, please don't hesitate to reach out again.

We're here to help!

Best regards,
Medical Diagnosis System Support Team
"""
        
        html = f"""
        <html>
        <head>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
            </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2 style="color: #2c3e50;">Your Question Has Been Answered! <i class="fa-regular fa-message"></i></h2>
                    
                    <p>Hello <strong>{name}</strong>,</p>
                    
                    <p>Thank you for your patience! We've reviewed your inquiry and prepared a response.</p>
                    
                    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h4 style="margin-top: 0; color: #1976d2;"><i class="fa-solid fa-question" style="color: #cd0a0a;"></i> Your Question:</h4>
                        <p style="margin: 10px 0; font-style: italic;">"{question}"</p>
                    </div>
                    
                    <div style="background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h4 style="margin-top: 0; color: #2e7d32;"><i class="fa-solid fa-question" style="color: #cd0a0a;"></i> Our Response:</h4>
                        <p style="margin: 10px 0;">{response}</p>
                    </div>
                    
                    <div style="background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0; text-align: center;">
                        <p style="margin: 0;">
                            <strong>Still need help?</strong><br>
                            Don't hesitate to reach out again. We're here to help!
                        </p>
                    </div>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <p style="font-size: 0.9em; color: #7f8c8d;">
                        We're here to help!<br>
                        <strong>Medical Diagnosis System Support Team</strong>
                    </p>
                </div>
            </body>
        </html>
        """
        
        return EmailService.send_email(subject, email, body, html)


# Convenience functions for backward compatibility
def send_email_notification(to_email: str, name: str, 
                           diagnosis: str, description: str) -> bool:
    """Backward compatible diagnosis notification function"""
    return EmailService.send_diagnosis_notification(to_email, name, diagnosis, description)


def send_appointment_notification(to_email: str, name: str, 
                                  day: str, time: str) -> bool:
    """Backward compatible appointment notification function"""
    return EmailService.send_appointment_notification(to_email, name, day, time)


def send_registration_notification(to_email: str, fname: str) -> bool:
    """Backward compatible registration notification function"""
    return EmailService.send_registration_notification(to_email, fname)


def send_login_notification(to_email: str, username: str) -> bool:
    """Backward compatible login notification function"""
    return EmailService.send_login_notification(to_email, username)


def send_help_notification(to_email: str, names: str) -> bool:
    """Backward compatible help notification function"""
    return EmailService.send_help_notification(to_email, names)

def send_diagnosis_notification(to_email: str, names: str,diagnosis: str, description: str) -> bool:
    """Backward compatible help notification function"""
    return EmailService.send_diagnosis_notification(to_email, names,diagnosis, description)


def send_helpReply_notification(to_email: str, names: str, 
                                response: str, question: str) -> bool:
    """Backward compatible help reply notification function"""
    return EmailService.send_help_reply_notification(to_email, names, question, response)


def send_doctor_notification(to_email: str, name: str, specialty: str, 
                            day: str, password: str) -> bool:
    """Backward compatible doctor notification function"""
    return EmailService.send_doctor_notification(to_email, name, specialty, day, password)



def send_help_notification(to_email, names):
    try:
        subject = "HELP Notification"
        body = f"Hello {names},\n\nYour Question was received successfully. We usually answer back in less than 48 hours."
        msg = Message(subject, recipients=[to_email], body=body)
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as err:
        flash(f"Email Sending Error:{str(err)}","error")