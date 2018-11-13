# Hen1 Problem
# Student B

HENS = 4
DAYS = 7

grand_sum = 0
for i in range(DAYS):
    day_sum = sum(int(s) for s in input('Enter eggs laid by each hen for day {}: '.format(i + 1)).split(','))
    print('Day {}   {} egg(s)'.format(i + 1, day_sum))
    grand_sum += day_sum
print()
print('Average number of eggs              ' + str(round(grand_sum / HENS)))
print('Total number of eggs for the week   ' + str(grand_sum))
