import os
import unittest

from Test.Utilities import BasicUtils


class UtilitiesTest(unittest.TestCase):
    def setUp(self):
        self.utils = BasicUtils()
        self.left_json = ""
        self.right_json = ""


    def test_null_base64decode(self):
        base64_String="bnVsbA=="
        expected_value="null"
        decoded_string=self.utils.decode_base64(base64_String)
        self.assertEquals(expected_value,decoded_string)

    def test_valid_base64decode(self):
        base64_String="amUgbmUgbGUgdHJvdXZlIHBhcyBuZWNlc3NhaXJlIGRldmVuaXIgdsOpZ8OpdGFyaWVuIHBvdXIgw6p0cmUgZW4gYm9ubmUgc2FudMOp"
        expected_value="je ne le trouve pas necessaire devenir végétarien pour être en bonne santé"
        decoded_string=self.utils.decode_base64(base64_String)
        self.assertEquals(expected_value,decoded_string)

    def test_invalid_base64decode(self):
        base64_string="VGhpcyBpyBjb21wbGV0ZWx5IGZpbmU=="
        with self.assertRaises(UnicodeDecodeError):
            self.utils.decode_base64(base64_string)

    def test_mismatch_base64decode(self):
        base64_String="SXNzdWUgd2FzIGNhdXNlZCBieSBhbiBpbnRlcm5hbCBjb21wYXRpYmlsaXR5"
        expected_value="But that can’t stop us from changing"
        decoded_string=self.utils.decode_base64(base64_String)
        self.assertNotEquals(expected_value, decoded_string)

    def test_save_empty_filepath(self):
        file_contents="Testing"
        file_path=None
        self.utils.save_file(file_contents, file_path)

    def test_save_empty_filecontents(self):
        file_contents=None
        file_path=os.path.dirname(os.getcwd())+os.sep+"unit.test"
        self.utils.save_file(file_contents, file_path)
        self.assertIsNone(self.utils.read_json_from_file(file_path))

    def test_read_empty_filepath(self):
        file_path=None
        file_contents=self.utils.read_json_from_file(file_path)
        self.assertIsNone(file_contents)