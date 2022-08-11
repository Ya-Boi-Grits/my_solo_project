from pydoc import resolve
from flask_app.models.achievement import Achievement
from flask_app.models.user import User
from flask import render_template, redirect, request, session, jsonify
import requests
import json
import os
from flask_app import newsapi
from newsapi import NewsApiClient
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

####### Visible Routes #######


@app.route('/landing')
def landing_page():
    return render_template('login.html')


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/dashboard')
def view_dashboard():
    if 'user_id' not in session:
        redirect('/landing')
    top_headlines = newsapi.get_top_headlines(q='finance',category='business',language='en',country='us')
    return render_template('dashboard.html', all_achievements=Achievement.get_all_achievements_from_db(), top_headlines=top_headlines)


####### Hidden Routes #######


@app.route('/')
def redirect_to_landing():
    return redirect('/landing')


@app.route('/process_registration', methods=['POST'])
def process_registration():
    if not User.validate_registration(request.form):
        return redirect('/register')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": hashed_pw
    }
    session['user_id'] = User.register_user(data)
    more_data = {
        "id": session['user_id']
    }
    this_user = User.select_user(more_data)
    session['first_name'] = this_user.first_name
    session['first_name'] = this_user.first_name
    session['last_name'] = this_user.last_name
    session['email'] = this_user.email
    return redirect('/dashboard')


@app.route('/process_login', methods=['POST'])
def process_login():
    user_found = User.validate_login(request.form)
    if user_found == False:
        return redirect('/landing')
    session['user_id'] = user_found.id
    session['first_name'] = user_found.first_name
    session['last_name'] = user_found.last_name
    session['email'] = user_found.email
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/landing')
