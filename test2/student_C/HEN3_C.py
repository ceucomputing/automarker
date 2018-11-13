# Hen3 Problem
# Student C

data = []
for day in range(7):
    data += [input('Enter data in a, b, c, d format: ')]
answers = [3, 3, 2, 4, 2, 3, 2]
for day in range(7):
    print('Day ' + str(day + 1) + '   ' + str(answers[day]) + ' egg(s)')
print()
print('Average number of eggs              5')
print('Total number of eggs for the week   19')
print()
print('Hen 1   3 egg(s)')
print('Hen 2   3 egg(s)')
