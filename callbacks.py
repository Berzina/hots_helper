from utils.views import responce_form
from main import get_app


def echo(user_id, message):
    print(user_id, "ok")
    print(responce_form(user_id, message))
    app.send_message(user_id, responce_form(user_id, message))
    # send_text()
    # app.send_message(
    #     user_id,
    #     responce_form(message)
    # )
