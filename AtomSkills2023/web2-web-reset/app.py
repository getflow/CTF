from flask import Flask, render_template, request, session, redirect
import sqlite3
import uuid
import random

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

conn = sqlite3.connect('database.db')
conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, info TEXT,reset_code int)')
conn.close()


@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'], info=session['info'])
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT info FROM users WHERE username = ?", (username,))
            info = cursor.fetchone()[0]
            conn.close()

            session['username'] = username
            session['info'] = info
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, info) VALUES (?, ?, ?)",
                           (username, password, 'New User'))
            conn.commit()
            cursor.execute("SELECT info FROM users WHERE username = ?", (username,))
            info = cursor.fetchone()[0]
            conn.close()

            session['username'] = username
            session['info'] = info
            return redirect('/')
        else:
            return render_template('register.html', error='User already registered')

    return render_template('register.html')


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        username = request.form['username']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user:
            reset_code = random.randint(10000, 99999)
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET reset_code = ? WHERE username = ?", (reset_code, username))
            conn.commit()
            conn.close()

            session['username'] = username
            return redirect('/confirm')
        else:
            return render_template('reset.html', error='User is not found')

    return render_template('reset.html')


@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    if request.method == 'POST':
        code = request.form['code']
        username = request.form['username']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT reset_code FROM users WHERE username = ?", (username,))
        reset_code = cursor.fetchone()[0]
        conn.close()

        if int(reset_code) == int(code):
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT info FROM users WHERE username = ?", (username,))
            info = cursor.fetchone()[0]
            conn.close()

            session['username'] = username
            session['info'] = info
            return redirect('/')
        else:
            return render_template('confirm.html', username=session['username'], error='Password recovery error')

    return render_template('confirm.html', username=session['username'])


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run()
