mylist = ['d', '1','7', 'b', 'B', 'be', 'wa', '2', '12', '', '$', '*']
print(mylist)
mylist.sort()
print(mylist)

mylist.sort(reverse = True)
print(mylist)

original = [5, 2, 3, 1, 4]
newer = sorted(original)
print(original)
print(newer)

ori_tuple = ('a', 's', '3', '6')
new_list = sorted(ori_tuple)
print(ori_tuple)
print(new_list)