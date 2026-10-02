'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Student(s): Artemis W., Faye G., Nikki Z., Jess C., Yasir F.
Description: Project 1 - GPA Calculator
'''

from flask import Flask
import os

''' Need this for Linux running (may cause issues on Windows (could be 'prj-1/instance' directory not being read))'''
base_dir = os.path.dirname(os.path.abspath( __file__))
root_dir = os.path.abspath(os.path.join(base_dir, '..', '..'))


app = Flask("GPA Calculator Web App",
            template_folder = os.path.join(root_dir, 'templates'),
            static_folder = os.path.join(root_dir, 'static'))

app.secret_key = 'You will never know!'
'''End of Linux running code'''

# db initialization
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prj1.db'
db.init_app(app)

from app import models
with app.app_context(): 
    db.create_all()

# login manager
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User

# user_loader callback
@login_manager.user_loader
def load_user(id):
    try: 
        return db.session.query(User).filter(User.id==id).one()
    except: 
        return None

from app import routes