# Hen3 Problem
# Student D

number_of_hens = int(input('Enter number of hens: '))

if number_of_hens > 0:
    day = input('Enter eggs laid for day 1: ')
    if number_of_hens == 1:
        day1_eggs = int(day)
    elif number_of_hens == 2:
        day1_eggs = [int(day[0]), int(day[3])]
    elif number_of_hens == 3:
        day1_eggs = [int(day[0]), int(day[3]), int(day[6])]
    elif number_of_hens == 4:
        day1_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9])]
    elif number_of_hens == 5:
        day1_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9]), int(day[12])]
    elif number_of_hens == 6:
        day1_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9]), int(day[12]), int(day[15])]
    day = input('Enter eggs laid for day 2: ')
    if number_of_hens == 1:
        day2_eggs = int(day)
    elif number_of_hens == 2:
        day2_eggs = [int(day[0]), int(day[3])]
    elif number_of_hens == 3:
        day2_eggs = [int(day[0]), int(day[3]), int(day[6])]
    elif number_of_hens == 4:
        day2_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9])]
    elif number_of_hens == 5:
        day2_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9]), int(day[12])]
    elif number_of_hens == 6:
        day2_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9]), int(day[12]), int(day[15])]
    day = input('Enter eggs laid for day 3: ')
    if number_of_hens == 1:
        day3_eggs = int(day)
    elif number_of_hens == 2:
        day3_eggs = [int(day[0]), int(day[3])]
    elif number_of_hens == 3:
        day3_eggs = [int(day[0]), int(day[3]), int(day[6])]
    elif number_of_hens == 4:
        day3_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9])]
    elif number_of_hens == 5:
        day3_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9]), int(day[12])]
    elif number_of_hens == 6:
        day3_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9]), int(day[12]), int(day[15])]
    day = input('Enter eggs laid for day 4: ')
    if number_of_hens == 1:
        day4_eggs = int(day)
    elif number_of_hens == 2:
        day4_eggs = [int(day[0]), int(day[3])]
    elif number_of_hens == 3:
        day4_eggs = [int(day[0]), int(day[3]), int(day[6])]
    elif number_of_hens == 4:
        day4_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9])]
    elif number_of_hens == 5:
        day4_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9]), int(day[12])]
    elif number_of_hens == 6:
        day4_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9]), int(day[12]), int(day[15])]
    day = input('Enter eggs laid for day 5: ')
    if number_of_hens == 1:
        day5_eggs = int(day)
    elif number_of_hens == 2:
        day5_eggs = [int(day[0]), int(day[3])]
    elif number_of_hens == 3:
        day5_eggs = [int(day[0]), int(day[3]), int(day[6])]
    elif number_of_hens == 4:
        day5_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9])]
    elif number_of_hens == 5:
        day5_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9]), int(day[12])]
    elif number_of_hens == 6:
        day5_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9]), int(day[12]), int(day[15])]
    day = input('Enter eggs laid for day 6: ')
    if number_of_hens == 1:
        day6_eggs = int(day)
    elif number_of_hens == 2:
        day6_eggs = [int(day[0]), int(day[3])]
    elif number_of_hens == 3:
        day6_eggs = [int(day[0]), int(day[3]), int(day[6])]
    elif number_of_hens == 4:
        day6_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9])]
    elif number_of_hens == 5:
        day6_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9]), int(day[12])]
    elif number_of_hens == 6:
        day6_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9]), int(day[12]), int(day[15])]
    day = input('Enter eggs laid for day 7: ')
    if number_of_hens == 1:
        day7_eggs = int(day)
    elif number_of_hens == 2:
        day7_eggs = [int(day[0]), int(day[3])]
    elif number_of_hens == 3:
        day7_eggs = [int(day[0]), int(day[3]), int(day[6])]
    elif number_of_hens == 4:
        day7_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9])]
    elif number_of_hens == 5:
        day7_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9]), int(day[12])]
    elif number_of_hens == 6:
        day7_eggs = [int(day[0]), int(day[3]), int(day[6]), int(day[9]), int(day[12]), int(day[15])]

print('Day 1   ' + str(sum(day1_eggs)) + ' egg(s)')
print('Day 2   ' + str(sum(day2_eggs)) + ' egg(s)')
print('Day 3   ' + str(sum(day3_eggs)) + ' egg(s)')
print('Day 4   ' + str(sum(day4_eggs)) + ' egg(s)')
print('Day 5   ' + str(sum(day5_eggs)) + ' egg(s)')
print('Day 6   ' + str(sum(day6_eggs)) + ' egg(s)')
print('Day 7   ' + str(sum(day7_eggs)) + ' egg(s)')

print()

if number_of_hens == 1:
    hen1_eggs = day1_eggs + day2_eggs + day3_eggs + day4_eggs + day5_eggs + day6_eggs + day7_eggs
    average_eggs = round(hen1_eggs / number_of_hens)
    print('Average number of eggs              ' + str(average_eggs))
    total_eggs = hen1_eggs
    print('Total number of eggs for the week   ' + str(total_eggs))
elif number_of_hens == 2:
    hen1_eggs = day1_eggs[0] + day2_eggs[0] + day3_eggs[0] + day4_eggs[0] + day5_eggs[0] + day6_eggs[0] + day7_eggs[0]
    hen2_eggs = day1_eggs[1] + day2_eggs[1] + day3_eggs[1] + day4_eggs[1] + day5_eggs[1] + day6_eggs[1] + day7_eggs[1]
    average_eggs = round((hen1_eggs + hen2_eggs) / number_of_hens)
    print('Average number of eggs              ' + str(average_eggs))
    total_eggs = hen1_eggs + hen2_eggs
    print('Total number of eggs for the week   ' + str(total_eggs))
elif number_of_hens == 3:
    hen1_eggs = day1_eggs[0] + day2_eggs[0] + day3_eggs[0] + day4_eggs[0] + day5_eggs[0] + day6_eggs[0] + day7_eggs[0]
    hen2_eggs = day1_eggs[1] + day2_eggs[1] + day3_eggs[1] + day4_eggs[1] + day5_eggs[1] + day6_eggs[1] + day7_eggs[1]
    hen3_eggs = day1_eggs[2] + day2_eggs[2] + day3_eggs[2] + day4_eggs[2] + day5_eggs[2] + day6_eggs[2] + day7_eggs[2]
    average_eggs = round((hen1_eggs + hen2_eggs + hen3_eggs) / number_of_hens)
    print('Average number of eggs              ' + str(average_eggs))
    total_eggs = hen1_eggs + hen2_eggs + hen3_eggs
    print('Total number of eggs for the week   ' + str(total_eggs))
elif number_of_hens == 4:
    hen1_eggs = day1_eggs[0] + day2_eggs[0] + day3_eggs[0] + day4_eggs[0] + day5_eggs[0] + day6_eggs[0] + day7_eggs[0]
    hen2_eggs = day1_eggs[1] + day2_eggs[1] + day3_eggs[1] + day4_eggs[1] + day5_eggs[1] + day6_eggs[1] + day7_eggs[1]
    hen3_eggs = day1_eggs[2] + day2_eggs[2] + day3_eggs[2] + day4_eggs[2] + day5_eggs[2] + day6_eggs[2] + day7_eggs[2]
    hen4_eggs = day1_eggs[3] + day2_eggs[3] + day3_eggs[3] + day4_eggs[3] + day5_eggs[3] + day6_eggs[3] + day7_eggs[3]
    average_eggs = round((hen1_eggs + hen2_eggs + hen3_eggs + hen4_eggs) / number_of_hens)
    print('Average number of eggs              ' + str(average_eggs))
    total_eggs = hen1_eggs + hen2_eggs + hen3_eggs + hen4_eggs
    print('Total number of eggs for the week   ' + str(total_eggs))
elif number_of_hens == 5:
    hen1_eggs = day1_eggs[0] + day2_eggs[0] + day3_eggs[0] + day4_eggs[0] + day5_eggs[0] + day6_eggs[0] + day7_eggs[0]
    hen2_eggs = day1_eggs[1] + day2_eggs[1] + day3_eggs[1] + day4_eggs[1] + day5_eggs[1] + day6_eggs[1] + day7_eggs[1]
    hen3_eggs = day1_eggs[2] + day2_eggs[2] + day3_eggs[2] + day4_eggs[2] + day5_eggs[2] + day6_eggs[2] + day7_eggs[2]
    hen4_eggs = day1_eggs[3] + day2_eggs[3] + day3_eggs[3] + day4_eggs[3] + day5_eggs[3] + day6_eggs[3] + day7_eggs[3]
    hen5_eggs = day1_eggs[4] + day2_eggs[4] + day3_eggs[4] + day4_eggs[4] + day5_eggs[4] + day6_eggs[4] + day7_eggs[4]
    average_eggs = round((hen1_eggs + hen2_eggs + hen3_eggs + hen4_eggs + hen5_eggs) / number_of_hens)
    print('Average number of eggs              ' + str(average_eggs))
    total_eggs = hen1_eggs + hen2_eggs + hen3_eggs + hen4_eggs + hen5_eggs
    print('Total number of eggs for the week   ' + str(total_eggs))
elif number_of_hens == 6:
    hen1_eggs = day1_eggs[0] + day2_eggs[0] + day3_eggs[0] + day4_eggs[0] + day5_eggs[0] + day6_eggs[0] + day7_eggs[0]
    hen2_eggs = day1_eggs[1] + day2_eggs[1] + day3_eggs[1] + day4_eggs[1] + day5_eggs[1] + day6_eggs[1] + day7_eggs[1]
    hen3_eggs = day1_eggs[2] + day2_eggs[2] + day3_eggs[2] + day4_eggs[2] + day5_eggs[2] + day6_eggs[2] + day7_eggs[2]
    hen4_eggs = day1_eggs[3] + day2_eggs[3] + day3_eggs[3] + day4_eggs[3] + day5_eggs[3] + day6_eggs[3] + day7_eggs[3]
    hen5_eggs = day1_eggs[4] + day2_eggs[4] + day3_eggs[4] + day4_eggs[4] + day5_eggs[4] + day6_eggs[4] + day7_eggs[4]
    hen6_eggs = day1_eggs[5] + day2_eggs[5] + day3_eggs[5] + day4_eggs[5] + day5_eggs[5] + day6_eggs[5] + day7_eggs[5]
    average_eggs = round((hen1_eggs + hen2_eggs + hen3_eggs + hen4_eggs + hen5_eggs + hen6_eggs) / number_of_hens)
    print('Average number of eggs              ' + str(average_eggs))
    total_eggs = hen1_eggs + hen2_eggs + hen3_eggs + hen4_eggs + hen5_eggs + hen6_eggs
    print('Total number of eggs for the week   ' + str(total_eggs))

print()

if hen1_eggs < 4:
    print('Hen 1   ' + str(hen1_eggs) + ' egg(s)')
if number_of_hens > 1 and hen2_eggs < 4:
    print('Hen 2   ' + str(hen2_eggs) + ' egg(s)')
if number_of_hens > 2 and hen3_eggs < 4:
    print('Hen 3   ' + str(hen3_eggs) + ' egg(s)')
if number_of_hens > 3 and hen4_eggs < 4:
    print('Hen 4   ' + str(hen4_eggs) + ' egg(s)')
if number_of_hens > 4 and hen5_eggs < 4:
    print('Hen 5   ' + str(hen5_eggs) + ' egg(s)')
if number_of_hens > 5 and hen6_eggs < 4:
    print('Hen 6   ' + str(hen6_eggs) + ' egg(s)')
