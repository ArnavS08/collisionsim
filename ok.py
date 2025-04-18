import time

abc = "abcdefghijklmnopqrstuvyxyq"
letter = "hello"
found = ""
counter = 0

for letters in letter:
    for char in abc:
        print(found + char)
        counter += 1
        time.sleep(0.07)
        if letters == char:
            found += char
            print(str(counter) + " iterations")
            break