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
        "4.中国共产党第十九次全国代表大会，是在全面建成小康社会决胜阶段、中国特色社会主义进入_______的关键时期召开的一次十分重要的大会。",
        "A、新时期      B、新阶段     C、新征程      D、新时代",
        "D"
    ],
    [
        "5.十九大的主题是:不忘初心，_______，高举中国特色社会主义伟大旗帜，决胜全面建成小康社会，夺取新时代中国特色社会主义伟大胜利，为实现中华民族伟大复兴的中国梦不懈奋斗。",
        "A、继续前进       B、牢记使命      C、方得始终       D、砥砺前行",
        "B"
    ],
    [
        "6.中国共产党是中国⼯⼈阶级的先锋队，同时是中国⼈民和______的先锋队，是中国特⾊社会主义事业的领导核⼼。",
        "A、新社会阶层    B、中华民族    C、知识分⼦    D、农民阶级",
        "B"
    ],
    [
        "7.近代以来，中华民族⾯对着两⼤历史任务：⼀个是______；⼀个是实现国家繁荣富强和⼈民共同富裕。",
        "A、反对帝国主义    B、反对封建主义    C、求得民族独⽴和⼈民解放    D、实现民族复兴",
        "C"

    ],
    [
        "8.______是中国⾰命史上具有重⼤意义的事件，标志着中国新民主主义⾰命的开端。",
        "A、⾟亥⾰命    B、护国运动    C、五四运动    D、⼆次⾰命",
        "C"
    ],
    [
        "9.1921年7⽉23⽇，党的⼀⼤在上海开幕。后因代表们的活动受到监视，⼤会转移到浙江______继续召开。",
        "A、杭州西湖    B、嘉兴南湖    C、绍兴东湖    D、宁波东钱湖",
        "B"
    ],
    [
        "10.1922年7⽉，党的⼆⼤第⼀次提出了明确的______的民主⾰命纲领。",
        "A、⼟地⾰命    B、反帝反封建    C、社会主义⾰命    D、民族⾰命",
        "B"
    ]
]


if os.name == 'nt':  # for windows
    os.system('cls')
else:  # for mac and linux(here, os.name is 'posix')
    os.system('clear')

print("====================================================")
print("|         欢迎参加纪念建党100周年知识竞赛         |")
print("====================================================")
time.sleep(2)
score = 0
score_pre = 10

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
print("测试结束，正在计算得分，请稍等......")
time.sleep(2)
print("此次测验您的总分是：" + str(score))
