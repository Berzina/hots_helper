from main import app
from utils.views import responce_form


def echo(user_id, message):
    # print(responce_form(message))
    app.send_message(
        user_id,
        responce_form(message)
    )
