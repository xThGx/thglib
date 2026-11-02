from turtle import *

bgcolor("black")

i = 0
while i < 4:
    color("lime")
    forward(50)
    right(90)
    i += 1

left(180)
forward(50)
right(180)
circle(50)
forward(150)
circle(50)

color("lime")
forward(150)
circle(50)

color("red")
forward(150)
circle(50)

color("purple")
forward(150)
circle(50)

begin_fill()

color("white")
backward(800)
left(60)
forward(30)
right(120)
forward(30)
right(120)
forward(30)

end_fill()


done()
