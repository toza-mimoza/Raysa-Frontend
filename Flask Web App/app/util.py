from app.models.bot_models import Bots


def check_if_bot_exists(query_name):
    """Query DB for the Bot"""
    if not Bots.query.filter_by(bot_name=query_name).first():
        return False
    return True
