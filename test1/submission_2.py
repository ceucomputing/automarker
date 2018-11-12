x = input("Enter x: ")
y = input("Enter y: ")
if not x.isdigit() or not y.isdigit():
    print('Error')
else:
    print(int(x) + int(y))
