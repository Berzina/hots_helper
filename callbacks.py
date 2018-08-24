def choose(app, user_id, message):
    from utils import filters
    from data.storage import BLIZZ_HEROES

    bheroes = filters.by_choose(BLIZZ_HEROES, message)

    for bhero in bheroes:
        send_hero_profile(app, user_id, bhero)


def echo(app, user_id, message):
    from utils.views import responce_form
    app.send_message(
        user_id,
        responce_form(user_id, message)
    )


def send_hero_profile(app, user_id, bhero):
    from views import represent_stats

    caption = '**{}**\n```{}```'.format(bhero.hero.name,
                                        represent_stats(bhero.hero.stats))

    if bhero.hero.image:
        try:
            app.send_photo(
                user_id,
                photo=bhero.hero.image,
                caption=caption
            )
        except Exception as e:
            print("Can't fetch img: {}.".format(bhero.hero.image))
            print("Reason: {}".format(e))
            app.send_message(
                user_id,
                caption
            )
    else:
        app.send_message(
            user_id,
            caption
        )
