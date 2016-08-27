import unittest
import json
from json.decoder import JSONDecodeError

from Test.jsonComparison import CompareJson


class JsonEqualityTest(unittest.TestCase):

    def setUp(self):
        self.compare_json = CompareJson()
        self.left_json = ""
        self.right_json = ""
        self.msg_success="Success"
        self.msg_leftjson_empty = "Left JSON is empty"
        self.msg_rightjson_empty = "Right JSON is empty"
        self.msg_instance_mismatch = "Left and Right JSON are not same instances"
        self.msg_item_miss = "left Json Item is not present in right Json"
        self.msg_value_mismatch = "Final primitive values are not matching"

    def test_empty_json_left(self):
        self.left_json = None
        self.right_json=json.loads("""
            {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "title": "Product",
            "description": "A product from Acme's catalog",
            "type": "object",
            "properties": {
                "id": {
                    "description": "The unique identifier for a product",
                    "type": "integer"
                }
            },
            "required": ["id"]
        } """)
        self.compare_json.check_json_equal(self.left_json, self.right_json)
        self.assertEquals(self.msg_leftjson_empty, self.compare_json.final_errmsg)

    def test_empty_json_right(self):
        self.right_json = None
        self.left_json=json.loads("""{
                  "swagger": "2.0",
                  "info": {
                    "version": "1.0.0",
                    "title": "Swagger Petstore",
                    "description": "A sample API that uses a petstore as an example to demonstrate features in the swagger-2.0 specification",
                    "termsOfService": "http://swagger.io/terms/",
                    "contact": {
                      "name": "Swagger API Team",
                      "email": "foo@example.com",
                      "url": "http://madskristensen.net"
                    },
                    "license": {
                      "name": "MIT",
                      "url": "http://github.com/gruntjs/grunt/blob/master/LICENSE-MIT"
                    }
                  }
                }""")
        self.compare_json.check_json_equal(self.left_json, self.right_json)
        self.assertEquals(self.msg_rightjson_empty, self.compare_json.final_errmsg)

    def test_invalid_jsonformat_left(self):
        with self.assertRaises(JSONDecodeError):
            self.left_json=json.loads("""
                {
                    "name":"Product",
                    "properties":
                    {
                "id":
                {
                        "type":"number",
                        "description":"Product identifier",
                        "required":true
                },
                "name":
                {
                        "description":"Name of the product",
                        "type":"string",
                        "required":true
                }
                """)

    def test_invalid_jsonformat_right(self):
        with self.assertRaises(JSONDecodeError):
            self.right_json=json.loads("""
                {
                    "name": "mledoze/countries",
                    "version": "1.7.7",
                    "description": "World countries in JSON, CSV, XML and Yaml",
                    "keywords": ["world", "countries", "json", "csv", "xml", "yaml"],
                    "homepage": "https://mledoze.github.io/countries/",
                    "license": "Open Database License",
                    "authors": [
                        {"name": "Mohammed Le Doze"}
                    ]
                """)

    def test_mismatching_jsonEntities(self):
        self.left_json = json.loads("""
                [
            {
                "color": "red",
                "value": "#f00"
            }
        ]
        """)

        self.right_json = json.loads("""
            {
                "color": "red",
                "value": "#f00"
            }
        """)
        self.compare_json.check_json_equal(self.left_json, self.right_json)
        self.assertEquals(self.msg_instance_mismatch, self.compare_json.final_errmsg)

    def test_identical_jsonEntities(self):
        self.left_json=json.loads("""{
                "id": "0001",
                "type": "donut",
                "name": "Cake",
                "ppu": 0.55,
                "batters":
                    {
                        "batter":
                            [
                                { "id": "1001", "type": "Regular" },
                                { "id": "1002", "type": "Chocolate" },
                                { "id": "1003", "type": "Blueberry" },
                                { "id": "1004", "type": "Devil's Food" }
                            ]
                    }}""")

        self.right_json=json.loads("""{
                "id": "0001",
                "type": "donut",
                "name": "Cake",
                "ppu": 0.55,
                "batters":
                    {
                        "batter":
                            [
                                { "id": "1001", "type": "Regular" },
                                { "id": "1002", "type": "Chocolate" },
                                { "id": "1003", "type": "Blueberry" },
                                { "id": "1004", "type": "Devil's Food" }
                            ]
                    }}""")
        self.compare_json.check_json_equal(self.left_json, self.right_json)
        self.assertEquals(self.msg_success, self.compare_json.final_errmsg)

    def test_unordered_matching_jsonEntities(self):
        self.left_json = json.loads("""
            {
            "errors": [
                {"error": "invalid", "field": "email"},
                {"error": "required", "field": "name"}
            ],
            "success": false
            }""")
        self.right_json = json.loads("""
            {
            "success": false,
            "errors": [
                {"field": "name","error": "required"},
                {"error": "invalid", "field": "email"}
            ]
            }""")
        self.compare_json.check_json_equal(self.left_json, self.right_json)
        self.assertEquals(self.msg_success, self.compare_json.final_errmsg)

    def test_elements_missing_json(self):
        self.left_json = json.loads("""
                {"name": {
                    "common": "Puerto Rico",
                    "official": "Commonwealth of Puerto Rico",
                    "native": {
                        "eng": {
                            "official": "Commonwealth of Puerto Rico",
                            "common": "Puerto Rico"
                        },
                        "spa": {
                            "official": "Estado Libre Asociado de Puerto Rico",
                            "common": "Puerto Rico"
                        }
                    }
                },
                "tld": [".pr"],
                "callingCode": ["1787", "1939"]}
                """)

        self.right_json = json.loads("""
                {"name": {
                    "common": "Puerto Rico",
                    "official": "Commonwealth of Puerto Rico",
                    "native": {
                        "eng": {
                            "official": "Commonwealth of Puerto Rico",
                            "common": "Puerto Rico"
                        },
                        "spa": {
                            "official": "Estado Libre Asociado de Puerto Rico",
                            "common": "Puerto Rico"
                        }
                    }
               }
            }
                """)
        self.compare_json.check_json_equal(self.left_json, self.right_json)
        self.assertEquals(self.msg_item_miss, self.compare_json.final_errmsg)

    def test_diffVal_sameKey_json(self):
        self.left_json = json.loads("""
            {
             "firstName": "John",
             "lastName": "Smith",
             "age": 25,
             "address":
             {
                 "streetAddress": "21 2nd Street",
                 "city": "New York",
                 "state": "NY",
                 "postalCode": "10021"
             }
            }
        """)
        self.right_json = json.loads("""
        {
             "firstName": "Agent",
             "lastName": "Smith",
             "age": 45,
             "address":
             {
                 "streetAddress": "21 2nd Street",
                 "city": "New York",
                 "state": "NY",
                 "postalCode": "10021"
             }
            }
        """)
        self.compare_json.check_json_equal(self.left_json, self.right_json)
        self.assertEquals(self.msg_value_mismatch, self.compare_json.final_errmsg)

    def test_idential_simpleJson(self):
        self.left_json = json.loads("""
            {
            "id": 1,
            "name": "A green door",
            "price": 12.50,
            "tags": ["home", "green"]
            }
        """)
        self.right_json = json.loads("""
            {
            "id": 1,
            "name": "A green door",
            "price": 12.50,
            "tags": ["home", "green"]
            }
        """)
        self.compare_json.check_json_equal(self.left_json, self.right_json)
        self.assertEquals(self.msg_success, self.compare_json.final_errmsg)

    def test_identical_arrayJson(self):
        self.left_json = json.loads("""
            [
            {
                "color": "red",
                "value": "#f00"
            },
            {
                "color": "green",
               "value": "#0f0"
            },
            {
                "color": "blue",
                "value": "#00f"
            }]
        """)
        self.right_json = json.loads("""
            [
            {
                "color": "red",
                "value": "#f00"
            },
            {
                "color": "green",
               "value": "#0f0"
            },
            {
                "color": "blue",
                "value": "#00f"
            }]
        """)
        self.compare_json.check_json_equal(self.left_json, self.right_json)
        self.assertEquals(self.msg_success, self.compare_json.final_errmsg)

if __name__ == '__main__':
    unittest.main()
