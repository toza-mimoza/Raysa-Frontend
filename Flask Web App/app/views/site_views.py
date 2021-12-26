from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required
from sqlalchemy.orm import query

from app import db
from app.models.site_models import Site 
from app.secrets_file import INIT_SITE_NAME

site_blueprint = Blueprint('site', __name__, template_folder='templates')

def get_site():
    query_site = Site.query.filter(Site.site_name == INIT_SITE_NAME).first()
    if not query_site:
        return page_not_found("Site")
    
    query_site.site_visitors_total_count+=1
    db.session.commit()
    return query_site

def add_view(site):
    site.site_visitors_total_count+=1
    db.session.commit()

@site_blueprint.app_errorhandler(404)
def page_not_found(content_name):
    '''
    Returns 404 Page Not Found Custom Error page.
    content_name: Type of content not found (bot, conversation, etc.)
    '''
    return render_template('404.html', content_name=content_name), 404

@site_blueprint.app_errorhandler(500)
def internal_server_error(e):
    '''
    Returns 500 Internal Server Error page.
    '''
    return render_template('500.html'), 500

@site_blueprint.route('/about')
def about():
    '''Returns a template for the project's abouts page.'''
    query_site = get_site()

    return render_template('about.html', data=query_site)

@site_blueprint.route('/backend')
@roles_required('Admin')  # Limits access to users with the 'admin' role
def backend():
    '''Returns a template for the Raysa site backend page.'''
#    return '<h1>Hello World!</h1>'
#    user_agent = request.headers.get('User-Agent')
#    return '<p>Your browser is {}</p>'.format(user_agent)
    data = {
        "key": "value"
    }
    return render_template('backend.html', data=data)