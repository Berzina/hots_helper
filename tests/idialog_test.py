import unittest
from dialogs.choose_by_map import ChooseByMap

from dialogs import ichat


class TestIDialog(unittest.TestCase):

    # def test_machine(self):
    #     self.dialog = ChooseByMap(123)
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
    #     ichat.start("smth", 123, 'choosebymap', True)

    #     ichat.receive("smth", 123, 123, 'choosebymap-hello_chosen-1', True)
    #     ichat.receive("smth", 123, 123, 'choosebymap-map_chosen-14', True)
    #     ichat.receive("smth", 123, 123, 'choosebymap-criteria_chosen-2', True)
    #     ichat.receive("smth", 123, 123, 'choosebymap-role_chosen-3', True)
    #     ichat.receive("smth", 123, 123, 'choosebymap-exited-0', True)
    #     ichat.receive("smth", 123, 123, 'choosebymap-exited-2', True)

    # def test_ichat_bye_in_body(self):
    #     ichat.start("smth", 123, 'choosebymap', True)

    #     ichat.receive("smth", 123, 123, 'choosebymap-hello_chosen-1', True)
    #     ichat.receive("smth", 123, 123, 'choosebymap-map_chosen-14', True)
    #     ichat.receive("smth", 123, 123, 'choosebymap-bye-0', True)
    #     ichat.receive("smth", 123, 123, 'choosebymap-criteria_chosen-2', True)
    #     ichat.receive("smth", 123, 123, 'choosebymap-role_chosen-3', True)
    #     ichat.receive("smth", 123, 123, 'choosebymap-exited-0', True)
    #     ichat.receive("smth", 123, 123, 'choosebymap-exited-2', True)

    # def test_ichat_wrong_callback_seq(self):
    #     ichat.start("smth", 123, 'choosebymap', True)

    #     ichat.receive("smth", 123, 123, 'choosebymap-hello_chosen-1', True)
    #     ichat.receive("smth", 123, 123, 'choosebymap-map_chosen-14', True)
    #     ichat.receive("smth", 123, 123, 'choosebymap-role_chosen-3', True)
    #     ichat.receive("smth", 123, 123, 'choosebymap-criteria_chosen-2', True)
    #     ichat.receive("smth", 123, 123, 'choosebymap-exited-0', True)
    #     ichat.receive("smth", 123, 123, 'choosebymap-exited-2', True)

    def test_ichat_role_changing(self):
        ichat.start("smth", 123, 'choosebymap', True)

        ichat.receive("smth", 123, 123, 'choosebymap-hello_chosen-1', True)
        ichat.receive("smth", 123, 123, 'choosebymap-map_chosen-14', True)
        ichat.receive("smth", 123, 123, 'choosebymap-criteria_chosen-2', True)
        ichat.receive("smth", 123, 123, 'choosebymap-role_chosen-1', True)
        ichat.receive("smth", 123, 123, 'choosebymap-exited-2', True)
        ichat.receive("smth", 123, 123, 'choosebymap-role_chosen-3', True)
        ichat.receive("smth", 123, 123, 'choosebymap-exited-3', True)



if __name__ == '__main__':
    unittest.main()
