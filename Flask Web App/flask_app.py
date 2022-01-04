from app import create_app

app, socketio = create_app()


@socketio.on("connect")
def handle_connection():
    print("Connected a client...")


@socketio.on("message")
def handle_message(msg):
    print(f"Client message: {msg}")


@socketio.on("UserSendsMessage")
def handle_user_message(msg):
    print(f"User message: {msg}")


if __name__ == "__main__":
    socketio.run(app)
