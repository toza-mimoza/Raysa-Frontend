from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required

from app import db

from app.models.site_models import Site 
from app.secrets_file import INIT_SITE_NAME
from app.common.extensions import cache
from app.views.error_views import page_not_found

main_blueprint = Blueprint('main', __name__, template_folder='templates')

@main_blueprint.route('/')
@cache.cached(timeout=50)
def index():
    '''Returns a template for the index page.'''

    query_site = Site.query.filter(Site.site_name == INIT_SITE_NAME).first()
    if query_site:
        query_site.site_visitors_total_count+=1
        db.session.commit()
        
        return render_template('site/index.html', site_data=query_site)
    else: 
        return page_not_found("Site")

@main_blueprint.route('/member')
@login_required  # Limits access to authenticated users
@cache.cached(timeout=50)
def member_page():
    user = current_user

    context = {
        "user": user, 
    }
    return render_template('user/user_profile_page.html', context=context)



@main_blueprint.before_app_request
def before_request():
    # lang = get_locale()
    # lang = lang if lang else app.config['BABEL_DEFAULT_LOCALE']
    # set_lang(lang)

    if request.path.startswith('/admin'):
        if current_user.is_authenticated:
            if not current_user.has_role("Admin"):
                return redirect(url_for('user.logout'))
        else:
            return redirect(url_for('user.login'))

# @main_blueprint.route('/profile', methods=['GET', 'POST'])
# @login_required
# def user_profile_page():
#     # Initialize form
#     form = UserProfileForm(request.form, obj=current_user)

#     # Process valid POST
#     if request.method == 'POST' and form.validate():
#         # Copy form fields to user_profile fields
#         form.populate_obj(current_user)

#         # Save user_profile
#         db.session.commit()

#         # Redirect to home page
#         return redirect(url_for('main.index'))

#     # Process GET or invalid POST
#     return render_template('user/user_profile_page.html',
#                            form=form)