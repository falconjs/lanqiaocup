myletters = ['1', 'a', 's', '3', '1', '2']
if 'a' in myletters:
    print('I have found "a" in myletters.')
else:
    print('I didnot find "a" in myletters.')

if '2' in myletters:
    myletters.remove('2')
print(myletters)

# if '1' in myletters:
#     myletters.remove('1')
# print(myletters)

if 's' in myletters:
    print(myletters.index('s'))

# The index of 1 is 0
# The index of a is 1
# ...

idx = 0
for letter in myletters:
    print(letter)
    # print("The index of" ,letter ,'is' , myletters.index(letter))
    print("The index of" ,letter ,'is' , idx)
    idx = idx + 1