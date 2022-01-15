from flask import Blueprint

api = Blueprint("api", __name__)


@api.route("/api/create/conversation")
def create_conversation(content_name):
    """
    Creates a conversation 
    """
    response = ""
    return response
