week_data = []
for i in range(7):
    day_input = input('Enter data for day ' + str(i + 1) + ' in the format a, b, c, d: ')[::3]
    day_data = []
    for egg in day_input:
        day_data += [int(egg)]
    week_data += [day_data]

grand_total = 0
for i in range(7):
    total = sum(week_data[i])
    grand_total += total
    print('Day ' + str(i) + '   ' + str(total) + ' egg(s)')

print()

print('Average number of eggs              ' + str(round(grand_total / 4)))
print('Total number of eggs for the week   ' + str(grand_total))
