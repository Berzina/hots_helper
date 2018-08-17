from collections import namedtuple
from data import dialogs

SESSIONS = {}

Dialog = namedtuple('Dialog', ('name', 'incoming', 'lenreq', 'callback'))


def hello(user_id, dialog_name):
    global SESSIONS

    active_dialog = get_active_dialog(user_id)

    if active_dialog:
        bye(user_id)

    SESSIONS[user_id] = Dialog(dialog_name,
                               {0: 1},
                               dialogs.dialog_map[dialog_name]['lenreq'],
                               dialogs.dialog_map[dialog_name]['callback'])

    return {"ok": True, "message": reply(user_id, dialog_name, 0)}


def listen(app, user_id, dialog_name, reply_cntr, phrase_idx):

    active_dialog = get_active_dialog(user_id)

    if active_dialog:
        if active_dialog.name == dialog_name:

            if len(active_dialog.incoming) == active_dialog.lenreq:
                return {"ok": False,
                        "message": "We're not a friends anymore. Say me bye."}

            active_dialog.incoming.update({reply_cntr: phrase_idx})

            response = reply(user_id, dialog_name, reply_cntr)

            if response['question']:
                return {"ok": True, "message": response}
            else:
                bye(user_id,
                    active_dialog.callback(app, user_id,
                                           active_dialog.incoming))
        else:
            return {"ok": False, "message": "Dunno what you want to do."}
    else:
        return {"ok": False, "message": "Start dialog before send me smth."}


def bye(user_id, callback=None, callback_params=None):
    SESSIONS.pop(user_id)

    if callback:
        return callback(callback_params)


def reply(user_id, dialog_name, reply_cntr):

    next_reply_cntr = get_next_reply_cntr(user_id, reply_cntr)

    if next_reply_cntr:
        next_question = dialogs.dialog_map[dialog_name]\
                                          ['questions']\
                                          .get(next_reply_cntr)

    else:
        next_question = None

    return {'question': next_question, 'reply_cntr': next_reply_cntr}


def get_active_dialog(user_id):
    return SESSIONS.get(user_id)


def get_next_reply_cntr(user_id, reply_cntr):

    active_dialog = get_active_dialog(user_id)

    next_idx = reply_cntr + 1

    if not active_dialog.incoming.get(next_idx):
        if next_idx > active_dialog.lenreq + 1:
            next_idx = None
    else:
        next_idx = None

        for i in range(active_dialog.lenreq - 1):
            if not active_dialog.incoming.get(i + 1):
                next_idx = i + 1

    return next_idx



