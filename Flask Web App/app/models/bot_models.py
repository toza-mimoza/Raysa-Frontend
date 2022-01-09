from .db import db, BaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid
import logging
from datetime import date, timedelta
import datetime
from .db_exceptions import DBexception

log = logging.getLogger(__name__)

bots_conversations = db.Table(
    "bots_conversations",
    db.Column("bot_id", db.Integer, db.ForeignKey("bots.id"), primary_key=True),
    db.Column(
        "conversation_uuid",
        UUID(),
        db.ForeignKey("conversations.uuid"),
        primary_key=True,
    ),
)

bot_tags = db.Table(
    "bot_tags",
    db.Column("tags_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
    db.Column("bot_id", db.Integer, db.ForeignKey("bots.id"), primary_key=True),
)


class Bots(BaseModel, db.Model):
    """Model to hold data about a (chat)bot"""

    __tablename__ = "bots"
    id = db.Column(db.Integer, primary_key=True)
    bot_name = db.Column(db.String(50))
    bot_tags = db.relationship(
        "Tags",
        secondary=bot_tags,
        lazy="subquery",
        backref=db.backref("bots", lazy=True),
    )
    bot_conversations = db.relationship(
        "Conversations",
        secondary=bots_conversations,
        lazy="subquery",
        backref=db.backref("bots", lazy=True),
    )
    bot_description = db.Column(db.String(300))
    bot_added_at = db.Column(db.DateTime())
    bot_stats = db.relationship("Statistics", backref="statistics", lazy=True)
    vm_name = db.Column(db.String(30))
    vm_res_group = db.Column(db.String(30))
    vm_type = db.Column(db.String(30))
    vm_ip = db.Column(db.String(15))
    vm_vcpu = db.Column(db.Float)
    vm_region = db.Column(db.String(15))
    vm_ram = db.Column(db.Float)


class Tags(db.Model):
    """Model for tagging system for bots."""

    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(30))


class Conversations(BaseModel, db.Model):
    """Model that holds data about conversations happening with the widget on the Raysa Platform."""

    __tablename__ = "conversations"
    uuid = db.Column(
        UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex
    )
    messages = db.relationship("Messages", backref="conversations", lazy=True)


class Actor(BaseModel, db.Model):
    """Model for the conversations sender and receiver of messages."""

    __tablename__ = "actors"
    uuid = db.Column(
        UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex
    )
    actor_messages = db.relationship("Messages", backref="actors", lazy=True)


class Messages(BaseModel, db.Model):
    """Model for the messages that are part of conversations."""

    __tablename__ = "messages"
    uuid = db.Column(
        UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex
    )
    sender_uuid = db.Column(UUID(), db.ForeignKey("actors.uuid"), nullable=False)
    conversation_uuid = db.Column(
        UUID(), db.ForeignKey("conversations.uuid"), nullable=False
    )
    message_text = db.Column(db.String(150))


class Statistics(BaseModel, db.Model):
    """Model for holding statistics for a particular bot."""

    __tablename__ = "statistics"
    stats_id = db.Column(db.Integer, primary_key=True)
    bot_id = db.Column(db.Integer, db.ForeignKey("bots.id"))
    date_added = db.Column(db.Date, default=datetime.date.today(), nullable=False)
    num_requests_handled = db.Column(db.Integer)

    @classmethod
    def create(cls, **kwargs):
        """
        Overloaded create Crud operation for Statistics class.
        Compared to base classmethod this method checks if Statistics object for the same date and same bot exists before adding it to the DB.
        """
        # init instance
        instance = None
        # get date and bot_id from arguments
        date_from_args = None
        bot_id_from_args = None

        for kw in kwargs:
            if kw == "date_added":
                date_from_args = kwargs[kw]
            if kw == "bot_id":
                bot_id_from_args = kwargs[kw]

        # if date is specified
        if date_from_args:
            # compare this date to anything in db
            query = Statistics.retrieve(
                bot_id=bot_id_from_args, date_added=date_from_args
            )

            # if such date exists stored in a Statistics object
            if query:
                return None
            else:
                instance = cls(**kwargs)

                try:
                    db.session.add(instance)
                    db.session.commit()
                except DBexception as e:
                    log.critical(
                        f"{e.__class__.__name__}: The {instance.__class__.__name__} cannot be CREATED in DB."
                    )
                    raise
                log.info(
                    f"A Statistics object with date: {instance.date_added} successfully added to DB."
                )
        else:
            # if date is not specified
            instance = cls(**kwargs)
            # see if it was added today
            query = Statistics.retrieve(date_added=date.today())

            if query:
                # if it is, log it on WARNING level
                log.warn(
                    f"Statistics object for date: {date.today()} already added to DB!"
                )
            else:
                try:
                    db.session.add(instance)
                    db.session.commit()
                except DBexception as e:
                    log.critical(
                        f"{e.__class__.__name__}: The {instance.__class__.__name__} cannot be CREATED in DB."
                    )
                    raise
                log.info(
                    f"A Statistics object with date: {instance.date_added} successfully added to DB."
                )
        return instance

    @classmethod
    def retrieve_past_week(cls, **kw):
        """
        Retrieve cRud operation returning a list of Statistic objects within the past week.
        """
        last_week_date = date.today() - timedelta(days=7)
        base_query = db.session.query(cls)
        query_optional = base_query.filter_by(**kw)
        query_date = query_optional.filter(Statistics.date_added > last_week_date)
        final_query = query_date.all()

        log.info(
            f"Multiple instances of {Statistics.__class__.__name__} from the past week are being RETRIEVED from the DB."
        )
        return final_query
