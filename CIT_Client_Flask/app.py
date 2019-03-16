from flask import Flask, render_template, redirect, url_for, request, session, flash
import re
from Database.database_handler import DatabaseHandler

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/home')
def home():
    if session.get('logged_in') is None:
        return redirect(url_for('login'))
    username = session['username']
    group_id = session['group_id']

    group_info = DatabaseHandler.find('groups', group_id)
    print (group_info)

    platforms = group_info['platforms']
    print(platforms)
    team = group_info['members']
    print(team)

    return render_template('index.html', username=username, platforms=platforms, team=team, re=re)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = DatabaseHandler.find('users', request.form['username'])
        if user is None or user['password'] != request.form['password']:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['username'] = request.form['username']
            session['group_id'] = user['group_id']
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    session.pop('group_id', None)
    session.pop('logged_in', None)
    return redirect(url_for('index'))


# @app.route('/api/v1.0/platforms/<string:username>', methods=['GET', 'PUT'])
# def get_user_platforms(username):
#     print('In the get_user_platforms route')
#     if username == 'JaneD':
#         return jsonify({"Hackathon": "This is the hackathon page", "Rapid Cyber": "This is the rapid cyber page"})
#     else:
#         return jsonify({"Hackathon": "This is the hackathon page"})


if __name__ == '__main__':
    app.run()
