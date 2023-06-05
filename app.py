from flask import Flask, render_template, url_for
from database.db import Clients,session,engine


app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/base')
def base():
    print(url_for('base'))
    return render_template('base.html')

@app.route('/user')
def actors():
    clients = session.query(Clients).all()
    return render_template('clients.html', clients=clients)

# @app.route('/base')
# def base():
#     return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
