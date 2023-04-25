import os
from flask import render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
from app import app, db
from app.forms import *
import imghdr
from app.models import User, Person
from flask_login import current_user, login_user, logout_user, login_required
from flask_wtf import CSRFProtect
from app.forms import RegistrationForm

csrf = CSRFProtect(app)


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    formatt = imghdr.what(None, header)
    if not formatt:
        return None
    return '.' + (formatt if formatt != 'jpeg' else 'jpg')

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Roman'}
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/all_persons')
def get_all_persons():
    a_persons = db.session.scalars(db.select(Person)).all()
    return render_template('all_persons.html', title='All Persons', persons=a_persons)


@app.route("/person-by-id/<int:person_id>")
def get_person_by_id(person_id):
    a_person = db.get_or_404(Person, person_id)
    return render_template("person_by_id.html", person=a_person)


@app.route("/add_person", methods=["POST", "GET"])
def add_person():
    form = AddPersonForm()
    new_person = Person()
    if form.validate_on_submit():
        new_person.group = form.group.data
        new_person.name = form.name.data
        new_person.mobile = form.mobile.data
        new_person.nationality = form.nationality.data
        new_person.department = form.department.data
        new_person.position = form.position.data
        new_person.team = form.team.data
        new_person.sport = form.sport.data
        image = form.image.data
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        print(f"{image_path}")
        # file_ext = os.path.splitext(filename)[1]
        # if file_ext != validate_image(image.stream):
        #     return "Invalid image", 400
        image.save(image_path)
        new_person.image = image_path
        print(new_person.image)
        db.session.add(new_person)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("add_person.html", form=form, person=new_person)



# @app.route("/user-by-username/<username>")
# def user_by_username(username):
#     user = db.one_or_404(db.select(AlWaslPerson).filter_by(username=username), description=f"No user named '{username}'.")
#     return render_template("show_user.html", user=user)


# To update data, modify attributes on the model objects:
#
# user.verified = True
# db.session.commit()

# To delete data, pass the model object to db.session.delete():
#
# db.session.delete(user)
# db.session.commit()

