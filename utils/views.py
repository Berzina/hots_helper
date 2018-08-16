from data.storage import HAPPY_HEROES, BLIZZ_HEROES
from data import update
from utils.filters import take_by_name


def get_hero_view_by_name(name):
    some_heroes = take_by_name(HAPPY_HEROES, name)

    if not some_heroes:
        return 'Found no heroes for you :( Is {} hero name correct?'\
               .format(name)
    elif len(some_heroes) == 1:

        try:
            bh = next(bhero for bhero in BLIZZ_HEROES
                      if bhero.hero.name == some_heroes[0].name)

        except StopIteration:
            return 'Hero {name} is not fully updated by some reason.'\
               .format(name)

        return open_build(bh)
    else:
        return link_build(some_heroes)


def open_build(bh):

    builds_header = '''
* __{}__
```
---------------
 lvl  | talent
      | idx
---------------```'''

    builds_table = '''```
{:^6}|{:^8}
{}
---------------```
'''

    build_full_table = ''

    for build in bh.builds:
        build_full_table += builds_header.format(build.name)

        for talent in build.talents:
            build_full_table += builds_table.format(talent.level, talent.idx,
                                                    talent.name)

        build_full_table += '\n'

    return '''
**{name}**


{btable}
'''.format(name=bh.hero.name,
           btable=build_full_table)


def link_build(some_heroes):
    response = ''

    for hero in some_heroes:
            response += '''
**{name}**


__Builds:__

{blist}


'''\
.format(name=hero.name,
        blist='\n'.join(['* {bname}: {blink}'
                         .format(bname=build.name,
                                 blink=build.link)
                         for build in hero.build_refs]))
