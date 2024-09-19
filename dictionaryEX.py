# Dictionary : key-value pair로 이루어진(unordered 순서가 없는) collection. 자바에서 map 인터페이스와 유사
# key값은 중복을 허용하지 않으며,  value 값은 중복을 허용한다.

#list : []
#tuple : ()
#dictionary : {}

dict1 = {'apple': '사과', 'banana': '바나나', 'cherry': '체리', 'Orange': '오렌지'}

print(dict1)

# key로 value를 얻어오기
print(dict1['apple'])

# key 를 중복해서 넣는다면? (같은 key 를 넣으면 해당 key에 대한 value가 overWrite)
dict1['apple'] = '애플회사'
print(dict1)

# value값은 중복 가능
dict1['버내나'] = '바나나'
print(dict1)

# dictionary 에서 모든 key를 가져오기
keys = dict1.keys()
keys2 = list(dict1.keys()) # dict1.values() : dict2의 value 들을 list로 반환
print(keys)
print(keys2)

# dict1의 키와 value 를 tuple 형태로 반환 시키기
print(list(dict1.items()))

# 해당 dictionary 에 key가 존재한다면 그 값을 얻어오기
if 'apple' in dict1:
    print(dict1['apple'])
else:
    print('없다')