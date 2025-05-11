# ---------------------------------------------------------------------------- #
# Imports
# ---------------------------------------------------------------------------- #
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect  # Security: CSRF protection
import logging
from logging import Formatter, FileHandler
from forms import LoginForm, RegisterForm, ForgotForm  # Explicit imports
from os import environ  # Security: Load env vars safely


# ---------------------------------------------------------------------------- #
# App Config
# ---------------------------------------------------------------------------- #
app = Flask(__name__)
app.config.from_object('config')

# Security: Enforce CSRF protection
csrf = CSRFProtect(app)

# Security: Ensure SECRET_KEY is set via environment variable
if not app.config.get('SECRET_KEY'):
    raise ValueError("SECRET_KEY not set in config or environment variables.")


# ---------------------------------------------------------------------------- #
# Controllers
# ---------------------------------------------------------------------------- #
@app.route('/')
def home():
    """Homepage route."""
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    """About page route."""
    return render_template('pages/placeholder.about.html')


@app.route('/login')
def login():
    """Login page route."""
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    """Registration page route."""
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    """Password reset page route."""
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


# ---------------------------------------------------------------------------- #
# Error Handlers
# ---------------------------------------------------------------------------- #
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('errors/500.html'), 500


# ---------------------------------------------------------------------------- #
# Logging (Security: Avoid logging sensitive data)
# ---------------------------------------------------------------------------- #
if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        )
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('App started')


# ---------------------------------------------------------------------------- #
# Launch
# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
    # Security: Disable debug mode in production
    debug_mode = environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
