# manager for distributed system
# sends commands to nodes for:
#   triggering training of bots
#   file extraction (logs)
#   on the other end there is an HTTP RESTful API for offering files to download
#   SECURITY: implement token based authentication for RESTful service (API keys)
import requests
from flask_socketio import send, emit


def init_handlers(socketio):
    @socketio.on("connect")
    def handle_connection():
        print("Connected a client...")

    @socketio.on("message")
    def handle_message(msg):
        print(f"Client message: {msg}")

    @socketio.on("UserSendsMessage")
    def handle_user_message(msg):
        print(f"User message: {msg}")


def ack_client():
    print("Message was received by the client.")


class DistributedManager:
    """
    DistributedManager handles request sending and receiving to and from
    chatbots, which all communicate with the Raysa Flask platform.
    """

    responses_list = []

    def __init__(self, bot_url_list):
        self.bot_url_list = bot_url_list

    def send_request_to(self, url, body, headers=None):
        if headers is None:
            return requests.post(url, json=body)
        else:
            return requests.post(url, headers=headers, json=body)

    def send_request_to_all(self, body, headers=None):
        """
        This class uses the attribute bot_url_list to send requests to all
        chatbots.
        """

        for bot in self.bot_url_list:
            self.responses_list.append(
                self.send_request_to(self.bot_url_list[bot], body)
            )

    def get_best_matched_response(self):
        return None
