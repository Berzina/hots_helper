from telegraph import Telegraph

from views import page_pattern

# from html_telegraph_poster import TelegraphPoster
# t = TelegraphPoster()

MY_NAME = 'hotsassistbot'

telegraph = Telegraph()
telegraph.create_account(short_name=MY_NAME)


def make_page(blizzard_hero, build_idx):
    rows = ''
    for talent in blizzard_hero.builds[build_idx].talents:
        rows += page_pattern.ROW_PATTERN.format(talent=talent,
                                                talent_level_emodji=page_pattern.EMODJI_NUMBER_MAPPING[int(talent.level)])

    return page_pattern.PAGE.format(hero=blizzard_hero.hero,
                                    bhero=blizzard_hero,
                                    build=blizzard_hero.builds[build_idx],
                                    rows=rows)


def send_page(title, content):
    title = title if title else MY_NAME

    response = telegraph.create_page(title,
                                     html_content=content)

    return 'https://telegra.ph/{}'.format(response['path'])
