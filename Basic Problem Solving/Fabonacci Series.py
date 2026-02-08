num = int(input("enter index"))
a = 1
b = 1
for i in range(3, num+1):
    c = a+b
    a = b
    b = c
print(c)
    