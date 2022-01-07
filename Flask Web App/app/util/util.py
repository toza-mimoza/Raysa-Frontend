from datetime import datetime
from time import mktime

from app.models.bot_models import Bots


def check_if_bot_exists(query_name) -> bool:
    """Query DB for the Bot"""
    if not Bots.query.filter_by(bot_name=query_name).first():
        return False
    return True


def get_unix_time() -> int:
    """Returns current Unix time integer."""
    return int(mktime(datetime.now().timetuple()))


def get_by_name_from_list(query, list):
    """
    Returns an element from the list based on item's name.
    O(n) complexity.
    """
    for item in list:
        if query == item.name:
            return item
    return None
