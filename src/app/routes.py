'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Student: Artemis W., Faye G., Nikki Z., Jess C., Yasir F.
Description: Project 1 - GPA Calculator
'''

from app import app, db
from app.models import User, Course, Enrollment
from app.forms import SignUpForm, LoginForm, EnrollmentForm, DeleteEnrollmentForm, UpdateGradeForm
# TODO
# from gpa_calculator_xx import calculate_gpa
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')

# TODO: from hwk-3
@app.route('/users/signup', methods=['GET', 'POST'])
def signup():
    return "Work in progress..."
    
# TODO: from hwk-3
@app.route('/users/login', methods=['GET', 'POST'])
def login():
    return "Work in progress..."

# TODO: from hwk-3
@app.route('/users/signout', methods=['GET', 'POST'])
def signout():
    return "Work in progress..."

# TODO
@app.route('/enrollments')
@login_required
def list_enrollments():
        enroll = User.query.all()
        return render_template('enrollments.html', enroll=enroll)

# TODO
@app.route('/enrollments/delete/<course_prefix>/<course_number>', methods=['POST'])
@login_required
def delete_enrollment(course_prefix, course_number):
    return "Work in progress..."

# TODO
@app.route('/enrollments/create', methods=['GET', 'POST'])
@login_required
def create_enrollment():
    form = EnrollmentForm()
    if form.validate_on_submit():
        new_enrollment = Enrollment(
            user_id=current_user.id,
            course_prefix=form.course_prefix.data, 
            course_number=form.course_number.data
        )
        db.session.add(new_enrollment)
        db.session.commit()
        return redirect(url_for('list_enrollments'))
        
    return render_template('create_enrollment.html', form=form)

@app.route('/enrollments/update/<course_prefix>/<course_number>', methods=['GET', 'POST'])
@login_required
def update_enrollment(course_prefix, course_number):
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_prefix=course_prefix, course_number=course_number).first_or_404()
    form = UpdateGradeForm(grade=enrollment.grade)
    if form.validate_on_submit():
        enrollment.grade = form.grade.data
        db.session.commit()
        return redirect(url_for('list_enrollments'))
    return render_template('update_enrollment.html', form=form, enrollment=enrollment)