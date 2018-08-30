import pytest
from functools import partial
from pprint import pprint

from dialogs import ichat


cfq_start = partial(ichat.start, "app", 'user_id',
                    'chooseforquick', testing=True)
cfd_start = partial(ichat.start, "app", 'user_id',
                    'choosefordraft', testing=True)
c_receive = partial(ichat.receive, "app", 'query_id', 'user_id',
                    testing=True)

draft_callbacks = {"receive_heroes":
                   ['choosefordraft-map_chosen-14',
                    'choosefordraft-mode_chosen-2',
                    'choosefordraft-skill_chosen-7',
                    'choosefordraft-criteria_chosen-2',
                    'choosefordraft-role_chosen-1',
                    'choosefordraft-exited-0'],

                   "receive_heroes_2":
                   ['choosefordraft-map_chosen-13',
                    'choosefordraft-mode_chosen-2',
                    'choosefordraft-skill_chosen-2',
                    'choosefordraft-criteria_chosen-2',
                    'choosefordraft-role_chosen-1',
                    'choosefordraft-exited-0'],

                   "bye_in_body":
                   ['choosefordraft-map_chosen-14',
                    'choosefordraft-mode_chosen-2',
                    'choosefordraft-skill_chosen-2',
                    'choosefordraft-bye-0',
                    'choosefordraft-criteria_chosen-2',
                    'choosefordraft-role_chosen-1',
                    'choosefordraft-exited-0'],

                   "wrong_callback_seq":
                   ['choosefordraft-map_chosen-14',
                    'choosefordraft-skill_chosen-2',
                    'choosefordraft-role_chosen-1',
                    'choosefordraft-mode_chosen-2',
                    'choosefordraft-criteria_chosen-2',
                    'choosefordraft-exited-0'],

                   "role_changing":
                   ['choosefordraft-map_chosen-14',
                    'choosefordraft-mode_chosen-2',
                    'choosefordraft-skill_chosen-2',
                    'choosefordraft-criteria_chosen-2',
                    'choosefordraft-role_chosen-1',
                    'choosefordraft-exited-2',
                    'choosefordraft-role_chosen-3',
                    'choosefordraft-exited-3']}


def test_ichat_cfd():
    cfd_start()

    for callback in draft_callbacks["receive_heroes"]:
        c_receive(callback)

    cfd_start()

    for callback in draft_callbacks["receive_heroes_2"]:
        c_receive(callback)


@pytest.mark.skip(reason="Tested and good.")
def test_ichat_cfquick():
    cfq_start()
    c_receive('chooseforquick-role_chosen-1')
    c_receive('chooseforquick-survivability_chosen-2')
    c_receive('chooseforquick-utility_chosen-1')
    c_receive('chooseforquick-damage_chosen-3')
    c_receive('chooseforquick-complexity_chosen-3')
    c_receive('chooseforquick-exited-1')
    c_receive('chooseforquick-exited-2')
