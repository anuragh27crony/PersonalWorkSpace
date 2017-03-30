import jsonschema

from jsonschema import ValidationError
from jsonschema import validate

json_schema = {"type": "object", "additionalProperties": False,
               "required": ["message", "data", "success"],
               "properties": {
                   "success": {"type": "boolean"},
                   "message": {
                       "type": "object",
                       "$ref": "#/definitions/messageDefinition"
                   },
                   "data": {
                       "type": "object",
                       "properties": {
                           "fragments": {
                               "type": "array",
                               "items": {
                                   "$ref": "#/definitions/fragmentDefinition"
                               }
                           }
                       }
                   }
               },
               "definitions": {
                   "messageDefinition": {
                       "required": ["type", "id"],
                       "additionalProperties": False,
                       "properties": {
                           "type": {
                               "enum": ["videoUploadReply"]
                           },
                           "id": {
                               "type": "string",
                               "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
                           }
                       }
                   },
                   "dataDefinition": {
                       "required": ["fragments"],
                       "properties": {
                           "fragments": {
                               "type": "array",
                               "items": {
                                   "$ref": "#/definitions/fragmentDefinition"
                               }
                           }
                       }
                   },
                   "fragmentDefinition": {
                       "additionalProperties": False,
                       "required": ["startDateTime", "endDateTime", "size", "location"],
                       "properties": {
                           "startDateTime": {"type": "string", "format": "date-time"},
                           "endDateTime": {"type": "string", "format": "date-time"},
                           "size": {"type": "integer", "minimum": 1},
                           "location": {"type": "string"}
                       }
                   }
               }
               }

input_data = {"success": True, "message": {"type": "videoUploadReply", "id": "dcbaedf5-3e13-4807-b8ed-5c6848f88f6d"},
              "data": {"fragments": [{"startDateTime": "2016-09-13T10:40:00Z",
                                      "location": "D:/civolution/Data/VerificationVideo/01/160913/10/WcT0768160913104000_01.mp4",
                                      "endDateTime": "2016-09-13T10:41:00Z", "size": 509514},
                                     {"startDateTime": "2016-09-13T10:41:00Z",
                                      "location": "D:/civolution/Data/VerificationVideo/01/160913/10/WcT0768160913104100_01.mp4",
                                      "endDateTime": "2016-09-13T10:42:00Z", "size": 502532},
                                     {"startDateTime": "2016-09-13T10:42:00Z",
                                      "location": "D:/civolution/Data/VerificationVideo/01/160913/10/WcT0768160913104200_01.mp4",
                                      "endDateTime": "2016-09-13T10:43:00Z",
                                      "size": 496151}]}}

try:
    validate(input_data, json_schema, format_checker=jsonschema.FormatChecker())
except ValidationError as e:
    print(e)
