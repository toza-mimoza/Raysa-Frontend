import logging
import random
from flask import session
from flask_socketio import emit
from app.util.util import dict_questions, remove_quotes_from_str
from app.util.constants import STUB_RESPONSE

log = logging.getLogger(__name__)


def handle_connection():
    log.info("Connected a client.")
    # start a new conversation
    # create_conversation(app, db)


def handle_message(msg):
    log.info(f"Client message: {msg}")
    pass


def handle_user_message(msg):
    log.info(f"User sent: {msg}")
    # response = dist_manager.send_request_to(url, body)
    emit("response_event", STUB_RESPONSE)  # response.text
    log.info(f"Response emitted: {STUB_RESPONSE}")  # response.text
    pass


def handle_question_request():
    rand_number = random.randint(1, len(dict_questions))
    response = dict_questions[rand_number]
    emit("response_question_event", remove_quotes_from_str(response))  # response.text
    log.info(f"User requested a random question, got: {response}.")
    pass
