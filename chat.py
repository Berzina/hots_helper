from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton

from main import app

from utils import dialogue


def start(user_id, dialog_name):
    dialogue.hello(user_id, dialog_name)
    send_message(user_id, dialog_name, 0, 1)


def send_message(user_id, dialog_name, reply_cntr, phrase_idx):

    response = dialogue.listen(user_id, dialog_name, reply_cntr, phrase_idx)

    if response["ok"]:
        response = response["message"]
        if type(response) == dict:
            app.send_message(
                user_id,
                response["question"]["q"],
                reply_markup=InlineKeyboardMarkup(
                    [
                        generate_buttons(dialog_name,
                                         response["reply_cntr"],
                                         response["question"]["a"])
                    ]
                )
            )
        else:
            app.send_message(
                user_id,
                "Hey smth is broken, sorry friend ^^'"
            )


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
