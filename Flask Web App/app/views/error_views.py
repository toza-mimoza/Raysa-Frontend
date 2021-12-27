from flask import Blueprint, render_template 

error_blueprint = Blueprint('error', __name__, template_folder='templates')

@error_blueprint.app_errorhandler(404)
def page_not_found(content_name):
    '''
    Returns 404 Page Not Found Custom Error page.
    content_name: Type of content not found (bot, conversation, etc.)
    '''
    return render_template('error_pages/404.html', content_name=content_name), 404

@error_blueprint.app_errorhandler(500)
def internal_server_error(e):
    '''
    Returns 500 Internal Server Error page.
    '''
    return render_template('error_pages/500.html'), 500