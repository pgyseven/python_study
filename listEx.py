#자바 스크립트의 배열과 같은 방식으로 동작하는 list 에 대해 알아보자
# 크기가 동적인 배열, 모든 자료형을 다 list에 관리 할 수 있다.

list = [1, 2, 3.14, False, 'hello', [4,5,6]];
print(list);

# list에 요소를 추가
list.append('world');
print(list);

# list에서 index 2번째 요소 값을 가져와 출력
print(list[2]); #3.14
print(list[5][1]) #5

list[5][2] = 60
print(list)

# list에서 4번째 요소를 삭제
del(list[4])
print(list)

# list에서 마지막 요소를 꺼내기
print(list.pop()) #마지막 요소를 꺼낸 후 list 삭제
print(list)

list2 = [10, 5, 1, 4, 7, 12]
list2.sort() # list를 오름차순으로 정렬
print(list2)

list2.reverse() #역순으로
print(list2)    

list.insert(3, 'inserted') # 3번째 index에 'inserted'를 추가
print(list)

print(len(list)) # list의 길이 반환

#len을 이요하여 list2의 모든 값을 더해서 sum에 저장
sum = 0
for i in list2 : #rang 시작값이 생략되어 있으니 0부터 시작이다.
    sum += i
print(sum)

list2.append(10)
print(list2)

print(list2.count(10)) # list2안에 10이 몇번 나오는지 count

print(list2.index(10), 2) # list2에서 10이 2번째 index 이후에 나오는 index

