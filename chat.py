from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton

from utils import dialogue

from main import send_keyboard, send_text


def send_message(user_id, dialog_name, reply_cntr, phrase_idx):
    print(app.resolve_peer(user_id))

    response = dialogue.listen(user_id, dialog_name, reply_cntr, phrase_idx)

    print(response)

    if response["ok"]:
        response = response["message"]
        if type(response) == dict:
            send_keyboard(user_id,
                          response["question"]["q"],
                          InlineKeyboardMarkup(
                                [
                                    generate_buttons(dialog_name,
                                                     response["reply_cntr"],
                                                     response["question"]["a"])
                                ]
                          ))
        else:
            send_text(user_id, "Hey smth is broken, sorry friend ^^'")


def start(user_id, dialog_name):
    dialogue.hello(user_id, dialog_name)
    send_message(user_id, dialog_name, 0, 1)


def generate_buttons(dialog_name, new_reply_cntr, variants):
    buttons = []

    for variant_idx, variant in variants.items():
        callback_data = "{dialog}_{reply_cntr}_{phrase_idx}"\
                        .format(dialog=dialog_name,
                                reply_cntr=new_reply_cntr,
                                phrase_idx=variant_idx)

        buttons.append(InlineKeyboardButton(variant,
                                            callback_data=callback_data))

    return buttons
