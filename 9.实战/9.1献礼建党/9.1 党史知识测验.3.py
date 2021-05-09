import time
import os

examination = [
    [
        "1.中国共产党第一次全国代表大会是_____年___月____日，在______举行。",
        "A.1921 7 23 ；浙江  B.1923 6 12 ；广州",
        "A"
    ],
    [
        "2.南昌起义在1927年__月__日举行。",
        "A. 8 ；1 B. 9 ；9",
        "A"
    ]
]

if os.name == 'nt':  # for windows
    os.system('cls')
else:  # for mac and linux(here, os.name is 'posix')
    os.system('clear')

print("欢迎参加此竞赛")
time.sleep(2)
score = 0
score_pre = 50

for num, exam in enumerate(examination):
    question, choice, correctAnswer = exam[0], exam[1], exam[2]
    print()
    print(question)
    print(choice)
    answer = input("你的回答是：")
    if answer == correctAnswer:
        print(f'\033[92m恭喜，回答正确！\033[0m')
        score = score + score_pre
    else:
        print(f'\033[91m遗憾，回答错误！\033[0m')
    time.sleep(1)

print()
print("测试结束，正在计算得分，请稍等……")
time.sleep(2)
print("此次测验您的总分是：" + str(score))
