from flask.ext.sqlalchemy import SQLAlchemy
from GPIOConfig import dbSchema,dbHost,dbPass,dbUser

db = SQLAlchemy()
db.create_engine('mysql://{0}:{1}@{2}/{3}'.format(dbUser,dbPass,dbHost,dbSchema))

#...

class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'UserRecords'

    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    sessionId = db.Column(db.String)
    active = db.Column(db.Boolean, default=True)

    def is_active(self):
        """True, as all users are active."""
        return self.active

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
