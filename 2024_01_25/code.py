# sorted()
import time

seperator = ", "
answers = []

time.sleep(1)
print()

# Prompt for input
for i in range(4):
    answer = input("Enter answer {}: ".format(i + 1))
    answers.append(answer)

sorted_answers = sorted(answers)
reversed_answers = sorted(answers, reverse=True)

# Print the four answers in one line
print("\noriginal:", seperator.join(answers))
print("  sorted:", seperator.join(sorted_answers))
print("reversed:", seperator.join(reversed_answers))
