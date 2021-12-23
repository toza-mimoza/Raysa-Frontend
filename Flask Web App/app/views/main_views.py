from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required

from app import db
from app.models.user_models import UserProfileForm, UserRegisterForm
from app.models.bot_models import Bot

from app.util import check_if_bot_exists 

main_blueprint = Blueprint('main', __name__, template_folder='templates')

@main_blueprint.app_errorhandler(404)
def page_not_found(content_name):
    '''
    Returns 404 Page Not Found Custom Error page.
    content_name: Type of content not found (bot, conversation, etc.)
    '''
    return render_template('404.html', content_name=content_name), 404

@main_blueprint.app_errorhandler(500)
def internal_server_error(e):
    '''
    Returns 500 Internal Server Error page.
    '''
    return render_template('500.html'), 500

@main_blueprint.route('/')
def index():
    '''Returns a template for the index page.'''
#    return '<h1>Hello World!</h1>'
#    user_agent = request.headers.get('User-Agent')
#    return '<p>Your browser is {}</p>'.format(user_agent)
    return render_template('index.html')

# The User page is accessible to authenticated users (users that have logged in)
# @main_blueprint.route('/user')
# @login_required  # Limits access to authenticated users
# def user():
#     '''Returns a template for the user profile page.'''
#     return render_template('user_profile_page.html')
# The User page is accessible to authenticated users (users that have logged in)

@main_blueprint.route('/member')
@login_required  # Limits access to authenticated users
def member_page():
    return render_template('user_page.html')
# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_required('Admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('admin_page.html')

@main_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.index'))

    # Process GET or invalid POST
    return render_template('user_profile_page.html',
                           form=form)