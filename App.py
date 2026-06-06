from Auth import *
from CRUD import *
from flask import Flask, request, session, redirect, render_template, jsonify
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'a-safe-local-development-key')

@app.route('/')
def identification():
    if session.get('user_id') is not None:
        print(session.get('access'))
        return redirect('/db')

    return ('''
    <form method="POST">
        <H1>Login Details</H1>
        <input name="user_id" pattern="[a-zA-Z0-9]+" required></input>
        <input name="password" required"></input>
        <button type="submit" formaction="/login">Login</button>
        <button type="submit" formaction="/signup">Sign Up</button>
    </form>
    ''')

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form.get('user_id')
    password = request.form.get('password')
    if account_exists(user_id,password):
        session['access']=get_access(user_id)
        session['user_id'] = user_id
        session.permanent = False
        return redirect('/db')
    else:
        return '<p>login failed</p>'

@app.route('/signup', methods=['POST'])
def signup():
    user_id = request.form.get('user_id').lower()
    password = request.form.get('password')
    if userid_exists(user_id):
        return '<p>user already exists</p>'
    else:
        new_account(user_id,password)
        return '<p>user created successfully</p>'
@app.route('/db')
def db():
    if session.get('user_id') is not None:
        data=get_all()
        access=get_access(session['user_id'])
        if access is not None and access[0] =='TEACHER':
            return render_template('teacher.html',data=data)
        return render_template('student.html',data=data)
    else:
        return redirect('/')
@app.route('/db/<command>', methods=['POST'])
def dbGet(command):
    outcome = command.split(',')
    if outcome[0]=='insert':
        name=outcome[1]
        grade=outcome[2]
        insert(name,grade)
    elif outcome[0]=='update':
        id=outcome[1]
        grade=outcome[2]
        update(id,grade)
    elif outcome[0]=='delete':
        id=outcome[1]
        delete(id)
    return redirect('/db')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)