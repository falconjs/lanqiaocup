# for looper in [1, 2, 3, 4, 5]:
#     print(str(looper) + ' times 8 = ' + str(looper * 8))
#     print(looper, 'times 8 =', looper * 8)

first = "a"
second = "b"
third = "c"

for i in [first, second, third]:
    print(i)

for num, i in enumerate([first, second, third]):
    print(num, i)
