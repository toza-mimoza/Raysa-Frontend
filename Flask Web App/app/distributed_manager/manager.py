# manager for distributed system
# sends commands to nodes for:
#   triggering training of bots
#   file extraction (logs)
#   on the other end there is an HTTP RESTful API for offering files to download
#   SECURITY: implement token based authentication for RESTful service (API keys)

import requests
import logging
from flask import session
from .trackers import MessageTracker
from app.util.util import get_or_set_session_uid
from app.models.bot_models import Conversations

log = logging.getLogger(__name__)


def create_conversation(app, db):
    db.init_app(app)
    session_uid = get_or_set_session_uid(session)

    with app.app_context():
        Conversations.create(session_uid=session_uid)


def init_dist_manager(bot_url_dict: dict = None):
    # db.init_app(app)
    # with app.app_context():
    #     print(app.name)
    #     Tags.create(tag_name="BotBOTBOT")
    dist_manager = DistributedManager(bot_url_dict)


class DistributedManager:
    """
    DistributedManager handles request sending and receiving to and from
    chatbots, which all communicate with the Raysa Flask platform.

    Attributes
    ----------
    bot_url_dict : dict{ Bot : str }
        dictionary of bots as keys and their URL addresses as strings.

    Methods
    -------
    send_request_to(self, url, body, headers=None)
        sends a HTTP request to the specified URL.

    send_request_to_all(self, body, headers=None)
        sends a HTTP request to each of the Bots in the Raysa cluster.

    get_best_matched_response(self)
        returns a best matched response string to the caller
    """

    responses_list = []

    def __init__(self, bot_url_dict):
        self.bot_url_dict = bot_url_dict

    def send_request_to(self, url, body, headers=None):
        if headers is None:
            return requests.post(url, json=body)
        else:
            return requests.post(url, headers=headers, json=body)

    def send_request_to_all(self, body, headers=None):
        """
        This class uses the attribute bot_url_dict to send requests to all
        chatbots.
        """

        for bot in self.bot_url_dict:
            self.responses_list.append(
                self.send_request_to(self.bot_url_dict[bot], body)
            )

    def get_best_matched_response(self):
        return None
