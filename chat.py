from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton

from utils import dialogue


def send_message(app, user_id, dialog_name, reply_cntr, phrase_idx):

    response = dialogue.listen(app, user_id, dialog_name, reply_cntr, phrase_idx)

    if response["ok"]:
        response = response["message"]
        if type(response) == dict:
            app.send_message(user_id,
                             response["question"]["q"],
                             reply_markup=InlineKeyboardMarkup(
                                    generate_buttons(dialog_name,
                                                     response["reply_cntr"],
                                                     response["question"]["a"])
                             ))
        else:
            app.send_message(user_id, "Hey smth is broken, sorry friend ^^'")


def start(app, user_id, dialog_name):
    dialogue.hello(user_id, dialog_name)
    send_message(app, user_id, dialog_name, 0, 1)


def generate_buttons(dialog_name, new_reply_cntr, variants):
    buttons = []
    button_row = []

    for variant_idx, variant in variants.items():
        callback_data = "{dialog}_{reply_cntr}_{phrase_idx}"\
                        .format(dialog=dialog_name,
                                reply_cntr=new_reply_cntr,
                                phrase_idx=variant_idx)

        if len(button_row) == 2:
            buttons.append(button_row.copy())
            button_row = []

        button_row.append(InlineKeyboardButton(variant,
                                               callback_data=callback_data))

    if button_row:
        buttons.append(button_row)

    return buttons
