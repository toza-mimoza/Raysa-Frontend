from sqlalchemy.orm import backref
from .db import db, BaseModel
from sqlalchemy.dialects.postgresql import UUID

bots_conversations = db.Table('bots_conversations',
    db.Column('bot_id', db.Integer, db.ForeignKey('bots.id'), primary_key=True),
    db.Column('conversation_id', db.Integer, db.ForeignKey('conversations.uuid'), primary_key=True)
)

bot_tags = db.Table('bot_tags',
    db.Column('tags_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('bot_id', db.Integer, db.ForeignKey('bots.id'), primary_key=True)
)

class Bots(BaseModel, db.Model):
    """Model to hold data about a (chat)bot"""
    __tablename__ = 'bots'
    id = db.Column(db.Integer, primary_key = True)
    bot_name = db.Column(db.String(50))
    bot_tags = db.relationship('Tags', secondary=bot_tags, lazy='subquery',
        backref=db.backref('bots', lazy=True))
    # bot_conversations = db.relationship('Conversations', secondary=bots_conversations, lazy='subquery',
    #     backref=db.backref('bots', lazy=True))
    bot_description = db.Column(db.String(300))
    bot_added_at = db.Column(db.DateTime())
    vm_name = db.Column(db.String(30))
    vm_res_group=db.Column(db.String(30))
    vm_type = db.Column(db.String(30))
    vm_ip = db.Column(db.String(15))
    vm_vcpu = db.Column(db.Float)
    vm_region = db.Column(db.String(15))
    vm_ram = db.Column(db.Float)

class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)

class Conversations(BaseModel, db.Model):
    '''Model that holds data about conversations happening with the widget on the Raysa Platform.'''
    __tablename__ = 'conversations'
    uuid = db.Column(UUID(as_uuid=True),
        primary_key=True, default=lambda: uuid.uuid4().hex)
    messages = db.relationship('Messages', backref='conversations', lazy = True)

class Actor(BaseModel, db.Model):
    '''Model for the conversations sender and receiver of messages.'''
    __tablename__ = 'actors'
    uuid=db.Column(UUID(as_uuid=True),
        primary_key=True, default=lambda: uuid.uuid4().hex)
    actor_messages = db.relationship('Messages', backref='actors', lazy = True)

class Messages(BaseModel, db.Model):
    '''Model for the messages that are part of conversations.'''
    __tablename__ = 'messages'
    uuid=db.Column(UUID(as_uuid=True),
        primary_key=True, default=lambda: uuid.uuid4().hex)
    sender_uuid = db.Column(db.Integer, db.ForeignKey('actors.uuid'),
        nullable=False)
    conversation_uuid = db.Column(db.Integer, db.ForeignKey('conversations.uuid'),
        nullable=False)
    message_text =  db.Column(db.String(150))
    
