import json
import unittest

from utils import CustomEncoder, Paging, ValidationError, generate_uuid, Validator


class UtilsTest(unittest.TestCase):

    def test_uuid(self):
        print(generate_uuid())
        self.assertEqual(len(generate_uuid()), 32)

    def test_valiate(self):
        form = dict(
            a=1,
            b=2,
            c=3
        )
        v = Validator().rule("a").rule("b").rule("c").rule("d", False, 4)
        _a, _b, _c, _d = v.validate_form(form)
        self.assertEqual(_a, 1)
        self.assertEqual(_b, 2)
        self.assertEqual(_c, 3)
        self.assertEqual(_d, 4)

    def test_validate_none_form(self):
        v = Validator().rule("page", False, 1).rule("per_page", False, 10)
        page, per_page = v.validate_form(None)
        self.assertEqual(page, 1)
        self.assertEqual(per_page, 10)

    def test_validate_none_form_required(self):
        v = Validator().rule("page")
        try:
            v.validate_form(None)
        except ValidationError as e:
            print(e)
        try:
            v.validate_form(dict(size=2))
        except ValidationError as e:
            print(e)

    def test_extend(self):
        try:
            [].extend(None)
        except TypeError as e:
            print(e)

    def test_paging(self):
        p = Paging(101, 1, 10)
        print(json.dumps(p.__dict__))
    
    def test_json_encode(self):
        p = Paging(101, 1, 10)
        print(CustomEncoder().encode(p))
        