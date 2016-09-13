# import http.client
# conn = http.client.HTTPSConnection('paypal.com', 443)
# conn.putrequest('GET', '/')
# conn.endheaders() # <---
# r = conn.getresponse()
# print(r.read())


import http.client
conn = http.client.HTTPSConnection('paypal.com', 443)
conn.request('GET', '/') # <---
r = conn.getresponse()
print(vars(r.msg))
print(r.read())