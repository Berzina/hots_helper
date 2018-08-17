from utils.views import responce_form


def echo(app, user_id, message):
    app.send_message(
        user_id,
        responce_form(user_id, message)
    )
