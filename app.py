from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

def get_db_connection():
    conn = sqlite3.connect('Vaccination Tracker.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('home.html', email=session.get('email'), firstname=session.get('firstname'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Parents WHERE Email = ?', (email,))
        account = cursor.fetchone()
        conn.close()
        if account and check_password_hash(account['Password'], password):
            session['loggedin'] = True
            session['id'] = account['ParentID']
            session['email'] = account['Email']
            session['firstname'] = account['Firstname']
            return redirect(url_for('tracker'))
        else:
            flash('Incorrect email/password!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = generate_password_hash(request.form['password'])
        phone = request.form['phone']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Parents WHERE Email = ?', (email,))
        account = cursor.fetchone()
        
        if account:
            flash('Account already exists!')
        else:
            cursor.execute('INSERT INTO Parents (FirstName, LastName, Email, Password, PhoneNumber) VALUES (?, ?, ?, ?, ?)',
                           (firstname, lastname, email, password, phone))
            conn.commit()
            flash('You have successfully registered! Please login.')
            return redirect(url_for('login'))
        
        cursor.close()
        conn.close()
    return render_template('register.html')

@app.route('/add_child', methods=['GET', 'POST'])
def add_child():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        child_firstname = request.form['child_firstname']
        child_lastname = request.form['child_lastname']
        child_dob = request.form['child_dob']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Children (ParentID, FirstName, LastName, DateOfBirth) VALUES (?, ?, ?, ?)',
                       (session['id'], child_firstname, child_lastname, datetime.strptime(child_dob, '%Y-%m-%d').date()))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Child added successfully!')
        return redirect(url_for('tracker'))
    
    return render_template('add_child.html')

@app.route('/tracker')
def tracker():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT ChildID, FirstName, LastName, DateOfBirth FROM Children WHERE ParentID = ?', (session['id'],))
    children = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('tracker.html', firstname=session.get('firstname'), children=children)

@app.route('/child_tracker/<int:child_id>')
def child_tracker(child_id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT FirstName, DateOfBirth FROM Children WHERE ChildID = ?', (child_id,))
    child = cursor.fetchone()

    today = datetime.now().date()
    Already_Done = []
    Upcoming = []

    dob = datetime.strptime(child['DateOfBirth'], '%Y-%m-%d').date()
    for age_recommended in range(72):  # Assuming a vaccination schedule within the first six years
        vaccine_due_date = dob + relativedelta(months=+age_recommended)
        cursor.execute('SELECT Name, Description, AgeEndRecommended FROM Vaccinations WHERE AgeRecommended = ?', (age_recommended,))
        vaccinations = cursor.fetchall()
        for vaccination in vaccinations:
            vaccine_name = vaccination['Name']
            description = vaccination['Description']
            age_end_recommended = vaccination['AgeEndRecommended']
            vaccine_end_date = dob + relativedelta(months=+age_end_recommended) if age_end_recommended else vaccine_due_date
            if vaccine_due_date < today:
                Already_Done.append({
                    'child_name': f"{child['FirstName']}",
                    'vaccine_name': vaccine_name,
                    'start_date': vaccine_due_date,
                    'desc': description
                })
            else:
                Upcoming.append({
                    'child_name': f"{child['FirstName']}",
                    'vaccine_name': vaccine_name,
                    'start_date': vaccine_due_date,
                    'end_date': vaccine_end_date,
                    'desc': description
                })

    cursor.close()
    conn.close()

    return render_template('child_tracker.html', firstname=session.get('firstname'), Already_Done=Already_Done, Upcoming=Upcoming, child=child)

if __name__ == '__main__':
    app.run(debug=True)
