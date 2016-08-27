from Test.Utilities import BasicUtils


class CompareJson(object):

    def __init__(self):
        # Initializing all error messages
        self.final_errmsg = "Success"
        self.errmsg_json_empty = "JSON is empty"
        self.errmsg_mismatch_instance = "Left and Right JSON are not same instances"
        self.errmsg_element_missing = "left Json Item is not present in right Json"
        self.errmsg_value_mismatch = "Final primitive values are not matching"

    # Method for comparing elements in Left & Right Json recursively.
    def check_json_equal(self, left_json, right_json):
        # Checks for Empty json inputs and register respective error messages
        if left_json is None:
            self.failure_msg("Left %s" % self.errmsg_json_empty)
            return

        if right_json is None:
            self.failure_msg("Right %s" % self.errmsg_json_empty)
            return

        # Check whether left and right Json are of same instance (dict or list)
        if not isinstance(left_json, type(right_json)):
            self.failure_msg(self.errmsg_mismatch_instance)
            return

        # If json is of "dict" instance then extract key from left Json and verify it's presence in right Json.
        if isinstance(left_json, dict):
            for key_leftjson in left_json.keys():
                if right_json.get(key_leftjson) is not None:
                    # For matching key (present in both json) recursively call to compare next level values.
                    self.check_json_equal(left_json[key_leftjson], right_json[key_leftjson])
                else:
                    # A left Json key is missing (not present) in Right Json.
                    self.failure_msg(self.errmsg_element_missing)
                    return
        # If Json is of "List" instance then for every list item extract index from right Json to check the values.
        elif isinstance(left_json, list):
            for item_left_json in left_json:
                try:
                    # Fetch index from right json for list item of left Json (since order can be jumbled)
                    # Recursively call to compare next level of values.
                    index_right_json=right_json.index(item_left_json)
                    self.check_json_equal(item_left_json, right_json[index_right_json])
                except:
                    # Catch exception to report error when a list element from left json is not present in Right Json.
                    self.failure_msg(self.errmsg_element_missing)
                    return
        else:
            # Compare the value of Left Json with Right Json and report error in case of mismatch.
            if left_json != right_json:
                # self.failure_msg('%s -> %s-%s' % (self.errmsg_value_mismatch, left_json, right_json))
                self.failure_msg(self.errmsg_value_mismatch)
                return

    # Method which registers error message during Json Comparison
    def failure_msg(self, error_message=None):
        self.final_errmsg = error_message

    def compare_json(self, path_left_json_file, path_right_json_file):
        utils = BasicUtils()

        # Read json from files
        left_json = utils.read_json_from_file(path_left_json_file)
        right_json = utils.read_json_from_file(path_right_json_file)

        # Check the equality of 2 Json.
        self.check_json_equal(left_json, right_json)

        msg_output=utils.build_output(left_json, right_json,self.final_errmsg)
        return msg_output
