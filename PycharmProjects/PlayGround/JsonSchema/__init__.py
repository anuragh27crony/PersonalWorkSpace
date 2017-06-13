from jsonschema import ValidationError
from jsonschema import validate

schema = {"type": "object", "additionalProperties": False,
          "properties": {"success": {"type": "boolean"}, "price": {"type": "number"}, "name": {"type": "string"},
                         "channels": {"type": "array", "minItems": 1}}}

try:
    validate({"name": "Eggs", "channel": []}, schema)
    validate({"name": "Eggs", "channels": []}, schema)
except ValidationError as e:
    print(e)