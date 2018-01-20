#SpaceWars by Elliott Choi

import turtle
import os
import random
import time


#change background colour
turtle.bgcolor("black")
turtle.title("Space Wars")
#animiation speed of the turtle 
turtle.speed(0)
#create a turtle window, we hide it 
turtle.hideturtle()
#saves up memory
turtle.setundobuffer(1)
turtle.tracer(0)

#Sprite can use all the turtle methods
class Sprite(turtle.Turtle):
    #define constructor of the class
    def __init__(self,spriteshape,color,startx,starty):
        turtle.Turtle.__init__(self,shape=spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        #go to where we define as start
        self.goto(startx,starty)
        #speed of sprite movement
        self.speed=1
    
    #default sprite movement class    
    def move(self):
        self.fd(self.speed) 
        if self.xcor()>290:
            self.setx(290)
            self.rt(60)
        if self.xcor()<-290:
            self.setx(-290)
            self.rt(60)
        if self.ycor()>290:
            self.sety(290)
            self.rt(60)
        if self.ycor()<-290:
            self.sety(-290)
            self.rt(60)
        
    def is_collision(self,other):
        if (self.xcor()>=(other.xcor()-20)) and\
        (self.xcor()<=(other.xcor()+20)) and\
        (self.ycor()>=(other.ycor()-20)):
            if (self.ycor()<=(other.ycor()+20)):
                return True
        else:
            return False

#Game Class
class Game():
    #initialize the constructor
    def __init__(self):
        self.level=1
        self.score=0
        self.state="playing"
        
        #draw the info
        self.pen=turtle.Turtle()
        self.lives=3
    
    #draw the border
    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300,300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.pendown()
    
    def show_status (self):
        self.pen.undo()
        msg = "Score: %s"%(self.score)
        self.pen.penup()
        self.pen.goto(-300,310)
        self.pen.write(msg,font=("Arial",16,"normal"))
        
#Create the game object
game = Game()
game.draw_border()
game.show_status()

#enemy Sprites
class Enemy (Sprite):
    def __init__(self,spriteshape,color,startx,starty):
        #call to parent class
        Sprite.__init__(self,spriteshape,color,startx,starty)
        self.speed=6
        self.setheading(random.randint(0,360))

#enemy Sprites
class Ally (Sprite):
    def __init__(self,spriteshape,color,startx,starty):
        #call to parent class
        Sprite.__init__(self,spriteshape,color,startx,starty)
        self.speed=10
        self.setheading(random.randint(0,360))
    
    #overide boundary for ally class
    #default sprite movement class    
    def move(self):
        self.fd(self.speed) 
        if self.xcor()>290:
            self.setx(290)
            self.lt(60)
        if self.xcor()<-290:
            self.setx(-290)
            self.lt(60)
        if self.ycor()>290:
            self.sety(290)
            self.lt(60)
        if self.ycor()<-290:
            self.sety(-290)
            self.lt(60)

class Missile (Sprite):
    def __init__(self,spriteshape,color,startx,starty):
        #call to parent class
        Sprite.__init__(self,spriteshape,color,startx,starty)
        self.shapesize(stretch_wid=0.3,stretch_len=0.4,outline=None)
        self.speed=20
        self.status="ready"
        #self.goto(-1000, -1000)
        
    def fire(self):
        if self.status=="ready":
            self.goto(player.xcor(),player.ycor())
            self.setheading(player.heading())
            self.status= "firing"
        #overiding existing method in parent class
    
    def move(self):
        
        if self.status=="ready":
            self.goto(1000,1000)
        if self.status=="firing":
            self.fd(self.speed)
        
        #border check
        if self.xcor()< -290 or self.xcor()>290 or \
        self.ycor()<-290 or self.ycor()>290:
            self.goto(-1000, 1000)
            self.status="ready"

#child of the Sprite Class
class Player(Sprite):
    #same attributes as parent
    def __init__(self,spriteshape,color,startx,starty):
        #initializes itself as a sprite
        Sprite.__init__(self,spriteshape,color,startx,starty)
        self.speed=4
        self.lives=3
        
    def turn_left(self):
        self.lt(45)
    
    def turn_right(self):
        self.rt(45) 
    
    def accelerate(self):
        self.speed+=1
    
    def decelerate(self):
        self.speed-=1
    
#create player sprite
player = Player("triangle","white",0,0)
missile= Missile("triangle","yellow",0,0)

enemies=[]
for i in range(6):
    x=random.randint(-200,200)
    y=random.randint(-150,100)
    enemies.append(Enemy("circle","red",x,y))

allies=[]
for i in range(6):
    x=random.randint(-200,200)
    y=random.randint(-150,100)
    allies.append(Ally("square","blue",x,y))

#turtle module for onkey
turtle.onkey(player.turn_left,"Left")
turtle.onkey(player.turn_right,"Right")
turtle.onkey(player.accelerate,"Up")
turtle.onkey(player.decelerate,"Down")
turtle.onkey(missile.fire,"space")
turtle.listen()

#main game loop
while True:
    turtle.update()
    time.sleep(0.01)
    
    player.move()
    missile.move()
    
    for enemy in enemies:
        enemy.move()
        
        if player.is_collision(enemy):
            x=random.randint(-250,250)
            y=random.randint(-250,250)
            enemy.goto(x, y)
            game.score-=100
            game.show_status()
            
        if missile.is_collision(enemy):
            x=random.randint(-250,250)
            y=random.randint(-250,250)
            enemy.goto(x, y)
            missile.status="ready"
            game.score+=100
            game.show_status()
    
    for ally in allies:
        ally.move()
        
        if missile.is_collision(ally):
            x=random.randint(-250,250)
            y=random.randint(-250,250)
            ally.goto(x, y)
            missile.status="ready"
            game.score-=50
            game.show_status()

    
    

delay = raw_input("Press enter to finish . >")