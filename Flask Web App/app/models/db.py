import logging
from flask_sqlalchemy import SQLAlchemy
from .db_exceptions import DBexception

# Session.expire_on_commit = False
db = SQLAlchemy()

log = logging.getLogger(__name__)


class BaseMixin(object):
    @classmethod
    def create(cls, **kw):
        """Create Crud operation."""
        instance = cls(**kw)
        try:
            db.session.add(instance)
            db.session.commit()
            log.info(
                f"{instance.__class__.__name__}: The {instance.__class__.__name__} CREATED in DB."
            )
        except DBexception as e:
            log.critical(
                f"{e.__class__.__name__}: The {instance.__class__.__name__} cannot be CREATED in DB."
            )
            raise
        return instance

    @classmethod
    def retrieve(cls, **kw):
        """Retrieve cRud operation."""
        instance = db.session.query(cls).filter_by(**kw).first()
        if instance:
            log.info(
                f"{instance.__class__.__name__}: The {instance.__class__.__name__} RETRIEVED from the DB."
            )
        log.info(
            f"An instance of {instance.__class__.__name__} is being RETRIEVED from the DB."
        )
        return instance

    @classmethod
    def retrieve_all(cls, **kw):
        """
        Retrieve cRud operation returning a list of objects with common attribute specified by kw argument.
        """
        instances = db.session.query(cls).filter_by(**kw).all()
        if instances:
            log.info(
                f"Instances of {instances.__class__.__name__} are being RETRIEVED from the DB."
            )
        return instances

    @classmethod
    def update(cls, **kw):
        """Update crUd operation."""
        instance = db.session.query(cls).filter_by(**kw).first()
        if instance:
            try:
                db.session.add(instance)
                db.session.commit()
                log.info(
                    f"An instance of {instance.__class__.__name__} is UPDATED in the DB."
                )
            except DBexception as e:
                log.critical(
                    f"{e.__class__.__name__}: The {instance.__class__.__name__} cannot be UPDATED in the DB."
                )
            return True
        else:
            return False

    @classmethod
    def delete(cls, **kw):
        """Delete cruD operation."""
        instance = db.session.query(cls).filter_by(**kw).first()
        if instance:
            try:
                db.session.delete(instance)
                db.session.commit()
                log.info(
                    f"An instance of {instance.__class__.__name__} is DELETED from DB."
                )
            except DBexception as e:
                log.critical(
                    f"{e.__class__.__name__}: The {instance.__class__.__name__} cannot be DELETED from DB."
                )
            return True
        else:
            return False


class BaseModel(db.Model, BaseMixin):
    """Base data model for all objects"""

    __abstract__ = True
    # def __init__(self, *args):
    # #     super().__init__(*args)
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        """Define a base way to print models"""
        return "<{0.__class__.__name__}: created_on={0.created_on!r}>".format(self)

    # def json(self):
    #     """
    #     Define a base way to jsonify models, dealing with datetime objects
    #     """
    #     return {
    #         column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
    #         for column, value in self.to_dict().items()
    #     }
