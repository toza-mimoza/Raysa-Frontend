from app.util.util import get_unix_time


class Tracker:
    __abstract__ = True

    def __init__(self):
        self.created_on = get_unix_time()

    def __repr__(self):
        """Define a base way to print tracker"""
        return "<{0.__class__.__name__}: created_on={0.created_on!r}>".format(self)


class MessageTracker(Tracker):
    def __init__(self, sender=None, receiver=None):
        self.sent_at = get_unix_time()
        print(self.sent_at)


class ConversationTracker(Tracker):
    def __init__(self, message_list):
        super()
        self.message_list = message_list
