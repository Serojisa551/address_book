phone_number = 'a'
for elm in phone_number:
    if 48 > ord(elm) or ord(elm) > 57:
        print("lox")
    else:
        print(elm)