from .db import db, BaseModel


class Site(BaseModel, db.Model):
    """Model for the bot table"""

    __tablename__ = "site"
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(50))
    site_description = db.Column(db.String(300))
    site_visitors_total_count = db.Column(db.Integer)
