from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.decorators import doctor_required


records = Blueprint('records', __name__, url_prefix='/records')


@records.route('/dashboard')
def dashboard():
    
    return render_template('records/heartresults.html')