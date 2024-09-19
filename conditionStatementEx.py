# 조건문

# if~
# if ~ else ~
# if ~ elif(else if) ~ else ~

num = int(input("숫자 입력 >>"))

print("num : %d" % num)

if num == 0 :
    print("0")
elif num % 2 == 1 :
    print("홀수")
else :
    print("짝수")

# if문은 list와 함께 사용될 수 있다.
favheros = ["spiderman", "thor", "hulk"]

if "ironman" in favheros : 
    print("Ironman is not your favorite hero.") 