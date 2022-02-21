import os

# *****************************
# Environment specific settings
# *****************************

# DO NOT use "DEBUG = True" in production environments
DEBUG = True

SESSION_TYPE = "filesystem"
# DO NOT use Unsecure Secrets in production environments
# Generate a safe one with:
#     python -c "import os; print repr(os.urandom(24));"
SECRET_KEY = os.getenv("SECRET_KEY")

# DB settings
POSTGRES = {
    "user": os.getenv("POSTGRESQL_DB_USER"),
    "pw": os.getenv("POSTGRESQL_DB_PASS"),
    "db": os.getenv("POSTGRESQL_DB_NAME"),
    "host": os.getenv("POSTGRESQL_DB_HOST"),
    "port": os.getenv("POSTGRESQL_DB_PORT"),
}

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = (
    "postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s"
    % POSTGRES
)

SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids a SQLAlchemy Warning

# Flask-Mail settings
# For smtp.gmail.com to work, you MUST set "Allow less secure apps" to ON in Google Accounts.
# Change it in https://myaccount.google.com/security#connectedapps (near the bottom).
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_USERNAME = os.getenv("SMTP_MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("SMTP_MAIL_PASS")

# Sendgrid settings
SENDGRID_API_KEY = os.getenv("API_KEY_SENDGRID")

# Flask-User settings
USER_APP_NAME = os.getenv("APP_NAME")
USER_EMAIL_SENDER_NAME = os.getenv("ADMIN_USERNAME")
USER_EMAIL_SENDER_EMAIL = os.getenv("SMTP_MAIL_USERNAME")

ADMINS = [
    "{admin} <{email}>".format(
        admin=os.getenv("ADMIN_USERNAME"), email=os.getenv("SMTP_MAIL_USERNAME")
    ),
]
