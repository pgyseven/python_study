import turtle # {} 외부 라이브러리 패키지를 의미 gui 가 내장되어 있다.

turtle.shape("turtle") # turtle shape는 함수다. 커서의 모양을 turtle로 설정

# turtle.forward(200) 
# turtle.right(90) # 90도 right
# turtle.forward(200)
# turtle.right(90)
# turtle.forward(200)
# turtle.right(90)
# turtle.forward(200)

# for i in range(4):#자바에서 중간 브레스 역할을 들여쓰기로 한다 중요!
#     turtle.forward(200)
#     turtle.right(90)

  # "박근영" 글자 그리기
turtle.write("박", font=("Arial", 48, "normal"))
turtle.forward(50)  # 다음 글자를 위해 이동
turtle.write("근", font=("Arial", 48, "normal"))
turtle.forward(50)
turtle.write("영", font=("Arial", 48, "normal"))



turtle.done() # 프로그램이 종료되지 않고 대기하도록
