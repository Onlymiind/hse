word = input("Word:")
length = len(word)
if length % 2 == 0:
    print(word[length // 2] + word[(length // 2) + 1])
else:
    print(word[length // 2])