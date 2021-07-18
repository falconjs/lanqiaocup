numLines = int(input("How many lines do you want? A:"))
numStars = int(input("How many stars do you want? A2:"))
for x in range(0, numLines):
    for y in range(0,numStars):
        print("*", end='')
    print()