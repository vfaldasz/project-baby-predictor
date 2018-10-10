from sqlalchemy import func
from model import User
from model import Photo
from model import Project

from model import connect_to_db, db
from server import app
import datetime


def load_users():

    """Create example data for the test database."""

    User.query.delete()

    user1 = User(name= "Heather", email= "heather@gmail.com", password= "abc")
    user2 = User(name= "Virginia", email= "virginia@gmail.com", password= "abc")
    user3 = User(name= "Jonathan", email= "jonathan@gmail.com", password= "abc")

    db.session.add_all([user1, user2, user3])
    
    project1 = Project(user= user1)
    project2 = Project(user= user2)
    project3 = Project(user= user3)

    db.session.add_all([project1, project2, project3])
    

    photo1 = Photo(tag= "dad", url= "xyz", project= project1, user= user1)
    photo2 = Photo(tag= "mom", url= "abc", project= project2, user= user2)
    photo3 = Photo(tag= "mom", url= "bcd", project= project3, user= user3)

    db.session.add_all([photo1, photo2, photo3])
    

    db.session.commit()


def seed_data():
    load_users()

if __name__ == "__main__":
    from flask import Flask 
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to DB.")
    seed_data()



