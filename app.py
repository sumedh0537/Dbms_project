from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import IntegrityError

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for sessions

# Database connection setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pass@123",
    database="jobportal"
)
cursor = db.cursor()

@app.route('/delete_skill', methods=['POST'])
def delete_skill():
    skill = request.form['skill']
    user_id = session.get('user_id')

    if user_id:
        cursor.execute("DELETE FROM skills WHERE user_id=%s AND skill=%s", (user_id, skill))
        db.commit()
        return redirect(url_for('skills'))  # Redirect to skills page after deleting
    else:
        return "You need to log in to delete skills."
    
@app.route('/my_applications')
def my_applications():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    user_id = session['user_id']
    cursor.execute("SELECT a.id, c.name, a.application_status FROM applications a JOIN companies c ON a.company_id = c.id WHERE a.user_id = %s", (user_id,))
    applications = cursor.fetchall()

    return render_template('my_applications.html', applications=applications)

@app.route('/delete_application/<int:application_id>', methods=['POST'])
def delete_application(application_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    cursor.execute("DELETE FROM applications WHERE id = %s", (application_id,))
    db.commit()
    return redirect(url_for('my_applications'))  # Redirect back to the applications page

@app.route('/apply/<int:company_id>', methods=['POST'], endpoint='apply_company')
def apply(company_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    user_id = session['user_id']
    
    # Check if the user has already applied to this company
    cursor.execute("SELECT * FROM applications WHERE user_id = %s AND company_id = %s", (user_id, company_id))
    existing_application = cursor.fetchone()  # Fetch the result to avoid unread result error

    if existing_application:
        return "You have already applied to this company."  # Or redirect with a message

    cursor.execute("INSERT INTO applications (user_id, company_id) VALUES (%s, %s)", (user_id, company_id))
    db.commit()
    return redirect(url_for('companies'))  # Redirect back to companies page

@app.route('/')
def home():
    if 'user' in session:
        return render_template('index.html', username=session['user'])
    return render_template('index.html', username=None)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form.get('confirm-password')

        if password != confirm_password:
            return "Passwords do not match!"

        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                           (name, email, password))
            db.commit()
            session['user'] = name  # Set session after signup
            return redirect(url_for('home'))  # Redirect to home after signup
        except IntegrityError:
            return redirect(url_for('signup', error="Email already exists!"))  # Redirect with error message

    error_message = request.args.get('error')  # Get error message from URL
    return render_template('signup.html', error=error_message) 

@app.route('/skills', methods=['GET', 'POST'])
def skills():
    if request.method == 'POST':
        skill = request.form['skill']
        user_id = session.get('user_id')

        if user_id:
            cursor.execute("INSERT INTO skills (user_id, skill) VALUES (%s, %s)", (user_id, skill))
            db.commit()
            return redirect(url_for('skills'))  # Redirect to skills page after adding
        else:
            return "You need to log in to add skills."

    # Fetch existing skills for the logged-in user
    user_id = session.get('user_id')
    skills = []
    if user_id:
        cursor.execute("SELECT skill FROM skills WHERE user_id=%s", (user_id,))
        skills = cursor.fetchall()

    return render_template('skills.html', skills=skills)


@app.route('/companies')
def companies():
    print("Companies route accessed")  # Debugging line
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    return render_template('companies.html', companies=companies)

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    user_id = session['user_id']
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        try:
            # Update the user's name and email in the database
            cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, user_id))
            db.commit()  # Commit the changes to the database
            return redirect(url_for('home'))  # Redirect to home after updating
        except Exception as e:
            return str(e)  # Return error message if something goes wrong

    return render_template('update_profile.html', user=user)  # Render the form for updating the profile


@app.route('/apply/<int:company_id>', methods=['POST'])
def apply(company_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    user_id = session['user_id']
    cursor.execute("INSERT INTO applications (user_id, company_id) VALUES (%s, %s)", (user_id, company_id))
    db.commit()
    return redirect(url_for('companies'))  # Redirect back to companies page


@app.route('/update_skill', methods=['POST'])
def update_skill():
    old_skill = request.form['old_skill']
    new_skill = request.form['new_skill']
    user_id = session.get('user_id')

    if user_id:
        cursor.execute("UPDATE skills SET skill=%s WHERE user_id=%s AND skill=%s", (new_skill, user_id, old_skill))
        db.commit()
        return redirect(url_for('skills'))  # Redirect to skills page after updating
    else:
        return "You need to log in to update skills."

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT id, name FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]  # Store user ID in session
            session['user'] = user[1]  # Store user name in session
            return redirect(url_for('home'))
        else:
            return "Invalid email or password!"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

