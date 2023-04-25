from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))



class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(10))
    name = db.Column(db.String(20))
    mobile = db.Column(db.String(10))
    nationality = db.Column(db.String(20))
    department = db.Column(db.String(20))
    position = db.Column(db.String(20))
    team = db.Column(db.String(20))
    sport = db.Column(db.String(250))
    image = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Person {}>'.format(self.name)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)