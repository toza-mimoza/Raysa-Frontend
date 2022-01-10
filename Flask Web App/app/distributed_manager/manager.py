# manager for distributed system
# sends commands to nodes for:
#   triggering training of bots
#   file extraction (logs)
#   on the other end there is an HTTP RESTful API for offering files to download
#   SECURITY: implement token based authentication for RESTful service (API keys)
import random
import requests
import logging
import uuid
from app.util.util import get_or_set_session_uid
from flask import session
from flask_socketio import emit
from .trackers import MessageTracker
from app.util.util import dict_questions, remove_quotes_from_str
from app.models.bot_models import Tags, Conversations

log = logging.getLogger(__name__)


def init_dist_manager(socketio, app, db):
    db.init_app(app)
    # with app.app_context():
    #     print(app.name)
    #     Tags.create(tag_name="BotBOTBOT")
    dist_manager = DistributedManager(bot_url_dict={})
    STUB_RESPONSE = "STUB_RESPONSE"

    @socketio.on("connect")
    def handle_connection():
        log.info("Connected a client.")
        # check if session changed
        # start a new conversation

        session_uid = get_or_set_session_uid(session)

        with app.app_context():
            #
            # conversation = Conversations.retrieve(session_uid=session_uid)

            # if not conversation:
            #     Conversations.create(session_uid=session_uid)
            pass

    # general message channel for misc stuff, not to be used for user messages
    @socketio.on("message")
    def handle_message(msg):
        log.info(f"Client message: {msg}")
        pass

    @socketio.on("UserSendsMessage")
    def handle_user_message(msg):
        log.info(f"User sent: {msg}")
        # response = dist_manager.send_request_to(url, body)
        emit("response_event", STUB_RESPONSE)  # response.text
        log.info(f"Response emitted: {STUB_RESPONSE}")  # response.text
        pass

    @socketio.on("request_question_event")
    def handle_question_request():
        rand_number = random.randint(1, len(dict_questions))
        response = dict_questions[rand_number]
        emit(
            "response_question_event", remove_quotes_from_str(response)
        )  # response.text
        log.info(f"User requested a random question, got: {response}.")
        pass


def ack_client():
    log.info("Message was received by the client.")


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
        sends a RASA HTTP request to the specified URL.

    send_request_to_all(self, body, headers=None)
        sends a RASA HTTP request to each of the Bots in the Raysa cluster.

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
