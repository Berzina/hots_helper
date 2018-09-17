from telegraph import Telegraph

from views import page_pattern
from data.structures import Talent, Talent2, Build

from utils.fetcher import check_image, HOTSDOG_URL

# from html_telegraph_poster import TelegraphPoster
# t = TelegraphPoster()

MY_NAME = 'hotsassistbot'

telegraph = Telegraph()
telegraph.create_account(short_name=MY_NAME)


def make_page(blizzard_hero, build_idx):

    img = blizzard_hero.hero.image
    alt_img = (f'{HOTSDOG_URL}/img/hero_full/'
               f'{blizzard_hero.hero.en_name.lower()}.png')

    print(f"Check image: {check_image(img)}")

    if not check_image(img):
        hero = blizzard_hero.hero._replace(image=alt_img)
        blizzard_hero = blizzard_hero._replace(hero=hero)

    print(f"Image now: {blizzard_hero.hero.image}")

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
