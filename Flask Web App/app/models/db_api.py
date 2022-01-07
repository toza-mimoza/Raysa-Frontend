import logging
from typing import List, Union
from .db import db
from .bot_models import Actor, Bots, Conversations, Messages, Tags
from .user_models import User, Role
from app.util.util import get_unix_time, get_by_name_from_list
from flask_user.password_manager import PasswordManager
from flask import current_app as app
from .db_exceptions import DBexception
from flask.cli import with_appcontext

log = logging.getLogger(__name__)


@with_appcontext
def get_password_manager(app) -> PasswordManager:
    return PasswordManager(app)


@with_appcontext
def __add_model_to_db(model):
    """Internal function for adding a model to DB."""
    try:
        db.add(model)
        db.commit()
    except DBexception as e:
        log.critical(
            f"{e.__class__.__name__}: A {model.__class__.__name__} cannot be ADDED to DB."
        )
        raise


@with_appcontext
def __remove_model_from_db(model):
    """Internal function for removing a model from DB."""
    try:
        db.session.delete(model)
        db.commit()
    except DBexception as e:
        log.critical(
            f"{e.__class__.__name__}: The {model.__class__.__name__} cannot be DELETED from DB."
        )
        raise


@with_appcontext
def add_tag_to_bot(tag_name: str, bot_name: str) -> Union[Tags, None]:
    """Add actor to the DB."""

    # get bot name
    bot = Bots.query.filter(Bots.bot_name == bot_name).first()
    # make tag
    tag = Tags(tag_name=tag_name)
    if bot is not None:
        bot.tags_list.append(tag)
        __add_model_to_db(bot)
        app.logger.info(f"Tag with id <{tag.id}> added to bot {bot.bot_name}")
        return tag
    else:
        return None


@with_appcontext
def remove_tag_from_bot(tag_name: str, bot_name: str) -> Tags:
    """Remove tag from bot in the DB."""

    # get bot by name
    bot = Bots.query.filter(Bots.bot_name == bot_name and Bots.tags_list).first()
    # get tag from bot's list
    if bot is not None:
        tag = get_by_name_from_list(tag_name, bot.tags_list)
        if tag is None:
            return None
        bot.tags_list.remove(tag)
        __add_model_to_db(bot)
        log.info(f"Tag with id <{tag.id}> removed from bot {bot.bot_name}")
        return tag
    else:
        return None


@with_appcontext
def add_actor(actor_messages: List[Messages]) -> Actor:
    """Add actor to the DB."""
    actor = Actor(actor_messages=actor_messages)
    __add_model_to_db(actor)
    log.info(f"Actor {actor.uuid} added to DB.")
    return actor


@with_appcontext
def add_user(
    email: str,
    is_active: bool,
    password_hash: str,
    first_name: str,
    last_name: str,
    roles: List[Role],
) -> User:
    """Function to add messages and automatically conversation for it."""

    user = User(
        email=email,
        password=password_hash,
        active=is_active,
        first_name=first_name,
        last_name=last_name,
    )
    __add_model_to_db(user)
    log.info(f"User {user.id} added to DB.")
    return user


@with_appcontext
def add_bot(
    bot_name: str,
    bot_description: str,
    vm_name: str,
    vm_ip: str,
    vm_vcpu: int,
    vm_ram: float,
    vm_res_group: str = None,
    vm_type: str = None,
    vm_region: str = None,
    tags_list: List[Tags] = None,
    conv_list: List[Conversations] = None,
) -> Bots:
    """Function to add Bots to the DB ."""
    bot = Bots(
        bot_name=bot_name,
        bot_description=bot_description,
        bot_added_at=get_unix_time(),
        vm_name=vm_name,
        vm_ip=vm_ip,
        vm_vcpu=vm_vcpu,
        vm_ram=vm_ram,
    )

    __add_model_to_db(bot)
    log.info(f"Bot {bot.id} added to DB.")
    return bot


@with_appcontext
def add_message(sender, msg_txt, conversation):
    """
    Function to add messages and automatically add the passed conversation for
    it.
    """
    message = Messages(sender_uuid=sender.uuid, message_text=msg_txt)

    __add_model_to_db(message)
    log.info(f"Message {message.uuid} added to DB.")
    return message


@with_appcontext
def add_conversation(messages=None):
    """Function to add conversation to the DB."""

    conversation = Conversations(messages=messages)
    __add_model_to_db(conversation)
    log.info(f"Conversation {conversation.uuid} added to DB.")
    return conversation
