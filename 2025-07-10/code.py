# Formatting strings with .replace()
import time

#original message, such as a sensor or wireless message
message = "STATUS_OK"
print("\n original:", message)
time.sleep(1)

# replace underscore with space
display_msg = message.replace("_", " ")
print("\n replaced:", display_msg)
time.sleep(1)

# replace and make message lower case
lowercase_msg = message.replace("_", " ").lower()
print("\n replaced, lowercased:", lowercase_msg)
