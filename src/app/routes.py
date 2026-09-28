'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Student: Artemis W., Faye G., Nikki Z., Jess C., Yasir F.
Description: Project 1 - GPA Calculator
'''

from app import app, db
from app.models import User, Course, Enrollment
from app.forms import SignUpForm, LoginForm, EnrollmentForm, DeleteEnrollmentForm
from gpacgo_lib import calculate_gpa
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')

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
    
@app.route('/users/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        
        if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd):
            login_user(user)
            return redirect(url_for('list_enrollments'))
            
    return render_template('login.html', form=form)

@app.route('/users/signout', methods=['GET', 'POST'])
def signout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/enrollments')
@login_required
def list_enrollments():
    current_id = current_user.id
    enroll = Enrollment.query.filter(Enrollment.user_id == current_id).all()
    
    gpa = calculate_gpa(enroll)
    
    delete_form = DeleteEnrollmentForm()
    
    return render_template(
        'enrollments.html', 
        enrollments=enroll, 
        gpa=gpa, 
        delete_form=delete_form
    )

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


@app.route('/enrollments/create', methods=['GET', 'POST'])
@login_required
def create_enrollment():
    form = EnrollmentForm()
    courses = Course.query.all()
    form.course.choices = [
        (f"{c.prefix} {c.number}", f"{c.prefix} {c.number} - {c.name}") 
        for c in courses
    ]
    
    if form.validate_on_submit():
        prefix, number = form.course.data.split(' ', 1)
        new_enrollment = Enrollment(
            user_id=current_user.id,
            course_prefix=prefix,
            course_number=number,
            grade=form.grade.data
        )
        db.session.add(new_enrollment)
        db.session.commit()
        return redirect(url_for('list_enrollments'))
        
    return render_template('create_enrollment.html', form=form)