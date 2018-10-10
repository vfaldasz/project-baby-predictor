"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of photos website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(25), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    # photo_id = db.Column(db.Integer,db.ForeignKey('photos.photo_id'))

    #Define relationship to photo (not needed. extra)
    photos = db.relationship('Photo')

    projects = db.relationship('Project')


    """Provide helpful representation when printed."""
    def __repr__(self):

        return "<User user_id={} name={} email={} password={}>".format(self.user_id, self.name, self.email, self.password)


class Photo(db.Model):

    __tablename__ = "photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tag = db.Column(db.String(25), nullable=True)
    url = db.Column(db.String(64), nullable=True)
    project_id = db.Column(db.Integer,db.ForeignKey('projects.project_id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    

    #Define relationship to user
    user = db.relationship('User')
    project = db.relationship('Project')
    
    """Provide helpful representation when printed."""
    def __repr__(self):

        return "<Photo photo_id={} tag={} url={} project_id={} user_id={}>".format(self.photo_id, self.tag, self.url, self.project_id, self.user_id)

class Project(db.Model):

    __tablename__ = "projects"

    project_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))

    #Define relationship to user
    user = db.relationship('User')
    
    
    """Provide helpful representation when printed."""
    def __repr__(self):

        return "<Photo project_id={} user_id={}>".format(self.project_id, self.user_id)



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///babies'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
