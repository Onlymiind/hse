ticket_number = input("Номер билета:")
digits_list = []
for i in range(len(ticket_number)):
    digits_list.append(int(ticket_number[i]))
if sum(digits_list[:3]) == sum(digits_list[3:]):
    print("Счастливый билет")
else:
    print("Несчастливый билет")
