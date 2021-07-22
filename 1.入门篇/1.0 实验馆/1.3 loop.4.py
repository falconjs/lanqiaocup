someInput = input("please input : ")

# print(type(someInput))

print("1. someInput = " + str(someInput))
print("2. --- start of loop --- ")

while someInput != '3':
    print("3. while check pass !")
    print("4. someInput = " + str(someInput))
    someInput = input("5. please input again : ")

    if someInput == '5':
        print("6. continue")
        continue

    if someInput == '0':
        print("7. break")
        break

    print("8. Let's check input : " + str(someInput))
    print("9. --- next loop ---")

print("10. --- end of loop --- ")
print("11. someInput = " + str(someInput))
print()
