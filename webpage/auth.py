from flask import Blueprint
from flask import render_template, redirect, request, flash, url_for
from webpage import DB_NAME
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
   if request.method=='POST':
      u_email = request.form.get('email')
      pwd = request.form.get('password')

      user=User.query.filter_by(email=u_email).first()
      print (user)
      if user:
            if check_password_hash(user.password, pwd):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))       
            else:
               flash('Incorrect password, Please try again.', category='error')
      else:
         flash('Please enter your login credentials.',category='error')

   return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        u_email = request.form.get('email')
        f_name = request.form.get('fname')
        l_name = request.form.get('lname')
        contact = request.form.get('contact')
        pwd = request.form.get('password')
        cnf_pwd = request.form.get('cnfpassword')

        user = User.query.filter_by(email=u_email).first()

        if user:
            flash('User email already exists.', category='error')
        elif len(u_email)<4:
            flash('Email should have atleast 4 characters.', category='error')
        elif len(f_name)<3:
            flash('First Name should have atleast 3 characters.', category='error')
        elif len(l_name)<2:
            flash('Last Name should have atleast 2 characters.', category='error')
        elif len(contact)!=10:
            flash('Contact must have 10 numbers.', category='error')
        elif len(pwd) < 8:
            flash('Password should have atleast 8 characters.', category='error')
        elif pwd != cnf_pwd:
            flash('Confirm password doesn\'t match with the password.', category='error')
        else:
            new_user = User(first_name=f_name, last_name=l_name, email=u_email, contact=contact, password= generate_password_hash(pwd, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
           # login_user(user, remember=True)
            flash('User registered successfully!', category='success')
            return redirect(url_for('views.home')) 

    return render_template('signup.html', user=current_user)


   