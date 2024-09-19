# 파이썬의 주석(샵)
# 파이썬에서의 변수 선언
num1 = 3
num2 = 5
print(num1 + num2) # 8

print(type(num1))  # int

pi = 3.141592653589793 # float 이처럼 들어온 수에 따라서 타입이 결정된다.
print(type(pi))
# 반지름이 5cm 인 원의 원넓이
radus = 5
circleArea = pi * radus ** 2

print("원 넓이 :", circleArea)

#boolean
근영이가핸섬하나 = True
오늘은토요일이나 = False
print(type(근영이가핸섬하나)) # bool

# str (문자열)\
name = "근영"
print(type(name)) # str

# None (null)
myStr = None
if (myStr == None) :
    print("myStr is None")
else :
    print("myStr is not None")

# 기초 자료형은 위와 같다. 
# 위의 기초 자료형 이외에도 list(ArrayList), tuple(읽기 전용 ArrayList), set, dict(Map) 등이 있다.

