# ---------------------------------------------------------------------------- #
# Imports
# ---------------------------------------------------------------------------- #
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
import logging
from logging import Formatter, FileHandler
from forms import LoginForm, RegisterForm, ForgotForm
from os import environ
from werkzeug.security import generate_password_hash  # Security: Password hashing


# ---------------------------------------------------------------------------- #
# App Config (Security: Load SECRET_KEY from env)
# ---------------------------------------------------------------------------- #
app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')  # From environment variables

if not app.config['SECRET_KEY']:
    raise RuntimeError("SECRET_KEY not set in environment variables")

csrf = CSRFProtect(app)  # Enable CSRF protection


# ---------------------------------------------------------------------------- #
# Controllers
# ---------------------------------------------------------------------------- #
@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        # Security: Never hardcode passwords (Bandit B105)
        stored_password_hash = environ.get('ADMIN_PASSWORD_HASH')  # Pre-hashed
        input_password = form.password.data
        if stored_password_hash and check_password_hash(stored_password_hash, input_password):
            return "Login successful"
    return render_template('forms/login.html', form=form)


# ---------------------------------------------------------------------------- #
# Error Handlers
# ---------------------------------------------------------------------------- #
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


# ---------------------------------------------------------------------------- #
# Logging (Security: Sanitize logs)
# ---------------------------------------------------------------------------- #
if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    app.logger.addHandler(file_handler)


# ---------------------------------------------------------------------------- #
# Launch
# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
    app.run(debug=environ.get('FLASK_DEBUG', 'false').lower() == 'true')
