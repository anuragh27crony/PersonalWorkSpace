import os
import unittest

from Test.Utilities import BasicUtils
from Test.jsonComparison import CompareJson


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.utils = BasicUtils()
        self.json_compare=CompareJson()
        self.dirPath=os.path.dirname(os.getcwd())+os.sep
        self.left_file_path=self.dirPath+"left_integ.json"
        self.right_file_path = self.dirPath+"right_integ.json"
        self.msg_success="Success"
        self.msg_leftjson_empty = "Left JSON is empty"
        self.msg_rightjson_empty = "Right JSON is empty"
        self.msg_instance_mismatch = "Left and Right JSON are not same instances"
        self.msg_item_miss = "left Json Item is not present in right Json"
        self.msg_value_mismatch = "Final primitive values are not matching"

    def test_jsoncomparison_emptyjsonfile(self):
        encoded_left_json=""
        encoded_right_json="eyJlbXBsb3llZXMiOlsNCiAgICB7ImZpcnN0TmFtZSI6IkpvaG4iLCAibGFzdE5hbWUiOiJEb2UifSwNCiAgICB7Im" \
                          "ZpcnN0TmFtZSI6IkFubmEiLCAibGFzdE5hbWUiOiJTbWl0aCJ9LA0KICAgIHsiZmlyc3ROYW1lIjoiUGV0ZXIiLCAibGFzd" \
                          "E5hbWUiOiJKb25lcyJ9DQpdfQ=="
        self.utils.save_file(encoded_left_json, self.left_file_path)
        self.utils.save_file(encoded_right_json, self.right_file_path)
        actual_output=self.json_compare.compare_json(self.left_file_path, self.right_file_path)

        left_json=self.utils.read_json_from_file(self.left_file_path)
        right_json=self.utils.read_json_from_file(self.right_file_path)
        expected_output=self.utils.build_output(left_json,right_json,self.msg_leftjson_empty)

        self.assertEquals(expected_output, actual_output)

    def test_jsoncomparison_invalidjsonfile(self):
        encoded_left_json="ew0KICAgICJyZXNzb3VyY2UiOiB7DQogICAgICAgICJ0YWJsZS" \
                          "I6ICJ1c2VycyIsIA0KICAgICAgICAibmFtZSI6ICJhZHJlc3NfYm9vay5kYiINCiAgICB9fQ=="

        encoded_right_json="ew0KICAgICJyZXNzb3VyY2UiOiB7DQogICAgIC" \
                           "ICAgICAibmFtZSI6ICJhZHJlc3NfYm9vay5kYiINCiAgICB9fQ=="
        self.utils.save_file(encoded_left_json, self.left_file_path)

        with self.assertRaises(UnicodeDecodeError):
            self.utils.save_file(encoded_right_json, self.right_file_path)

    def test_jsoncomparison_validjsonfile(self):

        encoded_left_json="ew0KImlkIjogIjAwMDEiLA0KInR5cGUiOiAiZG9udXQiLA0KIm5hbWUiOiAiQ2FrZSIsDQoicHB1IjogMC41NQ0KfQ=="
        encoded_right_json="ew0KImlkIjogIjAwMDEiLA0KInR5cGUiOiAiZG9udXQiLA0KIm5hbWUiOiAiQ2FrZSIsDQoicHB1IjogMC41NQ0KfQ=="

        self.utils.save_file(encoded_left_json, self.left_file_path)
        self.utils.save_file(encoded_right_json, self.right_file_path)
        actual_output=self.json_compare.compare_json(self.left_file_path, self.right_file_path)

        left_json=self.utils.read_json_from_file(self.left_file_path)
        right_json=self.utils.read_json_from_file(self.right_file_path)
        expected_output=self.utils.build_output(left_json, right_json,self.msg_success)
        self.assertEquals(expected_output, actual_output)

    def test_jsoncomparison_missingjsonfile(self):
        encoded_left_json="ew0KICAiZmlyc3ROYW1lIjogIkpvaG4iLA0KICAibGFzdE5hbWUiOiAiU21pdGgiLA0KICAiaXNBbGl2ZSI6IHRydWV9"

        # Override default file path
        self.right_file_path = self.dirPath+"right_integ_missing.json"

        self.utils.save_file(encoded_left_json, self.left_file_path)
        actual_output=self.json_compare.compare_json(self.left_file_path, self.right_file_path)
        left_json=self.utils.read_json_from_file(self.left_file_path)
        right_json=self.utils.read_json_from_file(self.right_file_path)
        expected_output=self.utils.build_output(left_json,right_json,self.msg_rightjson_empty)
        self.assertEquals(expected_output,actual_output)

    def test_jsoncomparison_nonmatching(self):

        encoded_left_json="ew0KImlkIjogIjAwMDEiLA0KInR5cGUiOiAiZG9udXQiLA0KIm5hbWUiOiAiQ2FrZSIsDQoicHB1IjogMC41NQ0KfQ=="
        encoded_right_json="eyJlbXBsb3llZXMiOlsNCiAgICB7ImZpcnN0TmFtZSI6IkpvaG4iLCAibGFzdE5hbWUiOiJEb2UifSwNCiAgICB7Im" \
                          "ZpcnN0TmFtZSI6IkFubmEiLCAibGFzdE5hbWUiOiJTbWl0aCJ9LA0KICAgIHsiZmlyc3ROYW1lIjoiUGV0ZXIiLCAibGFzd" \
                          "E5hbWUiOiJKb25lcyJ9DQpdfQ=="

        self.utils.save_file(encoded_left_json, self.left_file_path)
        self.utils.save_file(encoded_right_json, self.right_file_path)
        actual_output=self.json_compare.compare_json(self.left_file_path, self.right_file_path)

        left_json=self.utils.read_json_from_file(self.left_file_path)
        right_json=self.utils.read_json_from_file(self.right_file_path)
        expected_output=self.utils.build_output(left_json, right_json,self.msg_item_miss)
        self.assertEquals(expected_output, actual_output)