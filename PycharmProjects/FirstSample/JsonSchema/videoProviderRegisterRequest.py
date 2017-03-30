from jsonschema import ValidationError
from jsonschema import validate

json_schema = {"type": "object", "additionalProperties": False,
               "required": ["message", "data"],
               "properties": {
                   "message": {
                       "type": "object",
                       "$ref": "#/definitions/messageDefinition"

                   },
                   "data": {
                       "type": "object",
                       "$ref": "#/definitions/dataDefinition"
                   }
               },
               "definitions": {
                   "messageDefinition": {
                       "required": ["type", "id"],
                       "additionalProperties": False,
                       "properties": {
                           "type": {
                               "enum": ["videoProviderRegisterRequest"]
                           },
                           "id": {
                               "type": "string",
                               "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
                           }
                       }
                   },
                   "dataDefinition": {
                       "additionalProperties": False,
                       "required": ["detectorId", "maxTransferQueueSize", "channels"],
                       "properties": {
                           "detectorId": {"type": "string"},
                           "maxTransferQueueSize": {"type": "integer", "minimum": 1},
                           "channels": {
                               "type": "array",
                               "items": {
                                   "$ref": "#/definitions/channelDefinition"
                               }
                           }
                       }
                   },
                   "channelDefinition": {
                       "additionalProperties": False,
                       "properties": {
                           "index": {"type": "integer", "minimum": 1, "maximum": 99},
                           "verificationVideo": {
                               "type": "object",
                               "properties": {
                                   "enabled": {"type": "boolean"}
                               }
                           },
                           "HQVideo": {
                               "type": "object",
                               "properties": {
                                   "enabled": {"type": "boolean"}
                               }
                           }
                       }
                   }
               }
               }

input_data = {"message": {"type": "videoProviderRegisterRequest",
                          "id": "276678da-954a-4865-a1a9-1e54fa9bca40"},
              "data": {"detectorId": "0678", "Asdasdasd": "asdasdasd", "maxTransferQueueSize": 1,
                       "channels": [{"index": 10, "verificationVideo": {"enabled": True}}]}}

try:
    validate(input_data, json_schema)
except ValidationError as e:
    print(e)
