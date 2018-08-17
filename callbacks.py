def choose(app, user_id, message):
    from utils import filters
    from data.storage import BLIZZ_HEROES

    bheroes = filters.by_choose(BLIZZ_HEROES, message)

    response = 'You can play them:\n{}'.format('\n'.join(
                                               [bhero.hero.name
                                                for bhero in bheroes]))

    app.send_message(
        user_id,
        response
    )


def echo(app, user_id, message):
    from utils.views import responce_form
    app.send_message(
        user_id,
        responce_form(user_id, message)
    )
