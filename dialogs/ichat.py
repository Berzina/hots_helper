from transitions.core import MachineError
from dialogs.choosers import ChooseForDraft, ChooseForQuick

import views

SESSIONS = {}

dialog_mapping = {'choosefordraft': ChooseForDraft,
                  'chooseforquick': ChooseForQuick}


def start(app, user_id, dialog_name, testing=False):
    global SESSIONS

    if user_id in SESSIONS:
        SESSIONS.pop(user_id)

    active_dialog = dialog_mapping[dialog_name](user_id)

    SESSIONS[user_id] = active_dialog

    active_dialog.hello()

    for response in active_dialog.send_back:
        send(app, None, user_id, response, None, testing)


def receive(app, query_id, user_id, query_data, testing=False):
    global SESSIONS

    dialog_name, trigger, answer_idx = query_data.split("-")

    if user_id not in SESSIONS:
        app.answer_callback_query(query_id)
        app.send_message(user_id, 'Start dialog to send me something.')
        return

    active_dialog = SESSIONS[user_id]

    print(f"Received trigger: {trigger} ({answer_idx})")
    try:
        active_dialog.trigger(trigger, answer_idx)
    except MachineError as e:
        send_error(app, query_id, user_id, "Did you just misclick?", testing)

    print(f"State after trigger: {active_dialog.state}")

    if active_dialog.state == 'end':
        SESSIONS.pop(user_id)
        if not testing:
            app.answer_callback_query(query_id)
            app.send_message(user_id, "Thanks for using me ^^")
    else:
        print(f"Next trigger: {active_dialog.next_trigger}")
        try:
            active_dialog.trigger(active_dialog.next_trigger)
        except MachineError as e:
            send_error(app, query_id, user_id,
                       "Did you just misclick?", testing)

        for response in active_dialog.send_back:
            send(app, query_id, user_id, response, active_dialog.result_repr,
                 testing)


def send(app, query_id, user_id, message, repr_method=None, testing=False):
    if query_id and not testing:
        app.answer_callback_query(query_id)

    if 'reply_markup' in message:
        if not testing:
            app.send_message(user_id, **message)
        else:
            print(f"Sending: {message['reply_markup']}")
    else:
        if not testing:
            views.send_view(app, user_id, repr_method, *message)
        else:
            print(f"Sending: {repr_method(*message)}")


def send_error(app, query_id, user_id, message, testing=False):
    if not testing:
        if query_id:
            app.answer_callback_query(query_id)
        app.send_message(user_id, message)
    else:
        print(message)
