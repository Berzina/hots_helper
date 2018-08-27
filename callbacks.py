def choose(app, user_id, message):
    from utils import filters
    from views import send_view, get_hero_profile
    from data.storage import BLIZZ_HEROES

    bheroes = filters.by_choose(BLIZZ_HEROES, message)

    for bhero in bheroes:
        send_view(app, user_id, get_hero_profile, bhero.hero.name)


def echo(app, user_id, message):
    from utils.views import responce_form
    app.send_message(
        user_id,
        responce_form(user_id, message)
    )
