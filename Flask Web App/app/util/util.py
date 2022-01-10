from datetime import datetime
from time import mktime

from app.models.bot_models import Bots

import pandas as pd
import uuid


def load_dict_from_csv(filename):
    return {row[0]: row[1] for _, row in pd.read_csv(filename).iterrows()}


dict_questions = load_dict_from_csv("app/util/sample_questions.csv")


def get_or_set_session_uid(session):
    if "uid" in session:
        return session["uid"]
    else:
        # generate uuid4
        session_uid = uuid.uuid4().hex
        session["uid"] = session_uid
        return session_uid
        pass


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


def remove_quotes_from_str(string: str) -> str:
    return string.replace('"', "")


def remove_quotes_around_str(string: str) -> str:
    if string.startswith('"'):
        string = string[1:]
    if string.endswith('"'):
        string = string[:-1]
    return string
