import logging
import random
import datetime
from flask_socketio import emit
from app.util.util import dict_questions, remove_quotes_from_str
from app.util.constants import STUB_RESPONSE, TIME_FORMAT_TRAINING
from app.distributed_manager.manager import DistributedManager

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
    DistributedManager.send_request_all(DistributedManager.bot_base_urls)
    DistributedManager.clear()
    DistributedManager.send_request_all(DistributedManager.bot_base_urls)
    pass


def handle_question_request():
    rand_number = random.randint(1, len(dict_questions))
    response = dict_questions[rand_number]
    emit("response_question_event", remove_quotes_from_str(response))  # response.text
    log.info(f"User requested a random question, got: {response}.")
    pass


def emit_start_time():
    now = datetime.datetime.now()
    response = now.strftime(TIME_FORMAT_TRAINING)
    emit("res_start_time", response)


def emit_end_time():
    now = datetime.datetime.now()
    response = now.strftime(TIME_FORMAT_TRAINING)
    emit("res_end_time", response)
