# Hen2 Problem
# Student D

day1 = input('Enter eggs laid for day 1: ')
day1_eggs = [int(day1[0]), int(day1[3]), int(day1[6]), int(day1[9])]
day2 = input('Enter eggs laid for day 2: ')
day2_eggs = [int(day2[0]), int(day2[3]), int(day2[6]), int(day2[9])]
day3 = input('Enter eggs laid for day 3: ')
day3_eggs = [int(day3[0]), int(day3[3]), int(day3[6]), int(day3[9])]
day4 = input('Enter eggs laid for day 4: ')
day4_eggs = [int(day4[0]), int(day4[3]), int(day4[6]), int(day4[9])]
day5 = input('Enter eggs laid for day 5: ')
day5_eggs = [int(day5[0]), int(day5[3]), int(day5[6]), int(day5[9])]
day6 = input('Enter eggs laid for day 6: ')
day6_eggs = [int(day6[0]), int(day6[3]), int(day6[6]), int(day6[9])]
day7 = input('Enter eggs laid for day 7: ')
day7_eggs = [int(day7[0]), int(day7[3]), int(day7[6]), int(day7[9])]

print('Day 1   ' + str(day1_eggs[0] + day1_eggs[1] + day1_eggs[2] + day1_eggs[3]) + ' egg(s)')
print('Day 2   ' + str(day2_eggs[0] + day2_eggs[1] + day2_eggs[2] + day2_eggs[3]) + ' egg(s)')
print('Day 3   ' + str(day3_eggs[0] + day3_eggs[1] + day3_eggs[2] + day3_eggs[3]) + ' egg(s)')
print('Day 4   ' + str(day4_eggs[0] + day4_eggs[1] + day4_eggs[2] + day4_eggs[3]) + ' egg(s)')
print('Day 5   ' + str(day5_eggs[0] + day5_eggs[1] + day5_eggs[2] + day5_eggs[3]) + ' egg(s)')
print('Day 6   ' + str(day6_eggs[0] + day6_eggs[1] + day6_eggs[2] + day6_eggs[3]) + ' egg(s)')
print('Day 7   ' + str(day7_eggs[0] + day7_eggs[1] + day7_eggs[2] + day7_eggs[3]) + ' egg(s)')

print()

hen1_eggs = day1_eggs[0] + day2_eggs[0] + day3_eggs[0] + day4_eggs[0] + day5_eggs[0] + day6_eggs[0] + day7_eggs[0]
hen2_eggs = day1_eggs[1] + day2_eggs[1] + day3_eggs[1] + day4_eggs[1] + day5_eggs[1] + day6_eggs[1] + day7_eggs[1]
hen3_eggs = day1_eggs[2] + day2_eggs[2] + day3_eggs[2] + day4_eggs[2] + day5_eggs[2] + day6_eggs[2] + day7_eggs[2]
hen4_eggs = day1_eggs[3] + day2_eggs[3] + day3_eggs[3] + day4_eggs[3] + day5_eggs[3] + day6_eggs[3] + day7_eggs[3]
average_eggs = (hen1_eggs + hen2_eggs + hen3_eggs + hen4_eggs) // 4
print('Average number of eggs              ' + str(average_eggs))
total_eggs = hen1_eggs + hen2_eggs + hen3_eggs + hen4_eggs
print('Total number of eggs for the week   ' + str(total_eggs))

print()

if hen1_eggs < 4:
    print('Hen 1   ' + str(hen1_eggs) + ' egg(s)')
if hen2_eggs < 4:
    print('Hen 2   ' + str(hen2_eggs) + ' egg(s)')
if hen3_eggs < 4:
    print('Hen 3   ' + str(hen3_eggs) + ' egg(s)')
if hen4_eggs < 4:
    print('Hen 4   ' + str(hen4_eggs) + ' egg(s)')
