from sqlalchemy import func
from model import User
from model import Project

from model import connect_to_db, db
from server import app
import datetime


def load_users_and_projects():

    """Create example data for the test database."""

    User.query.delete()

    user1 = User(name= "Heather", email= "heather@gmail.com", password= "abc")
    user2 = User(name= "Virginia", email= "virginia@gmail.com", password= "abc")
    user3 = User(name= "Jonathan", email= "jonathan@gmail.com", password= "abc")

    db.session.add_all([user1, user2, user3])
    
    project1 = Project(mom_url = "111", dad_url= "222", baby_url= "333", user= user1)
    project2 = Project(mom_url = "444", dad_url= "555", baby_url= "777", user= user2)
    project3 = Project(mom_url = "888", dad_url= "999", baby_url= "000", user= user3)

    db.session.add_all([project1, project2, project3])
    

    db.session.commit()


def seed_data():
    load_users_and_projects()

if __name__ == "__main__":
    from flask import Flask 
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to DB.")
    seed_data()



