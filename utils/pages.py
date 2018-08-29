from telegraph import Telegraph

from views import page_pattern
from utils.parser import Talent, Talent2, Build

# from html_telegraph_poster import TelegraphPoster
# t = TelegraphPoster()

MY_NAME = 'hotsassistbot'

telegraph = Telegraph()
telegraph.create_account(short_name=MY_NAME)


def make_page(blizzard_hero, build_idx):
    rows = ''

    full_page_pattern = page_pattern.PAGE \
                        if type(blizzard_hero.builds[build_idx]) == Build \
                        else page_pattern.PAGE_2

    for talent in blizzard_hero.builds[build_idx].talents:

        if type(talent) == Talent:
            row_pattern = page_pattern.ROW_PATTERN
        else:
            row_pattern = page_pattern.ROW_PATTERN_2

        rows += row_pattern.format(talent=talent)

    return full_page_pattern.format(hero=blizzard_hero.hero,
                                    bhero=blizzard_hero,
                                    build=blizzard_hero.builds[build_idx],
                                    rows=rows)


def send_page(title, content):
    title = title if title else MY_NAME

    response = telegraph.create_page(title,
                                     html_content=content)

    return 'https://telegra.ph/{}'.format(response['path'])
