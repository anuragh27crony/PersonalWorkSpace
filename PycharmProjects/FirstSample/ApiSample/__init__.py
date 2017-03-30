# import http.client
# conn = http.client.HTTPSConnection('paypal.com', 443)
# conn.putrequest('GET', '/')
# conn.endheaders() # <---
# r = conn.getresponse()
# print(r.read())


# import http.client
# conn = http.client.HTTPSConnection('paypal.com', 443)
# conn.request('GET', '/') # <---
# r = conn.getresponse()
# print(vars(r.msg))
# print(r.read())

# from decimal import Decimal, getcontext
#
#
#
# d = Decimal(219.92)
# d2 = Decimal(219.52)
# getcontext().prec = 3
# priceDiff = d - d2
# print(d)
# print(d2)
# print(priceDiff)
# cmp = Decimal(0.40)
# c,
# print(cmp)
# getcontext().prec = 3
# if priceDiff.compare(cmp) >= 0:
#     print "YES"
# else:
#     print "NO"
#
# d = Decimal('219.92')
# d2 = Decimal('219.52')
# priceDiff = d - d2
# if priceDiff.compare(Decimal('.40')) >= 0:
#     print "YES"
# else:
#     print "NO"

# print(d - d2)

from decimal import Decimal, ROUND_HALF_EVEN

d = Decimal(219.92).quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)
d2 = Decimal(219.52).quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)
priceDiff = d - d2
cmp = Decimal(0.40).quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)

if priceDiff.compare(cmp) >= 0:
    print "YES"
else:
    print "NO"

print(d)
print(d2)
print(priceDiff)
print(cmp)