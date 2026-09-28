'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Student: Artemis W., Faye G., Nikki Z., Jess C., Yasir F.
Description: Project 1 - GPA Calculator
'''

from app import app, db
from app.models import User, Course, Enrollment
from app.forms import SignUpForm, LoginForm, EnrollmentForm, DeleteEnrollmentForm
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
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.hashpw(form.passwd.data.encode('utf-8'), bcrypt.gensalt())
        
        new_user = User(id=form.id.data, passwd=hashed_pw)
        
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
        
    return render_template('signup.html', form=form)
    
# TODO: from hwk-3
@app.route('/users/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        
        if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd):
            login_user(user)
            return redirect(url_for('list_enrollments'))
            
    return render_template('login.html', form=form)

# TODO: from hwk-3
@app.route('/users/signout', methods=['GET', 'POST'])
def signout():
    logout_user()
    return redirect(url_for('index'))

# TODO
@app.route('/enrollments')
@login_required
def list_enrollments():
        current_id = current_user.id
        enroll = Enrollment.query.filter(Enrollment.user_id == current_id)
        return render_template('enrollments.html', enrollment=enroll)

# TODO
@app.route('/enrollments/delete/<course_prefix>/<course_number>', methods=['POST'])
@login_required
def delete_enrollment(course_prefix, course_number):
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id, 
        course_prefix=course_prefix, 
        course_number=course_number
    ).first()
    
    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()
        
    return redirect(url_for('list_enrollments'))

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