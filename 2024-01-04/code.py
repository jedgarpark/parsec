# CircuitPython Parsec
# split() a string into a list of strings based on a separator (default is whitespace)

import time
print("\n")

sentence = "This is a neat CircuitPython trick"
print(sentence)
time.sleep(1)
print("\n")

words = sentence.split()  # create a list named 'words'
print(words)
time.sleep(0.75)
print("\n")

for word in words:
    print(word)
    time.sleep(0.25)

print("\nThe sentence has", len(words), "words in it.")
