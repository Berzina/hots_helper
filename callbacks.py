from utils.views import responce_form
from main import send_text


def echo(user_id, message):
    print(user_id, "ok")
    print(responce_form(user_id, message))
    send_text(user_id, responce_form(user_id, message))
    # app.send_message(
    #     user_id,
    #     responce_form(message)
    # )
