# print 함수의 다양한 출력 방법을 알아보자.


#  print 함수는 다양한 서식을 제공한다.
# %d : 10진 정수
# %f : 실수 
# %s : 문자열

print("10진 정수 : %d" % 10)

print("%d * %d = %d" % (3, 4, 12))

print("실수 : %f" % 3.14)
print("실수 : %5.2f" % 3.14) # 전체 5자리 소수점 이하는 2자리

print("문자열 : %s" % "Hello, World!", end='') # end='' 이게 없다 치면 /n 이 자동으로 들어간다. 생략된거 근데 end='' 빈문자열을 넣어라 라고 했으니 줄바꿈 안하고 아래의 문장이 옆에 나온다.
print(" We are the world! ")
