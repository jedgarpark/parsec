# find out your board's MAC address
import wifi
wifi.radio.enabled=True
mac=wifi.radio.mac_address
print("mac is:", mac)  # byte string
print("mac is:", mac.hex())

# want to get fancy?

print(':'.join(f'{byte:02X}' for byte in mac)) # f-string formatted w colons, upper case

'''
 the format line converts each byte to upper case hexadecimal with zero padding
 to keep it two characters wide, using ':' colon seperators

1. Format each byte as hex

f'{byte:02X}'

This is an f-string format specifier:

• byte - the integer value of the byte
•    : - separator for format options
•   02 - pad with zeros to make it at least 2 characters wide
•    x - format as lowercase hexadecimal

So for each byte:

124 becomes '7c'
223 becomes 'df'
161 becomes 'a1'
148 becomes '94'
174 becomes 'ae'
38 becomes '26'

3. Join with colons

':'.join(...)

Takes the list of hex strings ['7c', 'df', 'a1', '94', 'ae', '26'] and joins them with : as the separator.

'''
