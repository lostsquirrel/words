import unittest

from user.models import InviteCode


class UserTest(unittest.TestCase):

    def test_invite_code(self):
        c = InviteCode("sfddsaf")
        {**c}