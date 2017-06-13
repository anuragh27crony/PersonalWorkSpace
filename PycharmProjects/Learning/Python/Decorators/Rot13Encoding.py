d = {}
for c in (65, 97):
    for i in range(26):
        print(chr(i+c) +"=>"+chr((i+13) % 26 + c))

