# import requests
# from requests.exceptions import HTTPError
#
# try:
#     headers={"Content-Type":"application/vnd.ttx.det.version.v0+json."}
#     response=requests.get("http://192.168.33.24:8001/v1/admin/status",headers=headers);
#     status_code=response.status_code
#     response_data=response.json()
#     status=response.raise_for_status()
#     print(type(response))
#     print(status_code)
#     print(status)
#     print(response_data)
#     print(response.content)
#     print(response.headers)
#     print(response.history)
# except HTTPError:
#     print("Error is observed")
# except ConnectionError:
#     print("Network disrupted")
# except TimeoutError:
#     print("Timeout")


test=15Minutes