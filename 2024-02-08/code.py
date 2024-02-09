# fun with lists -- run this once and watch the REPL for print output
import time

my_list = ['blue', 'green', 'indigo', 'orange', 'purple', 'red', 'violet', 'yellow']
my_list_length = len(my_list)

print("\n the whole list:", my_list)
time.sleep(1)

print("\n last element:", my_list[-1])
time.sleep(1)

print("\n a slice of the list:", my_list[0:my_list_length//2])
time.sleep(1)

print("\n everything but the last element:", my_list[0:-1])
time.sleep(1)

print("\n everything but the first element:", my_list[1:])
time.sleep(1)

tmp_first = my_list[0] # save the first element
my_list[0:-1] = my_list[1:]  # shift everything to the left
my_list[-1] = tmp_first  # put the first element to the last to 'wrap'

print("\n shift everything to the left:", my_list)
