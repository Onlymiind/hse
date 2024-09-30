
def find_matches(men, women):
    if len(men) != len(women):
        print("Внимание, кто-то может остаться без пары.")
        return
    men.sort()
    women.sort()
    print("Идеальные пары:")
    for i in range(len(men)):
        print(men[i], "и", women[i])

men = input("Men: ").split(" ")
women = input("Women: ").split(" ")
find_matches(men, women)