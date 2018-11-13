# Hen3 Problem
# Student A

num_hens = int(input('Enter number of hens: '))

week_data = []
for i in range(7):
    day_input = input('Enter data for day ' + str(i + 1) + ' in a comma-separated format: ')[::3]
    day_data = []
    for egg in day_input:
        day_data += [int(egg)]
    week_data += [day_data]

grand_total = 0
for i in range(7):
    total = sum(week_data[i])
    grand_total += total
    print('Day ' + str(i + 1) + '   ' + str(total) + ' egg(s)')

print()

print('Average number of eggs              ' + str(round(grand_total / num_hens)))
print('Total number of eggs for the week   ' + str(grand_total))

print()

hen_data = [0] * num_hens
for i in range(7):
    for j in range(num_hens):
        hen_data[j] += week_data[i][j]
for i in range(num_hens):
    if hen_data[i] < 4:
        print('Hen ' + str(i + 1) + '   ' + str(hen_data[i]) + ' egg(s)')
