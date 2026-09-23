'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Student(s):
Description: Project 1 - GPA Calculator
'''

from app import app, db
from app.models import Course

# TODO
courses = [ 
    ("CS","3250","SW Dev Methods and Tools",4),
    ("GWS","1200","Sexuality, Race, and Power",3),
    ("JMP","2610","Intro to Technical Writing",3),
    ("MTH","3130","Applied Methods in Linear Algebra",4),
    ("PHI","3370","Computers, Ethics, and Society",3)
]


with app.app_context():
    for prefix, number, name, credits in courses:
        new_course = Course(prefix=prefix, number=number, name=name, credits=credits)
        db.session.add(new_course)
    db.session.commit()
    print(f'Loaded {len(courses)} courses.')
