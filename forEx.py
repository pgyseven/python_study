# for 문

# for 변수 in range(시작값, 끝값, 증감값) :     -> 증감값을 생략하면 1이 된다.
# 반복 수행할 코드


#구구단의 단을 입력 받아 해당 단의 구구단을 출력하세요

# dan = int(input("구구단의 단을 입력하세요 : "))

# for i in range(1, 10):
#     print(f"{dan} x {i} = {dan * i}")



# 구구단 1~9 단까지 전체 출력 하는 프로그램을 이중 for문으로 작성하세요

# for dan in range(1, 10):
#     for i in range(1, 10):
#         print("%d * %d = %d" % (dan, i, dan * i), end=' ')
#     print() #줄바꿈


#구구단의 단을 입력 받아 해당 단의 구구단을 출력하세요 (while문으로)
dan = int(input("구구단의 단을 입력하세요 : "))
i = 1

while i < 10 :
    print("%d * %d = %d" % (dan, i, dan * i))
    i += 1

# 자매품 continue, break 도 자바와 똑같다.
 
