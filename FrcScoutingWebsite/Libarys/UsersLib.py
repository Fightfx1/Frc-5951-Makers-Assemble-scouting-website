from FrcScoutingWebsite import db
from sqlalchemy.ext.hybrid import hybrid_property
import bcrypt

class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String,nullable=False)
    authenticated = db.Column(db.Boolean, default=False, nullable=False)
    role = db.Column(db.String , default="Queen" , nullable=False)

    def get_role(self):
        return self.role

    def is_admin(self):
        return self.role == 'Admin' and self.authenticated

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False