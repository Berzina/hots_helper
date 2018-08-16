def take_by_name(happy_heroes, name):
    matching = [hero for hero in happy_heroes
                if name.lower() in hero.name.lower()]

    def match_score(hero):
        ru_pos = hero.ru_name.lower().find(name.lower())
        en_pos = hero.en_name.lower().find(name.lower())

        return ru_pos if ru_pos > en_pos else en_pos

    matching.sort(key=lambda x: match_score(x))

    return matching
