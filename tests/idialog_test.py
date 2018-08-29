import unittest
from dialogs.choosers import ChooseForDraft

from dialogs import ichat


class TestIDialog(unittest.TestCase):

    # def test_machine(self):
    #     self.dialog = choosefordraft(123)
    #     self.dialog.hello()
    #     self.dialog.hello_chosen(1)

    #     print(self.dialog)

    #     self.dialog.choose_map()
    #     self.dialog.map_chosen(7)

    #     self.dialog.choose_role()
    #     self.dialog.role_chosen(3)

    #     self.dialog.choose_criteria()
    #     self.dialog.criteria_chosen(1)

    #     self.dialog.bye()

    #     print(self.dialog.results)

    # def test_ichat_2_heroes_receiving(self):
    #     ichat.start("smth", 123, 'choosefordraft', True)

    #     ichat.receive("smth", 123, 123, 'choosefordraft-hello_chosen-1', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-map_chosen-14', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-criteria_chosen-2', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-role_chosen-3', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-exited-0', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-exited-2', True)

    # def test_ichat_bye_in_body(self):
    #     ichat.start("smth", 123, 'choosefordraft', True)

    #     ichat.receive("smth", 123, 123, 'choosefordraft-hello_chosen-1', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-map_chosen-14', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-bye-0', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-criteria_chosen-2', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-role_chosen-3', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-exited-0', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-exited-2', True)

    # def test_ichat_wrong_callback_seq(self):
    #     ichat.start("smth", 123, 'choosefordraft', True)

    #     ichat.receive("smth", 123, 123, 'choosefordraft-hello_chosen-1', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-map_chosen-14', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-role_chosen-3', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-criteria_chosen-2', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-exited-0', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-exited-2', True)

    # def test_ichat_role_changing(self):
    #     ichat.start("smth", 123, 'choosefordraft', True)

    #     ichat.receive("smth", 123, 123, 'choosefordraft-map_chosen-14', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-mode_chosen-2', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-criteria_chosen-2', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-role_chosen-1', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-exited-2', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-role_chosen-3', True)
    #     ichat.receive("smth", 123, 123, 'choosefordraft-exited-3', True)

    def test_ichat_cfquick(self):
        ichat.start("smth", 123, 'chooseforquick', True)

        ichat.receive("smth", 123, 123, 'choosefordraft-role_chosen-1', True)
        ichat.receive("smth", 123, 123, 'choosefordraft-survivability_chosen-2', True)
        ichat.receive("smth", 123, 123, 'chooseforquick-utility_chosen-1', True)
        ichat.receive("smth", 123, 123, 'chooseforquick-damage_chosen-3', True)
        ichat.receive("smth", 123, 123, 'chooseforquick-complexity_chosen-3', True)
        ichat.receive("smth", 123, 123, 'chooseforquick-exited-1', True)
        ichat.receive("smth", 123, 123, 'chooseforquick-exited-2', True)


if __name__ == '__main__':
    unittest.main()
