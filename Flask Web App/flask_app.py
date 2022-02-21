from app import create_app

app, socketio = create_app()

if __name__ == "__main__":
    # for socketio
    import eventlet

    eventlet.monkey_patch()

    socketio.run(app)
