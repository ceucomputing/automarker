# Hen3 Problem
# Student B

HENS = int(input('Enter hens: '))
DAYS = 7
REQUIRED_EGGS = 4

grand_sum = 0
hen_sums = [0] * HENS
for i in range(DAYS):
    day = [int(s) for s in input('Enter eggs laid by each hen for day {}: '.format(i + 1)).split(',')]
    day_sum = sum(day)
    print('Day {}   {} egg(s)'.format(i + 1, day_sum))
    grand_sum += day_sum
    for j in range(HENS):
        hen_sums[j] += day[j]
print()
print('Average number of eggs              ' + str(round(grand_sum / HENS)))
print('Total number of eggs for the week   ' + str(grand_sum))
print()
for i in range(HENS):
    if hen_sums[i] < REQUIRED_EGGS:
        print('Hen {}   {} egg(s)'.format(i + 1, hen_sums[i]))
