# 아래의 기능을 가진 프로그램을 함수를 이용하여 만들어 보자
# 마우스 왼쪽 버튼을 누르면 거북이가 클릭한 지점까지 임의의 색상으로 선을 그리면서 이동하도록 한다.
# 마우스 오른쪽 버튼을 누르면 거북이가 클릭한 지점까지 선을 그리지 않고 이동만 하도록 한다.
# 마우스 가운데 버튼을 누르면 거북이가 임의의 크기만큼 확대 또는 축소 되도록 한다.
import turtle
import random

#파이썬은 내가 쓸 함수를 위에서 만들어야 한다 인터프리터 방식이라서 위에서부터 한줄 한줄 실행되니깐
def screenLeftClick(x, y):
    #print(x, ", " , y)
    global r, g, b # r g b 를 전역적으로 사용하겠다고 선언
    turtle.pencolor(r, g, b) # pencolor() 함수로 pen color 를 설정
    turtle.pendown() # 팬업을 써서 오른쪽 버튼에 쓰기 위에서 여기서 안해도 그려지지만 썻다.
    turtle.goto(x, y)

def screenRightClick(x, y):
    #print(x, ", " , y)
    turtle.penup() # 팬업을 써서 오른쪽 버튼에 쓰기 위에서 여기서 안해도 그려지지만 썻다.
    turtle.goto(x, y)

def screenMiddleClick(x, y):
    #print(x, ", " , y)
    turtleSize = random.randrange(1, 10)
    turtle.shapesize(turtleSize)
    global r, g, b # r g b 를 전역적으로 사용하겠다고 선언
    r = random.random()
    g = random.random()
    b = random.random()




penSize = 10 # 기본 pen size
r, g, b = 0.0, 0.0, 0.0 # 기본 pen color

turtle.title("거북이 그림 그리기")
turtle.shape("turtle")
turtle.pensize(penSize)

turtle.onscreenclick(screenLeftClick, 1) # 스크린 영역에서 왼쪽 마우스 버튼을 클릭하면, onscreenclick클릭된 곳의 좌표를 보내줌
turtle.onscreenclick(screenRightClick, 3) # 스크린 영역에서 오른쪽 마우스 버튼을 클릭하면, onscreenclick클릭된 곳의 좌표를 보내줌 참고로 휠버튼이 2번이다.
turtle.onscreenclick(screenMiddleClick, 2) # 마우스 가운데 휠버튼 클릭하면

turtle.done()