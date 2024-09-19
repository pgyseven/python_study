import turtle
import random

myTurtle, tx, ty, tColor, tSize, tShape = [None] * 6
shapeList = []   # shapeList라는 이름에 빈 배열 리스트를 생성
playerTurtle = []
sWidth, sHeight = 500, 500

turtle.title('꼬북이 리스트 활용')
turtle.setup(sWidth, sHeight)
shapeList = turtle.getshapes()
#print(shapeList)
for i in range(0, 100)  : #0~99 반복
    random.shuffle(shapeList)   # 썪어줌
    #print(shapeList[0])
    myTurtle = turtle.Turtle(shapeList[0])
    tx = random.randint(-250, 250)
    ty = random.randint(-250, 250)
    #print(tx, ty)  # 꼬북이의 x, y 좌표
    r= random.random()
    g= random.random()
    b= random.random()
    tSize = random.randrange(1, 3)
    playerTurtle.append([myTurtle, tx, ty, tSize, r, g, b])

for t in playerTurtle :
    myTurtle = t[0]
    myTurtle.color(t[4], t[5], t[6])
    myTurtle.pencolor(t[4], t[5], t[6])
    myTurtle.turtlesize(t[3])
    myTurtle.goto(t[1], t[2])

    
turtle.done()