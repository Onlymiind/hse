year = int(input("Year:"))
if year % 100 == 0:
    if year % 400 == 0:
        print("Високосный год")
    else:
        print("Обычный год")
elif year % 4 == 0:
    print("Високосный год")
else:
    print("Обычный год")
