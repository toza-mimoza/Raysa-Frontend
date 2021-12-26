# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.

from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_user import UserManager, user_manager
from flask_gravatar import Gravatar
from flask_wtf.csrf import CSRFProtect
from .models.db import db
from .models.bot_models import Bots
from .models.user_models import User, Role
from .models.site_models import Site
import datetime
from .secrets_file import *
from .views import register_blueprints
from app.common.extensions import cache

# Instantiate Flask extensions
csrf_protect = CSRFProtect()

mail = Mail()
migrate = Migrate()
gravatar = None 
# cache = Cache(config=cache_config)

def init_data():
    '''Initialize site data'''
    if not Site.query.filter(Site.site_name == INIT_SITE_NAME).first():
        site = Site(site_name = INIT_SITE_NAME,
                site_description= "This is a currently ongoing project of building distributed Rasa chatbots with Ray distributed functions library, hence the project name Raysa.",
                site_visitors_total_count = 0,
            )

        db.session.add(site)
        db.session.commit()

    if not Bots.query.filter(Bots.bot_name == INIT_BOT_NAME1).first():
        bot1 = Bots(bot_name=INIT_BOT_NAME1, 
                bot_description = INIT_BOT_DESCRIPTION,
                bot_added_at = datetime.datetime.utcnow(),
                vm_name = INIT_VM_NAME_1,
                vm_type = INIT_VM_TYPE_1,
                vm_res_group = INIT_VM_RES_GROUP1,
                vm_ip = INIT_VM_IP_1,
                vm_vcpu = INIT_VM_VCPU1,
                vm_region = INIT_VM_REGION,
                vm_ram = INIT_VM_RAM1,
            )

        db.session.add(bot1)
        db.session.commit()

    if not Bots.query.filter(Bots.bot_name == INIT_BOT_NAME2).first():
        bot2 = Bots(bot_name=INIT_BOT_NAME2, 
                bot_description = INIT_BOT_DESCRIPTION,
                bot_added_at = datetime.datetime.utcnow(),
                vm_name = INIT_VM_NAME_2,
                vm_type = INIT_VM_TYPE_2,
                vm_res_group = INIT_VM_RES_GROUP2,
                vm_ip = INIT_VM_IP_2,
                vm_vcpu = INIT_VM_VCPU2,
                vm_region = INIT_VM_REGION,
                vm_ram = INIT_VM_RAM2,
            )

        db.session.add(bot2)
        db.session.commit()

    if not Bots.query.filter(Bots.bot_name == INIT_BOT_NAME3).first():
        bot3 = Bots(bot_name=INIT_BOT_NAME3, 
                bot_description = INIT_BOT_DESCRIPTION,
                bot_added_at = datetime.datetime.utcnow(),
                vm_name = INIT_VM_NAME_3,
                vm_type = INIT_VM_TYPE_3,
                vm_res_group = INIT_VM_RES_GROUP3,
                vm_ip = INIT_VM_IP_3,
                vm_vcpu = INIT_VM_VCPU3,
                vm_region = INIT_VM_REGION,
                vm_ram = INIT_VM_RAM3,
            )

        db.session.add(bot3)
        db.session.commit()

# Initialize Flask Application
def create_app(extra_config_settings={}):
    """Create a Flask application.
    """
    # Instantiate Flask
    app = Flask(__name__)

    # Load common settings
    app.config.from_object('app.settings')
    # Load environment specific settings
    app.config.from_object('app.local_settings')
    # Load extra settings from extra_config_settings param
    app.config.update(extra_config_settings)
    
    cache.init_app(app)
    # Setup Flask-SQLAlchemy
    db.init_app(app)
    #db.create_all()
    global gravatar
    gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    use_ssl=False,
                    base_url=None)
    # Setup Flask-Migrate
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
    # Setup Flask-Mail
    mail.init_app(app)

    # Setup WTForms CSRFProtect
    csrf_protect.init_app(app)

    # Register blueprints
    register_blueprints(app)
    
    # Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
    from wtforms.fields import HiddenField

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

    app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

    # Setup an error-logger to send emails to app.config.ADMINS
    init_email_error_handler(app)

    # Setup Flask-User to handle user account related forms
    #from .models.user_models import User, Role
    #from .views.main_views import user_profile_page

    # Setup Flask-User
    user_manager = UserManager(app, db, User)
    
    # Create 'admin@example.com' user with 'Admin' and 'Agent' roles

    with app.app_context():
        init_data()
        if not User.query.filter(User.email == SMTP_MAIL_USERNAME).first():
            user = User(email=SMTP_MAIL_USERNAME, 
                    email_confirmed_at=datetime.datetime.utcnow(),
                    password=user_manager.hash_password(SMTP_MAIL_PASS),
                    active=True,
                    first_name='Svetozar',
                    last_name='Stojanovic',
                )

            user.roles.append(Role(name='Admin'))
            user.roles.append(Role(name='Agent'))
            db.session.add(user)
            db.session.commit()
        

    @app.context_processor
    def context_processor():
        return dict(user_manager=user_manager)

    return app


def init_email_error_handler(app):
    """
    Initialize a logger to send emails on error-level messages.
    Unhandled exceptions will now send an email message to app.config.ADMINS.
    """
    if app.debug: return  # Do not send error emails while developing

    # Retrieve email settings from app.config
    host = app.config['MAIL_SERVER']
    port = app.config['MAIL_PORT']
    from_addr = app.config['MAIL_DEFAULT_SENDER']
    username = app.config['MAIL_USERNAME']
    password = app.config['MAIL_PASSWORD']
    secure = () if app.config.get('MAIL_USE_TLS') else None

    # Retrieve app settings from app.config
    to_addr_list = app.config['ADMINS']
    subject = app.config.get('APP_SYSTEM_ERROR_SUBJECT_LINE', 'System Error')

    # Setup an SMTP mail handler for error-level messages
    import logging
    from logging.handlers import SMTPHandler

    mail_handler = SMTPHandler(
        mailhost=(host, port),  # Mail host and port
        fromaddr=from_addr,  # From address
        toaddrs=to_addr_list,  # To address
        subject=subject,  # Subject line
        credentials=(username, password),  # Credentials
        secure=secure,
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    # Log errors using: app.logger.error('Some error message')
