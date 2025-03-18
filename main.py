import math
from turtle import Turtle, Screen


global Objects
Objects = []


class Object:
    def __init__(self, x, y):
        self.mass = float(input("Enter the mass of your object: "))
        self.x = int(x)
        self.y = int(y)
        self.radius = float(input("Enter the radius of your object: "))
        self.turtle = Turtle(shape="circle")
        self.turtle.speed(0)
        self.turtle.shapesize(self.radius, self.radius)

    def create(self):
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)

    def move(self, x, y):
        self.turtle.goto(x, y)


def calculateVectorPosition(x, y, velocity, vxp, vyp):
    """
    This function serves no purpose in the planetary body simulation.
    This project was originally for simulating objects being thrown and stopping on the ground due to the force of friction,
    but I became more interested in astrophysics and decided to change to planetary bodies to see how long it would take gravity to bring two objects together.
    """
    print("Base values:")
    print("x:", x, "m")
    print("y:", y, "m")
    frictionAccel = fGrass*g
    velocityX = 1
    if vxp == 0 or vyp == 0:
        theta = 0
    else:
        theta = math.atan(vyp / vxp)
        if theta < 0:
            theta += math.pi
    printTheta = theta * (180 / math.pi)
    print("velocity:", velocity, "m/s at {:.2f} degrees from ground.".format(printTheta))
    velocityX = velocityX * (velocity * (math.cos(theta)))
    velocityY = velocity * (math.sin(theta))
    if velocityX < 0:
        frictionAccel *= -1
    time = 0
    while True:
        t.goto(x*10, y*10)
        t.pendown()
        x = x + (velocityX / 1000)
        if velocityY > 0:
            y = y + (velocityY / 1000)
        else:
            if y >= abs(velocityY / 1000):
                y = y + (velocityY / 1000)
            elif abs(velocityY / 1000) >= y > 0:
                y = 0
                print("At time t=", (time / 1000), " seconds, the ball has hit the ground!", sep="")
        velocityY -= (g / 1000)
        if y == 0:
            if abs(velocityX) > abs(frictionAccel / 1000):
                velocityX -= (frictionAccel / 1000)
            elif abs(frictionAccel / 1000) >= abs(velocityX) > 0:
                print("At time t=", (time / 1000), " seconds, the ball has stopped!", sep="")
                break
        time += 1


def createObject(x, y):
    t.penup()
    t.setx(x)
    t.sety(y)
    print("(", t.xcor(), ", ", t.ycor(), ")", sep="")
    newObject = Object(t.xcor(), t.ycor())
    newObject.create()
    Objects.append(newObject)
    if len(Objects) == 2:
        simObjectMotion(newObject, Objects[0], 0, 0)


def calculateDistanceBetweenObjects(object1, object2):
    if object1.x > object2.x:
        xDist = object1.x - object2.x
        absXDist = abs(object1.x - object2.x)
    else:
        xDist = object2.x - object1.x
        absXDist = abs(object2.x - object1.x)
    if object1.y > object2.y:
        yDist = object1.y - object2.y
        absYDist = abs(object1.y - object2.y)
    else:
        yDist = object2.y - object1.y
        absYDist = abs(object2.y - object1.y)
    dist = math.sqrt(math.pow(absXDist, 2) + math.pow(absYDist, 2))
    return [dist, xDist, yDist]


def calculateGravitationalAcc(object1, object2):
    forceOfG = ((G * object1.mass * object2.mass) / calculateDistanceBetweenObjects(object1, object2)[0])
    accOne = forceOfG / object1.mass
    accTwo = forceOfG / object2.mass
    return [accOne, accTwo]


def defineHitbox(obj):
    half_side = obj.radius * 10
    left = obj.x - half_side
    right = obj.x + half_side
    top = obj.y + half_side
    bottom = obj.y - half_side
    return (left, right, top, bottom)


def checkTouching(obj1, obj2):
    left1, right1, top1, bottom1 = defineHitbox(obj1)
    left2, right2, top2, bottom2 = defineHitbox(obj2)

    if right1 < left2 or right2 < left1:
        return False
    if top1 < bottom2 or top2 < bottom1:
        return False
    return True


def simObjectMotion(thisObject, otherObject, velocityX, velocityY):
    """
    Best values for objects are as follows:
    mass1 - 3000000000
    mass2 - 200000
    you can choose whichever radius you want it does not affect the gravity calculations, only the hit boxes/visuals :)
    """
    time = 0
    while True:
        if checkTouching(thisObject, otherObject):
            thisObject.turtle.color("red")
            print("The objects have made contact!")
            break
        Xdistance = -(thisObject.x - otherObject.x)
        Ydistance = -(thisObject.y - otherObject.y)
        TOTdistance = math.sqrt(math.pow(Xdistance, 2) + math.pow(Ydistance, 2))

        theta = math.atan(Ydistance / Xdistance)
        if Xdistance < 0:
            theta += math.pi

        forceOfG = ((G * thisObject.mass * otherObject.mass) / TOTdistance)
        accOfG = forceOfG / thisObject.mass
        XaccOfG = accOfG * math.cos(theta)
        thisObject.x += (velocityX / 10)
        velocityX += (XaccOfG / 10)
        YaccOfG = accOfG * math.sin(theta)
        thisObject.turtle.goto(thisObject.x, thisObject.y)
        thisObject.y += (velocityY / 10)
        velocityY += (YaccOfG / 10)


if __name__ == '__main__':
    screen = Screen()
    t = Turtle(shape="circle", visible=False)
    t.speed(0)
    t.shapesize(0.5, 0.5)
    t.pensize(3)
    g = 9.81
    G = (6.67 * (math.pow(10, -11)))
    fGrass = 0.35
    t.goto(0, 0)
    screen.onclick(createObject)
    screen.mainloop()
