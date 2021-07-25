numBlocks = int(input("How many blocks do you want? A:"))
numLines = int(input("How many lines do you want in each block? A2:"))
numStars = int(input("How many stars do you want in each line? A3:"))
for x in range(0, numBlocks):
    for y in range(0,numLines):
        for z in range(0,numStars):
            print("* ", end='')
        print()
    print()