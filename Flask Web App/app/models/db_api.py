from .db import db
from .bot_models import Actor, Bots, Conversations, Messages, Tags
from .user_models import User
from util.util import get_unix_time
from flask_user.password_manager import PasswordManager


def get_password_manager(app):
    return PasswordManager(app)


def add_tag_to_bot(tag_name):
    """Add actor to the DB."""
    tag = Tags(tag_name=tag_name)
    db.session.add(tag)
    db.session.commit()
    return tag


def add_actor(actor_messages):
    """Add actor to the DB."""
    actor = Actor(actor_messages=actor_messages)
    db.session.add(actor)
    db.session.commit()
    return actor


def add_user(email, is_active, password_hash, first_name, last_name, roles):
    """Function to add messages and automatically conversation for it."""

    user = User(
        email=email,
        password=password_hash,
        active=is_active,
        first_name=first_name,
        last_name=last_name,
    )
    db.session.add(user)
    db.session.commit()
    return user


def add_bot(
    bot_name,
    bot_description,
    vm_name,
    vm_ip,
    vm_vcpu,
    vm_ram,
    vm_res_group=None,
    vm_type=None,
    vm_region=None,
    tags_list=None,
    conv_list=None,
):
    """Function to add messages and automatically conversation for it."""
    bot = Bots(
        bot_name=bot_name,
        bot_description=bot_description,
        bot_added_at=get_unix_time(),
        vm_name=vm_name,
        vm_ip=vm_ip,
        vm_vcpu=vm_vcpu,
        vm_ram=vm_ram,
    )

    db.session.add(bot)
    db.session.commit()
    return bot


def add_message(sender, msg_txt, conversation):
    """
    Function to add messages and automatically add the passed conversation for
    it.
    """
    message = Messages(sender_uuid=sender.uuid, message_text=msg_txt)

    db.session.add(message)
    db.session.commit()
    return message


def add_conversation(messages=None):
    """Function to add conversation to the DB."""

    conversation = Conversations(messages=messages)
    db.session.add(conversation)
    db.session.commit()
    return conversation
