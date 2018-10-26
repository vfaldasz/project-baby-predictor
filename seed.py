from sqlalchemy import func
from model import User
from model import Project

from model import connect_to_db, db
from server import app
import datetime


def load_users_and_projects():

    """Create example data for the test database."""

    #User.query.delete()

    user1 = User(name= "Heather", email= "heather@gmail.com", password= "abc")
    user2 = User(name= "Virginia", email= "virginia@gmail.com", password= "abc")
    user3 = User(name= "Jonathan", email= "jonathan@gmail.com", password= "abc")
    user4 = User(name= "Jane", email= "jane@gmail.com", password= "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3")

    db.session.add_all([user1, user2, user3, user4])
    
    project1 = Project(mom_url = "project_1/111.jpg", dad_url= "project_1/222.jpg", baby_url= "project_1/result.png", user= user1)
    project2 = Project(mom_url = "project_2/444.jpg", dad_url= "project_2/555.jpg", baby_url= "project_2/result.png", user= user2)
    project3 = Project(mom_url = "project_3/888.jpg", dad_url= "project_3/999.jpg", baby_url= "project_3/result.png", user= user3)
    project4 = Project(mom_url = "project_4/888.jpg", dad_url= "project_4/999.jpg", baby_url= "project_4/result.png", user= user4)

    db.session.add_all([project1, project2, project3, project4])
    

    db.session.commit()


def seed_data():
    load_users_and_projects()

if __name__ == "__main__":
    from flask import Flask 
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to DB.")
    seed_data()



