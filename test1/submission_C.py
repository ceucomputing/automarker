# Addition Problem
# Student C

x = input("Enter x: ").strip()
y = input("Enter y: ").strip()
if len(x) > 0 and (x[0] == '-' or x[0].isdigit()) and (len(x) < 2 or x[1:].isdigit()) and len(y) > 0 and (y[0] == '-' or y[0].isdigit()) and (len(y) < 2 or y[1:].isdigit()):
    print(int(x) + int(y))
else:
    print('Error')
