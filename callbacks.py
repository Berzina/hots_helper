def choose(app, user_id, message):
    from utils import filters
    from data.storage import BLIZZ_HEROES
    from views import represent_stats

    bheroes = filters.by_choose(BLIZZ_HEROES, message)

    # response = 'You can play them:\n{}'.format('\n'.join(
    #                                            [bhero.hero.name
    #                                             for bhero in bheroes]))

    for bhero in bheroes:
        caption = '**{}**\n{}'.format(bhero.hero.name,
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


def echo(app, user_id, message):
    from utils.views import responce_form
    app.send_message(
        user_id,
        responce_form(user_id, message)
    )
