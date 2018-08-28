from transitions import Machine
from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton


class IDialog:

    def __init__(self, user_id):

        self.user_id = user_id

        self.old_answers = {}
        self.answers = {}

        # Initialize the state machine
        self.machine = Machine(model=self,
                               states=self.states,
                               transitions=self.transitions,
                               initial='start')

        self.results = []

        self.next_trigger = None
        self.send_back = []

        self.result_prepared = False

    def send_survey(self):
        print(f"\nState before triggering: {self.state}")

        q = self.dialog[self.state]["q"]
        ans = self.dialog[self.state]["a"]

        self.send_back = [{'text': q,
                          'reply_markup':
                           InlineKeyboardMarkup(
                                self.generate_buttons(
                                    self.dialog_name,
                                    self.dialog[self.state]["trans"],
                                    ans)
                           )}]

    def get_answer(self, given_answer):

        self.old_answers = self.answers.copy()

        print(f"\nCurrent state: {self.state}")

        answer = int(given_answer)

        try:
            human_answer = self.dialog[self.state]['a'][answer - 1]
        except Exception as e:
            print("Unknown answer, try again.")

        if self.is_starting and human_answer == 'No':
            self.trigger('bye')
        else:
            self.answers.update({self.state: human_answer})

            if self.dialog[self.state]["common_next"]:
                self.next_trigger = self.dialog[self.state]['next']
            else:
                self.next_trigger = self.dialog[self.state]['a']\
                                               [answer-1]['next']

            if self.next_trigger == 'bye':
                self.trigger('bye')

            print(f"\nOld answers: {self.old_answers}")
            print(f"\nAnswers: {self.answers}")

        self.send_back = []

# chooseformap_choosing map_idx

    def generate_buttons(self, dialog_name, trigger, variants):
        buttons = []
        button_row = []

        for variant_idx, variant in enumerate(variants):

            if type(variant) == dict:
                variant = variant["text"]

            callback_data = f"{dialog_name}-{trigger}-{variant_idx + 1}"

            if len(button_row) == 2:
                buttons.append(button_row.copy())
                button_row = []

            button_row.append(InlineKeyboardButton(
                variant,
                callback_data=callback_data))

        if button_row:
            buttons.append(button_row)

        if trigger != 'exited':

            end_data = f"{dialog_name}-bye-0"

            buttons.append([InlineKeyboardButton(
                            "Exit",
                            callback_data=end_data)])

        return buttons
