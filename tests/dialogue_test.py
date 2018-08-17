import unittest
from utils import dialogue

from data.dialogs import *


class TestDialog(unittest.TestCase):

    def setUp(self):
        self.test_id = "1"
        self.test_name = "choose"

    def test_nice_dialogue(self):
        print(dialogue.SESSIONS)
        print(dialogue.hello(self.test_id, self.test_name))

        print("\n\n")
        print(dialogue.SESSIONS)
        print(dialogue.listen(self.test_id, self.test_name, 1, 2))
        print("\n")
        print(dialogue.SESSIONS)
        print(dialogue.listen(self.test_id, self.test_name, 2, 1))
        print("\n")
        print(dialogue.SESSIONS)
        print(dialogue.listen(self.test_id, self.test_name, 3, 0))
        print("\n")
        print(dialogue.SESSIONS)
        print(dialogue.listen(self.test_id, self.test_name, 4, 2))
        print("\n")
        print(dialogue.SESSIONS)
        print(dialogue.listen(self.test_id, self.test_name, 5, 2))
        print("\n")

        print(dialogue.SESSIONS)
        print(dialogue.listen(self.test_id, self.test_name, 1, 2))

    def test_scrumbled_dialogue(self):
        print(dialogue.SESSIONS)
        print(dialogue.hello(self.test_id, self.test_name))

        print("\n\n")
        print(dialogue.SESSIONS)
        print(dialogue.listen(self.test_id, self.test_name, 1, 2))
        print("\n")
        print(dialogue.SESSIONS)
        print(dialogue.listen(self.test_id, self.test_name, 2, 1))
        print("\n")
        print(dialogue.SESSIONS)
        print(dialogue.listen(self.test_id, self.test_name, 3, 0))
        print("\n")
        print("\n")
        print(dialogue.SESSIONS)
        print(dialogue.listen(self.test_id, self.test_name, 2, 1))
        print(dialogue.SESSIONS)
        print(dialogue.listen(self.test_id, self.test_name, 4, 2))
        print("\n")
        print(dialogue.SESSIONS)
        print(dialogue.listen(self.test_id, self.test_name, 5, 2))
        print("\n")

        print(dialogue.SESSIONS)
        print(dialogue.listen(self.test_id, self.test_name, 6, 2))


if __name__ == '__main__':
    unittest.main()
