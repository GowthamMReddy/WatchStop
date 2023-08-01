import base64
from flask import Blueprint, jsonify
from flask import render_template, redirect, request, flash, url_for, current_app
from flask_login import login_required, current_user
from .models import User, Watches, Orders
from . import db
import os
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField
from wtforms.validators import DataRequired
import requests
import json

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    watches= Watches.query.all()
    return render_template("home.html", user=current_user, watches=watches)

@views.route('/admin', methods=['GET','POST'])
@login_required
def admin():
    id = current_user.id
    if id == 1:
         print('hello1')
         if request.method == 'POST':
              print('hello')
              if 'watch_img' not in request.files:
                flash('No image file selected',category='error')
                return redirect(url_for('views.admin'))
              watch_img=request.files['watch_img']
              image_data=watch_img.read()
              image_name=watch_img.filename
              if image_name=='':
                flash('No image file selected',category='error')
                return redirect(url_for('views.admin'))

              watch_mid = request.form.get('watch_mid')
              watch_name = request.form.get('watch_name')
              watch_type = request.form.get('watch_type')
              watch_price = request.form.get('watch_price')

              watch_modelid = Watches.query.filter_by(watch_mid=watch_mid).first()
        
              if watch_modelid:
                flash('Watch model Id already exists.', category='error')
              elif len(watch_name)<4:
                flash('Watch name should have atleast 4 characters.', category='error')
              elif watch_type=='':
                flash('Watch type shouldn\'t be blank', category='error')
              elif watch_price=='':
                flash('Watch price  shouldn\'t be blank', category='error')
       
              else:
                new_watch = Watches(watch_mid=watch_mid,watch_name=watch_name,watch_type=watch_type,watch_price=watch_price,img=image_data,img_name=image_name)
                db.session.add(new_watch)
                db.session.commit()
                flash('New Watch is added successfully!', category='success')
                return redirect(url_for('views.admin'))
         watches= Watches.query.all()
         return render_template("admin.html", user=current_user, watches=watches )
    else: 
      flash("You don't have required privilleges to access admin page")
      return render_template('home.html')
    


@views.route('/proddesc/<int:id>', methods=['GET', 'POST'])
@login_required
def proddesc(id):
    
    watch = Watches.query.get(id)
    watch.img = base64.b64encode(watch.img).decode('utf-8')

    return render_template('proddesc.html', user=current_user, watch=watch)

@views.route('/pay',methods=['GET','POST'])
@login_required
def pay():
   flash("Your payment is successful!")
   return render_template("success.html", user=current_user)

@views.route('/homescreen',methods=['GET','POST'])
@login_required
def homescreen():
    watches= Watches.query.all()
    return redirect(url_for('views.home')) 
    
    
    
 