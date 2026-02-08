from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"   # For sessions

# ---------------------- DATABASE CONNECTION ----------------------
try:
    db = mysql.connector.connect(
        host="localhost",     # ✅ Use localhost or 127.0.0.1
        user="root",          # ✅ Replace if your MySQL username is different
        password="",          # ✅ Enter your MySQL password here (if any)
        database="flask_login_db"
    )
    cursor = db.cursor(dictionary=True)
    print("✅ Database connected successfully!")
except mysql.connector.Error as err:
    print(f"❌ Database connection failed: {err}")

# ---------------------- ROUTES ----------------------

@app.route('/')
def home():
    return redirect(url_for('signup'))

# --- Signup Route ---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            return render_template('signup.html', error="Username already exists!")

        # Insert new user into database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return redirect(url_for('login'))

    return render_template('signup.html')


# --- Login Route ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            session['user'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password!")

    return render_template('login.html')


# --- Dashboard Route ---
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', username=session['user'])
    return redirect(url_for('login'))


# --- Logout Route ---
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
