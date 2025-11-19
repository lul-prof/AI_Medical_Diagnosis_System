from flask import Flask, request , render_template, request, url_for, session, redirect, flash,Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Question, Response, Appointment, BookedAppointment
from app.services.email_service import  EmailService, send_help_notification



main = Blueprint('main', __name__, url_prefix='/')






@main.route('/')
def index():
    return render_template('general/home.html')


@main.route('/developer')
def developer():
    return render_template('general/developer.html')



@main.route('/location')
def location():
    return render_template('general/locations.html')



@main.route('/contacts')
def contacts():
    return render_template('general/contacts.html')


@main.route('/help')
def help():
    return render_template('general/help.html')



@main.route('/appointment', methods=['GET','POST'])
def book_appointment():
    if request.method=='POST':
        try:
            name=request.form.get('name')
            contact=request.form.get('contact')
            email=request.form.get('email')
            specialty=request.form.get('specialty')
            day=request.form.get('day')
            
            appointment = Appointment(
                name=name,
                email=email,
                contact=contact,
                specialty=specialty,
                day=day
            )
            
            db.session.add(appointment)
            db.session.commit()

            flash("Appointment Queued for Verification successfully. Check your email after 2hrs","success")


        except Exception as err:
            flash(f"Check:{str(err)}","error")

            
    return render_template('general/contacts.html')


@main.route('/problem', methods=['GET','POST'])
def problem():
    try:
        if request.method=='POST':
            names=request.form.get('name')
            email=request.form.get('email')
            contact=request.form.get('contact')
            question=request.form.get('problem')

            
            quiz = Question(
                names=names,
                email=email,
                contact=contact,
                question=question
            )
            
            db.session.add(quiz)
            db.session.commit()

            flash("Question Received. We will respond soon!!!","success")

            send_help_notification(email, names)
            if send_help_notification(email, names):
                flash("Help Message send to your email successfully","success")
            else:
                flash("Error Sending Email. Check:","error")

    except Exception as e:
        flash(f"Check:{str(e)}","error")


    return render_template('general/help.html')  


@main.route('/responses')
def responses():
    responses = []
    try:
        responses = Response.query.all()
        responses = [
            {
                'id': r.id,
                'user': r.user,
                'question': r.question,
                'response': r.response
            }
            for r in responses
        ]

    except Exception as err:
        flash(f"Check {err}", "error")
    
    return render_template('general/responses.html', responses=responses)



