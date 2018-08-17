from callbacks import echo

# 0 idx is reserved for hello message!

CLASSIC_ANSWERS = {i: text for i, text
                   in enumerate(['For sure!', "Don't care.", 'No way!'])}

CHOOSE = {'questions': {i + 1: question for i, question in enumerate(
                               [{'q': 'Wanna play specific role?',
                                 'a': {i: text
                                       for i, text
                                       in enumerate(['support',
                                                     'assasin',
                                                     'warrior',
                                                     'specialist'])}},

                                {'q': "How'd you like to be fat? :3",
                                 'a': CLASSIC_ANSWERS},

                                {'q': "Are you kind and pretty lovely today?",
                                 'a': CLASSIC_ANSWERS},

                                {'q': """
Or may be you are angry and want to
release your rage? ^^""",

                                 'a': CLASSIC_ANSWERS},

                                {'q': """
Well do you want to show your incredible
skills? It's no problem if not,
play lazy, friend ^^.""",
                                 'a': CLASSIC_ANSWERS}])
                        },
          'lenreq': 6,
          'callback': echo}


dialog_map = {'choose': CHOOSE}
