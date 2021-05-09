import time
import os

examination = [
    [
        "1.中国共产党第一次全国代表大会是_____年___月____日，在______举行。",
        "A、1921 7 23 ，浙江     B、1923 6 12 ，广州     C、1924 7 15 ，徐州    D、1921 7 12 ，广西",
        "A"
    ],
    [
        "2.南昌起义在1927年__月__日举行。",
        "A、 8, 1     B、 9, 9     C、 10, 10     D、 7, 1",
        "A"
    ],
    [
        "3.随着马克思主义同中国工人运动的结合日益紧密、建立统一的中国共产党的条件日益成熟。在共产国际代表的促进下，中共一大于______在上海召开。",
        "A、1921年6月20日    B、1921年7月1日    C、1921年7月23日     D、1921年7月30日",
        "C"
    ],
    [
        "中国共产党第十九次全国代表大会，是在全面建成小康社会决胜阶段、中国特色社会主义进入_______的关键时期召开的一次十分重要的大会。",
        "A、新时期      B、新阶段     C、新征程      D、新时代",
        "D"
    ],
    [
        "十九大的主题是:不忘初心，_______，高举中国特色社会主义伟大旗帜，决胜全面建成小康社会，夺取新时代中国特色社会主义伟大胜利，为实现中华民族伟大复兴的中国梦不懈奋斗。",
        "A、继续前进       B、牢记使命      C、方得始终       D、砥砺前行",
        "B"
    ],
    [
        "",
        "",
        ""
    ],
    [
        "",
        "",
        ""
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
