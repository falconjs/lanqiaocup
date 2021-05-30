
list_a = [1, 2, 3, 4, 5]
list_b = ['A', 'B', 'C', 'D', 'E']

for i in list_b:
    print(i)

# list_in_list = [  [1, 2, 3, 4, 5],  [1, 2, 3, 4, 5],  [1, 2, 3, 4, 5]  ]

list_in_list = [
                   [1, 2, 3, 4, 5],
                   [1, 2, 3, 4, 5],
                   [1, 2, 3, 4, 5]
               ]

for i in list_in_list:
    for k in i:
        print(k)