from dialogs.interactive_dialog import IDialog

from utils.statistics import fetch_init, fetch_winrates
from utils import filters
from utils import sorting

from data.storage import BLIZZ_HEROES

import views

ok_answer = 'For sure!'
nvm_answer = "Don't care."
no_answer = 'No way!'

classic_answers = [ok_answer, nvm_answer, no_answer]


def get_maps():
    return fetch_init().get("maps")


def get_build():
    return fetch_init().get("build")


def get_modes():
    modes_dict = fetch_init().get("modes")

    return [modes_dict[str(idx+1)] for idx in range(len(modes_dict))
            if modes_dict[str(idx+1)] != "Quick Match"]


def get_mode_idx(mode_name):
    modes_dict = fetch_init().get("modes", {})

    for idx, name in modes_dict.items():
        if name == mode_name:
            return idx

    return None


class ChooseForDraft(IDialog):

    dialog_name = 'choosefordraft'

    result_repr = views.make_short_hero_profile

    states = ['start',

              'choosing map',
              'map chosen',

              'choosing mode',
              'mode chosen',

              'choosing skill',
              'skill chosen',

              'choosing sorting criteria',
              'sorting criteria chosen',

              'choosing role',
              'role chosen',

              'heroes sent',

              'exiting',
              'exited',

              'end']

    transitions = [

        {'trigger': 'hello',
         'source': 'start',
         'dest': '=',
         'after': 'choose_map'},

        {'trigger': 'choose_map',
         'source': 'start',
         'dest': 'choosing map',
         'after': 'send_survey'},

        {'trigger': 'map_chosen',
         'source': 'choosing map',
         'dest': 'map chosen',
         'before': 'get_answer'},

        {'trigger': 'choose_mode',
         'source': 'map chosen',
         'dest': 'choosing mode',
         'conditions': ['is_map_chosen'],
         'after': 'send_survey'},

        {'trigger': 'mode_chosen',
         'source': 'choosing mode',
         'dest': 'mode chosen',
         'before': 'get_answer'},

        {'trigger': 'choose_skill',
         'source': 'mode chosen',
         'dest': 'choosing skill',
         'after': 'send_survey'},

        {'trigger': 'skill_chosen',
         'source': 'choosing skill',
         'dest': 'skill chosen',
         'before': 'get_answer'},

        {'trigger': 'choose_criteria',
         'source': 'skill chosen',
         'dest': 'choosing sorting criteria',
         'conditions': ['is_map_chosen', 'is_mode_chosen'],
         'after': 'send_survey'},

        {'trigger': 'criteria_chosen',
         'source': 'choosing sorting criteria',
         'dest': 'sorting criteria chosen',
         'before': 'get_answer'},

        {'trigger': 'choose_role',
         'source': ['sorting criteria chosen', 'exiting'],
         'dest': 'choosing role',
         'conditions': ['is_map_chosen'],
         'after': 'send_survey'},

        {'trigger': 'role_chosen',
         'source': 'choosing role',
         'dest': 'role chosen',
         'before': 'get_answer'},

        {'trigger': 'send_heroes',
         'source': ['role chosen', 'exiting'],
         'dest': 'exiting',
         'after': 'get_heroes'},

        {'trigger': 'exit',
         'source': 'heroes sent',
         'dest': 'exiting',
         'after': 'send_survey'},

        {'trigger': 'exited',
         'source': 'exiting',
         'dest': None,
         'after': 'get_answer'},

        {'trigger': 'bye',
         'source': '*',
         'dest': 'end'}
    ]

    dialog = {
              'choosing map': {'q': "Which map do you need?",
                               'a': get_maps(),
                               'trans': 'map_chosen',
                               'next': 'choose_mode',
                               'common_next': True},

              'choosing mode': {'q': "Select the game mode:",
                                'a': get_modes(),
                                'trans': 'mode_chosen',
                                'next': 'choose_skill',
                                'common_next': True},

              'choosing skill': {'q': "Select your skill:",
                                 'a': ['bronze',
                                       'silver',
                                       'gold',
                                       'platinum',
                                       'diamond',
                                       'master',
                                       "don't care"],
                                 'trans': 'skill_chosen',
                                 'next': 'choose_criteria',
                                 'common_next': True},

              'choosing sorting criteria': {'q': 'Choose how to sort:',
                                            'a': ['by winrate percentage',
                                                  'by popularaty',
                                                  'by winned games'],
                                            'trans': 'criteria_chosen',
                                            'next': 'choose_role',
                                            'common_next': True},

              'choosing role': {'q': 'Wanna play specific role?',
                                'a': ['support',
                                      'assassin',
                                      'warrior',
                                      'specialist',
                                      "don't care"],
                                'trans': 'role_chosen',
                                'next': 'send_heroes',
                                'common_next': True},

              'exiting': {'q': 'Exit or more?',
                          'a': [{'text': 'More heroes',
                                 'next': 'send_heroes'},
                                {'text': 'Another role',
                                 'next': 'choose_role'},
                                {'text': 'Exit',
                                 'next': 'bye'}],
                          'trans': 'exited',
                          'common_next': False}}

    def is_map_chosen(self):
        return 'choosing map' in self.answers

    def is_mode_chosen(self):
        return 'choosing mode' in self.answers

    def is_skill_chosen(self):
        return 'choosing skill' in self.answers

    def is_role_chosen(self):
        return 'choosing role' in self.answers

    def is_role_changed(self):
        return self.old_answers.get("choosing role") \
               != self.answers.get("choosing role")

    def get_answer(self, given_answer):

        super().get_answer(given_answer)

        if self.is_map_chosen() \
           and self.is_mode_chosen() \
           and self.is_skill_chosen() \
           and not self.results:

            print("+"*50)
            self.fetch_map_stata()

        if self.is_role_changed():
            self.result_prepared = False

    def fetch_map_stata(self):
        self.all_heroes = []
        self.pointer = 0

        mode_name = self.answers["choosing mode"]

        if self.answers["choosing skill"] != "don't care":
            skill_mapping = {'bronze': 0,
                             'silver': 1,
                             'gold': 2,
                             'platinum': 3,
                             'diamond': 4,
                             'master': 5}

            skill_low = skill_mapping[self.answers["choosing skill"]]
            skill_high = skill_low + 1 if skill_low != 5 else None
        else:
            skill_low = None
            skill_high = None

        heroes_winrates = fetch_winrates(field=self.answers["choosing map"],
                                         mode=get_mode_idx(mode_name),
                                         skill_low=str(skill_low)
                                                   if skill_low else None,
                                         skill_high=str(skill_high)
                                                    if skill_high else None)

        for hero_winrate in heroes_winrates:

            _, bhero = filters.take_by_name(BLIZZ_HEROES,
                                            hero_winrate.hero_name)

            if bhero:
                self.all_heroes.append((bhero, hero_winrate))

        self.results = True

    def get_results(self):

        if self.answers['choosing role'] != "don't care":
            filtered_heroes = [(blizz_hero, hero_winrate)

                               for blizz_hero, hero_winrate
                               in self.all_heroes

                               if blizz_hero.hero.role.lower()
                               == self.answers['choosing role'].lower()]
        else:
            filtered_heroes = self.all_heroes

        if self.answers['choosing sorting criteria'] \
                == 'by winrate percentage':
            sorted_heroes = sorted(filtered_heroes,

                                   key=lambda structure:
                                   structure[1].percent,

                                   reverse=True)

        elif self.answers['choosing sorting criteria'] \
                == 'by popularaty':

            sorted_heroes = sorted(filtered_heroes,

                                   key=lambda structure:
                                   structure[1].count,

                                   reverse=True)

        elif self.answers['choosing sorting criteria'] \
                == 'by winned games':

            sorted_heroes = sorted(filtered_heroes,

                                   key=lambda structure:
                                   structure[1].win_count,

                                   reverse=True)
        else:
            sorted_heroes = []

        self.results = sorted_heroes
        self.result_prepared = True

        for hero, hero_win in self.results:
            print(hero.hero.name)

        print("Ready\n", "*"*50)

    def get_heroes(self):

        print("Getting heroes...")
        print(f"Result prapared? {self.result_prepared}")

        if not self.result_prepared:
            print("Preparing results...")
            self.get_results()

        print("Getting from:\n", "*"*50)
        for hero, hero_win in self.results:
            print(hero.hero.name, hero_win)
        print("*"*50)

        self.send_survey()

        self.send_back = self.results[self.pointer: self.pointer + 3] \
                         + self.send_back

        self.pointer += 3


class ChooseForQuick(IDialog):

    result_repr = views.make_long_hero_profile

    dialog_name = 'chooseforquick'

    states = ['start',

              'choosing role',
              'role chosen',

              'choosing survivability',
              'survivability chosen',

              'choosing utility',
              'utility chosen',

              'choosing damage',
              'damage chosen',

              'choosing complexity',
              'complexity chosen',

              'heroes sent',

              'exiting',
              'exited',

              'end']

    transitions = [

        {'trigger': 'hello',
         'source': 'start',
         'dest': '=',
         'after': 'choose_role'},

        {'trigger': 'choose_role',
         'source': 'start',
         'dest': 'choosing role',
         'after': 'send_survey'},

        {'trigger': 'role_chosen',
         'source': 'choosing role',
         'dest': 'role chosen',
         'before': 'get_answer'},

        {'trigger': 'choose_survivability',
         'source': 'role chosen',
         'dest': 'choosing survivability',
         'after': 'send_survey'},

        {'trigger': 'survivability_chosen',
         'source': 'choosing survivability',
         'dest': 'survivability chosen',
         'before': 'get_answer'},

        {'trigger': 'choose_utility',
         'source': 'survivability chosen',
         'dest': 'choosing utility',
         'after': 'send_survey'},

        {'trigger': 'utility_chosen',
         'source': 'choosing utility',
         'dest': 'utility chosen',
         'before': 'get_answer'},

        {'trigger': 'choose_damage',
         'source': 'utility chosen',
         'dest': 'choosing damage',
         'after': 'send_survey'},

        {'trigger': 'damage_chosen',
         'source': 'choosing damage',
         'dest': 'damage chosen',
         'before': 'get_answer'},

        {'trigger': 'choose_complexity',
         'source': 'damage chosen',
         'dest': 'choosing complexity',
         'after': 'send_survey'},

        {'trigger': 'complexity_chosen',
         'source': 'choosing complexity',
         'dest': 'complexity chosen',
         'before': 'get_answer'},

        {'trigger': 'send_heroes',
         'source': ['complexity chosen', 'exiting'],
         'dest': 'exiting',
         'after': 'get_heroes'},

        {'trigger': 'exit',
         'source': 'heroes sent',
         'dest': 'exiting',
         'after': 'send_survey'},

        {'trigger': 'exited',
         'source': 'exiting',
         'dest': None,
         'after': 'get_answer'},

        {'trigger': 'bye',
         'source': '*',
         'dest': 'end'}
    ]

    dialog = {
              'choosing role': {'q': 'Wanna play specific role?',
                                'a': ['support',
                                      'assassin',
                                      'warrior',
                                      'specialist',
                                      "don't care"],
                                'trans': 'role_chosen',
                                'next': 'choose_survivability',
                                'common_next': True},

              'choosing survivability': {'q': "How'd you like to be fat? :3",
                                         'a': classic_answers,
                                         'trans': 'survivability_chosen',
                                         'next': 'choose_utility',
                                         'common_next': True},

              'choosing utility': {'q':
                                   "Are you kind and pretty lovely today?",

                                   'a': classic_answers,
                                   'trans': 'utility_chosen',
                                   'next': 'choose_damage',
                                   'common_next': True},

              'choosing damage': {'q': "Or may be you are angry and want to "
                                       + "release your rage? ^^",
                                  'a': classic_answers,
                                  'trans': 'damage_chosen',
                                  'next': 'choose_complexity',
                                  'common_next': True},

              'choosing complexity': {'q': "Well do you want to show your "
                                           + "incredible skills? "
                                           + "It's no problem if not, "
                                           + "play lazy, friend ^^",
                                      'a': classic_answers,
                                      'trans': 'complexity_chosen',
                                      'next': 'send_heroes',
                                      'common_next': True},

              'exiting': {'q': 'Exit or more?',
                          'a': [{'text': 'More heroes',
                                 'next': 'send_heroes'},
                                {'text': 'Exit',
                                 'next': 'bye'}],
                          'trans': 'exited',
                          'common_next': False}}

    def get_results(self):

        self.all_heroes = []
        self.pointer = 0

        heroes_winrates = fetch_winrates(mode=get_mode_idx("Quick Match"))

        for hero_winrate in heroes_winrates:

            _, bhero = filters.take_by_name(BLIZZ_HEROES,
                                           hero_winrate.hero_name)

            if bhero:
                self.all_heroes.append((bhero, hero_winrate))

        if self.answers['choosing role'] != "don't care":
            filtered_heroes = [(blizz_hero, hero_winrate)

                               for blizz_hero, hero_winrate
                               in self.all_heroes

                               if blizz_hero.hero.role.lower()
                               == self.answers['choosing role'].lower()]
        else:
            filtered_heroes = self.all_heroes

        sorted_heroes = sorted(filtered_heroes,

                               key=lambda structure:
                               structure[1].percent,

                               reverse=True)

        ok_criteria = [criteria_name.split()[1]
                       for criteria_name, criteria_answer
                       in self.answers.items()
                       if criteria_answer == ok_answer]

        no_criteria = [criteria_name.split()[1]
                       for criteria_name, criteria_answer
                       in self.answers.items()
                       if criteria_answer == no_answer]

        for criteria in no_criteria + ok_criteria:
            reverse = True if criteria in ok_criteria else False
            sorted_heroes = sorted(sorted_heroes,

                                   key=lambda structure:
                                   structure[0].hero.stats._asdict()[criteria],

                                   reverse=reverse)

        self.results = sorted_heroes
        self.result_prepared = True

    def get_heroes(self):

        print("Getting heroes...")
        print(f"Result prapared? {self.result_prepared}")

        if not self.result_prepared:
            print("Preparing results...")
            self.get_results()

        print("Getting from:\n", "*"*50)
        for hero, hero_win in self.results:
            print(hero.hero.name, hero_win)
        print("*"*50)

        self.send_survey()

        self.send_back = self.results[self.pointer: self.pointer + 3] \
                         + self.send_back

        self.pointer += 3
