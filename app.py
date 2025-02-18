
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'
users = {
    'admin': generate_password_hash(' ') #add password here
}

@app.route('/')
def index():
    return render_template('register.html') 
@app.route('/register', methods=['GET', 'POST'])
def register():
 if request.method == 'POST':
        try:
            username = request.form['username'].strip()
            password = request.form['password']

            if not (3 <= len(username) <= 20):
                flash('Username must be 3-20 characters')
                return redirect(url_for('register'))

            if username in users:
                flash('Username already exists')
                return redirect(url_for('register'))

            users[username] = generate_password_hash(password)
            return redirect(url_for('login'))
            
        except Exception as e:
            flash('Registration error')
            return redirect(url_for('register'))
            
 return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if "admin" in username.lower():
            if check_password_hash(users.get('admin', ''), password):
                return "Congrats! Here's your flag: CTF_FLAG{login_bypass_success}"
            return "Hint: "
        if username in users:
            if check_password_hash(users[username], password):
                return f"Welcome {username}!"
            else:
                flash('Invalid credentials')
                return redirect(url_for('login'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))

    return render_template('ctf1.html')
if __name__ == '__main__':
    app.run(debug=False)