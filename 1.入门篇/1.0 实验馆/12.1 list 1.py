student = ['Sam', 'Tom', 'Peter', 'Mini']
studentnumber = [1, 2, 3 ,4]
print('students are', student)
print('students numbers are' , studentnumber)

friend = []
friend.append('Amy')
print(friend)
friend.append('David')
print(friend)

my_list = [5, 1, 0.4, 'BUG', friend]
print(my_list)

# print(student[2])
# print(my_list[4])
# print(my_list[4][1])

# print(studentnumber[1:3])
# print(studentnumber[0:4])

student[0] = 'Sally'
print(student)
student[2] = "Pency"
print(student)

my_list.extend(['xxx', 3, 'wgr'])
print(my_list)

friend.insert(1, 'Elex')
print(friend)
friend.insert(1, studentnumber)
print(friend)

student.remove("Tom")
print(student)

del studentnumber[1]
print(studentnumber)

lastMy_list = my_list.pop()
print(my_list)
print(lastMy_list)

second = my_list.pop(1)
print(second)
print(my_list)
