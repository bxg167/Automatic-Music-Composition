from Tkinter import Tk
from unittest import TestCase

from GUI.ActionButtons import ActionButtons


class TestActionButtons(TestCase):

    def setUp(self):
        self.window = Tk()
        self.actionButtons = ActionButtons(self.window)

    def tearDown(self):
        self.window.destroy()

    def test_set_running(self):
        self.actionButtons.set_running()
        self.assertTrue(self.actionButtons.is_running)

    def test_set_not_running(self):
        self.actionButtons.set_not_running()
        self.assertFalse(self.actionButtons.is_running)
