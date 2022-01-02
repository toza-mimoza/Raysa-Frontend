from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user

from app import db
from app.models.site_models import Site
from app.secrets_file import INIT_SITE_NAME
from app.views.error_views import page_not_found

site_blueprint = Blueprint("site", __name__, template_folder="templates")


def get_site():
    query_site = Site.query.filter(Site.site_name == INIT_SITE_NAME).first()
    if not query_site:
        return page_not_found("Site")

<<<<<<< HEAD
    query_site.site_visitors_total_count += 1
=======
    query_site.site_visitors_total_count+=1
>>>>>>> 327f879d76ba5cf776249bed536d64072690f323
    db.session.commit()
    return query_site


def add_view(site):
    site.site_visitors_total_count += 1
    db.session.commit()


@site_blueprint.route("/about")
def about():
    """Returns a template for the project's abouts page."""
    query_site = get_site()

    return render_template("site/about.html", data=query_site)


@site_blueprint.before_app_request
def before_request():
    # lang = get_locale()
    # lang = lang if lang else app.config['BABEL_DEFAULT_LOCALE']
    # set_lang(lang)

    if request.path.startswith("/admin"):
        if current_user.is_authenticated:
            if not current_user.has_role("Admin"):
                return redirect(url_for("user.logout"))
        else:
            return redirect(url_for("user.login"))


@site_blueprint.route("/backend")
def backend():
<<<<<<< HEAD
    """Redirects to the admin panel page at '/admin'."""
    return redirect("admin")
=======
    '''Redirects to the admin panel page at '/admin'.'''
    return redirect('admin')
>>>>>>> 327f879d76ba5cf776249bed536d64072690f323
