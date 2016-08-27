import base64
import json

left = json.loads("""
        {
            "errors": [
                {"error": "invalid", "field": "e-mail"},
                {"error": "required", "field": "name"}
            ],
            "success": "True",
            "Bermuda":["Hamilton","Somerset","Saint George"]
        }
        """)
right = json.loads("""
        {
            "success": "false",
            "errors": [
                {"error": "required", "field": "name"},
                {"error": "invalid", "field": "email"}
            ],
            "Bermuda":["Hamilton","Saint George","Somerset"]
        }
        """)
left_encode=base64.b64encode(left)
right_encode=base64.b64encode(right)

print(left)
print(right)
print(left_encode)
print(right_encode)
print(base64.b64decode(right)==right)
print(base64.b64decode(left)==left)

# print(base64.urlsafe_b64encode(left))
# print(base64.urlsafe_b64encode(right))