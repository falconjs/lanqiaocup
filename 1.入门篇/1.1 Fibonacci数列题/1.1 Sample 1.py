"""
问题描述

Fibonacci数列的递推公式为：Fn=Fn-1+Fn-2，其中F1=F2=1。
当n比较大时，Fn也非常大，现在我们想知道，Fn除以10007的余数是多少。

输入描述
n
输入格式输入包含一个整数n。

输出描述

输出格式输出一行，包含一个整数，表示Fn除以10007的余数。
"""

print("Please input n : ")
n = int(input())

print("n =", n)

f1 = 1
f2 = 1

# f3 = f1 + f2
# f4 = f2 + f3

i = 1
while i <= n:
    f3 = f1 + f2
    f1 = f2
    f2 = f3
    i += 1
    print(f3)

result = f3 % 100007

print("Result = {0}".format(result))




