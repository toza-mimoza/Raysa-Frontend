from app.util.util import get_unix_time
from app.models.bot_models import Actor, Messages
from typing import List


class Tracker:
    __abstract__ = True

    def __init__(self):
        self.created_on = get_unix_time()

    def __repr__(self):
        """Define a base way to print tracker"""
        return "<{0.__class__.__name__}: created_on={0.created_on!r}>".format(self)


class MessageTracker(Tracker):
    def __init__(
        self,
        message: Messages,
        sent_at: int,
        sender: Actor = None,
        receiver: Actor = None,
    ):
        self.sent_at = sent_at
        self.message = message
        self.sender = sender
        self.receiver = receiver


class ConversationTracker(Tracker):
    def __init__(self, message_list: List[MessageTracker]):
        super()
        self.message_tracker_list = message_list
