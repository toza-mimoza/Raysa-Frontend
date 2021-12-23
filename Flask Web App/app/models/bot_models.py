from os import name
from flask_sqlalchemy import SQLAlchemy
import datetime

from flask_user import UserMixin
from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from .db import db, BaseModel


class Bot(BaseModel, db.Model):
    """Model for the bot table"""
    __tablename__ = 'bots'
    id = db.Column(db.Integer, primary_key = True)
    bot_name = db.Column(db.String(50))
    bot_added_at = db.Column(db.DateTime())
    vm_name = db.Column(db.String(30))
    vm_type = db.Column(db.String(30))
    vm_ip = db.Column(db.String(15))
    vm_vcpu = db.Column(db.Float)
    vm_region = db.Column(db.String(15))
    vm_ram = db.Column(db.Float)
    def __init__(self,id,name):
            self.id = id
            self.name=name
