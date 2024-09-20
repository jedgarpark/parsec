# List comprehension
# create a new list based on an existing list in just one line
import time

orig_list = [True, False, True, False, True, False, True, False, False, True, True]
print("\noriginal list:", orig_list)
time.sleep(3)

# the loop way:
# new_loop_list = []  
# for x in orig_list:
#     if x is True:
#         new_loop_list.append("T")
#     else:
#         new_loop_list.append("F")
# print("new loop list", new_loop_list)
# time.sleep(1)

# the list comprehension way:
new_comp_list = ["T" if x else "F" for x in orig_list]
print("new comp list", new_comp_list)
time.sleep(2)

neat_list = ''.join(new_comp_list)
print("neat list:", neat_list)
time.sleep(2)
