from app.socketio_events.events import (
    handle_connection,
    handle_message,
    handle_user_message,
    handle_question_request,
)


def register_events(socketio):
    socketio.on_event("connect", handle_connection, namespace="/")
    socketio.on_event("message", handle_message, namespace="/")
    socketio.on_event("UserSendsMessage", handle_user_message, namespace="/")
    socketio.on_event("request_question_event", handle_question_request, namespace="/")
