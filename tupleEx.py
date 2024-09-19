# 튜플 : 리스트와 비슷하지만 변경할 수 없는(immutable) 자료형(read-only)

# tuple 생성

tuple1 = (1, 2, 3)
tuple2 = (10, 20, 30)

print(tuple1)

# tuple 에서 값 얻어오기
print(tuple2[2]) # 3

# tuple2[0] = 100 # 이건 불가능 하다 변경 불허

# list, tuple indexing
list = ['a', 'b', 'c', 'd', 'e', 'f']

# list[시작값:종료값(포함안됨)]
print(list[2:5]) # c d e / 2 <= index < 5
print(list[1:]) # 종료값이 생략 -> 1 <= index 부터 끝까지
print(list[:-1]) # 시작값이 생략되면 0 <= index < len(list)

tuple3 = ('apple', 'banana', 'cherry', 'blueberry', 'watermelon')
print(tuple3[2:]) # 2 번째 요소부터 끝까지
