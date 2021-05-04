print("欢迎参加此竞赛")

question = "中国共产党第一次全国代表大会是_____年___月____日，在______举行。"
choice = "A.1921 7 23 ；浙江  B.1923 6 12 ；广州"

print(question)
print(choice)

answer = input("你的回答是：")
correctAnswer = "A"
score = 0

if answer == correctAnswer:
    print("回答正确！")
    score = score + 1
    print("+1")

else:
    print("再试一试")
