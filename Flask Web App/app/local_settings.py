import os

# *****************************
# Environment specific settings
# *****************************
from .secrets_file import ADMIN_USERNAME, ADMIN_FULL_NAME, POSTGRESQL_DB_USER, POSTGRESQL_DB_NAME, POSTGRESQL_DB_PASS, POSTGRESQL_DB_HOST, POSTGRESQL_DB_PORT, API_KEY_SENDGRID, SMTP_MAIL_USERNAME, SMTP_MAIL_PASS
from .settings import APP_NAME
# DO NOT use "DEBUG = True" in production environments
DEBUG = True

# DO NOT use Unsecure Secrets in production environments
# Generate a safe one with:
#     python -c "import os; print repr(os.urandom(24));"
SECRET_KEY = 'This is an UNSECURE Secret. CHANGE THIS for production environments.'

# DB settings
POSTGRES = {
 'user': POSTGRESQL_DB_USER,
 'pw': POSTGRESQL_DB_PASS,
 'db': POSTGRESQL_DB_NAME, 
 'host': POSTGRESQL_DB_HOST,
 'port': POSTGRESQL_DB_PORT,
}

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids a SQLAlchemy Warning

# Flask-Mail settings
# For smtp.gmail.com to work, you MUST set "Allow less secure apps" to ON in Google Accounts.
# Change it in https://myaccount.google.com/security#connectedapps (near the bottom).
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_USERNAME = SMTP_MAIL_USERNAME
MAIL_PASSWORD = SMTP_MAIL_PASS

# Sendgrid settings
SENDGRID_API_KEY=API_KEY_SENDGRID

# Flask-User settings
USER_APP_NAME = APP_NAME
USER_EMAIL_SENDER_NAME = ADMIN_FULL_NAME
USER_EMAIL_SENDER_EMAIL = SMTP_MAIL_USERNAME

ADMINS = [
    '{admin} <{email}>'.format(admin=ADMIN_USERNAME, email=SMTP_MAIL_USERNAME),
    ]