# 2개의 정수를 받아서, 덧셈, 뺄셈, 곱셉 나눗셈의 결과를 화면에 출력하는 Python 프로그램

num1 = input("정수를 입력하세요 >>") #input() 함수로 입력받은 값은 str 타입이다.
num2 = input("정수를 입력하세요 >>")

print(num1, "+", num2 , "=", int(num1) + int(num2))
print(num1, "-", num2 , "=", int(num1) - int(num2))
print(num1, "*", num2 , "=", int(num1) * int(num2))
print(num1, "/", num2 , "=", int(num1) / int(num2))