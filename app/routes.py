from app import app, db
from flask import render_template, url_for
from app.database import Clients

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/base')
def base():
    print(url_for('base'))
    return render_template('base.html')

@app.route('/nav')
def nav():
    print(url_for('base'))
    return render_template('navbar.html')

@app.route('/user')
def actors():
    clients = Clients.query.all()
    return render_template('clients.html', clients=clients)
