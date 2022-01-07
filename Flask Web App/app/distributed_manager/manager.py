# manager for distributed system
# sends commands to nodes for:
#   triggering training of bots
#   file extraction (logs)
#   on the other end there is an HTTP RESTful API for offering files to download
#   SECURITY: implement token based authentication for RESTful service (API keys)
import requests
import logging
from flask_socketio import emit
from .trackers import MessageTracker


log = logging.getLogger(__name__)


def init_handlers(socketio):
    dist_manager = DistributedManager(bot_url_dict={})
    STUB_RESPONSE = "STUB_RESPONSE"

    @socketio.on("connect")
    def handle_connection():
        log.info("Connected a client.")
        pass

    @socketio.on("message")
    def handle_message(msg):
        log.info(f"Client message: {msg}")
        pass

    @socketio.on("UserSendsMessage")
    def handle_user_message(msg):
        log.info(f"User message: {msg}")
        # response = dist_manager.send_request_to(url, body)
        emit("response_event", STUB_RESPONSE)  # response.text
        log.info(f"Response emitted: {STUB_RESPONSE}")  # response.text
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
