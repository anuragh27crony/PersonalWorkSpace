import base64
import json
import os


class BasicUtils(object):
    def __init__(self):
        self.dirPath=os.path.dirname(os.getcwd())+os.sep
        self.left_file_path = self.dirPath+"left.json"
        self.right_file_path = self.dirPath+"right.json"

    def save_left_json(self, file_contents):
        self.save_file(file_contents, self.left_file_path)

    def save_right_json(self, file_contents):
        self.save_file(file_contents, self.right_file_path)

    def save_file(self, file_contents, file_path):
        if file_path is not None:
            with open(file_path, "wt") as file:
                if file_contents is not None:
                    decoded_contents = self.decode_base64(file_contents)
                    file.write(decoded_contents)

    # Method to read json from a given file path.
    def read_json_from_file(self, path_json_file):
        try:
            with open(path_json_file, "r") as file_data:
                json_data = json.load(file_data)
        except:
            json_data = None
        return json_data

    def decode_base64(self, base64_encoded_string):
        return base64.urlsafe_b64decode(base64_encoded_string.encode("UTF-8")).decode("UTF-8")

    def convert_to_json(self,json_object):
        return json.dumps(json_object, indent=4)

    def build_output(self, left_json,right_json, err_msg):
        # Appending Error Message
        if err_msg != "Success":
            err_msg = "Error Message is :"+err_msg
        else:
            err_msg = "Left & Right Json are Matching perfectly"

        if left_json is not None:
            err_msg += "\n JSON OutPut: \n"
            err_msg += self.convert_to_json(left_json)
        elif right_json is not None:
            err_msg += "\n JSON OutPut: \n"
            err_msg += self.convert_to_json(right_json)
        return err_msg
