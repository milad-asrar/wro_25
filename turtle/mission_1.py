# python3
from wro_turtle_01 import *

t.up()
# schaue nach norden am Start
heading = -90
t.setpos(1070, -50) 
t.setheading(heading)

# schaue nach westen am Start
heading = -180
t.setpos(1100, -90);  # startposition 
t.setheading(heading)
  
t.down()

t.clear()
def hole_erste_erdbeeren():
turn(-20)
go(200) 
turn(17)
go(120)
arme("beide", "runter")
go(-200)  
# zur 2. Erdbeere
turn(95)
go(180)
turn(-95)
arme("beide", "rauf")
go(180)
arme("beide", "runter")
go(-165)
turn(90)
go(120)

hole_erste_erdbeeren()

t.setheading(180)
# position am ende  der  schw. linie
t.setpos(-780, -190)
t.position()
t.clear()

def gehe_zum_kompost_und_marktplatz():
# gehe zum kompost und liefere, gelbe Erdbeere ab
    turn(-45)
    go(250)
    arme("links", "rauf")
    # gehe quer zurück
    go(-300)
    turn(-45) 
    go(-200)
    turn(-90)
    go(100)
    arme("beide","runter")
    go(-100)
    turn(90)  
    go(-250) 
    turn(-90)
    go(500)
    turn(-90)
    arme("rechts", "rauf")
    go(150) 
    go(-130)
    turn(90)
    go(600)
    turn(90)
    go(-300)  
    
# der Roboter befindet sich an der nördl. Bande
gehe_zum_kompost_und_marktplatz()
pos = t.position()


t.setpos(455, 570)
t.setheading(270)
go(100)
turn(-90)
# stehe an der ost bande

# position am ende  der  schw. linie
t.setpos(-780, -190); t.setheading(180)
t.position()
go(900)
turn(-90)



go(80)
turn(-90)
#%%
t.clear()
t.shapesize(stretch_wid=1, stretch_len=1)
t.pensize(10)
t.pencolor("Blue")
t.circle(20, 180)
t.undo()
#%%
# Schwarze Lienie zum linkesten baum
t.clear()
pos=t.position()
t.setheading(180)
turn(90)
go(450)
turn(-90)
go(250)
 
#%%
c=t.clear

#%%

pos("start1")
pos("start2")
pos("wall1")
pos("wall2")
pos("wall3")
pos("linie1")
pos("linie2")
pos("linie3")
#gehe gewächshaus1
pos("wall3")
go(200)
go(100)#folge linie
turn(-90)
go(210)
turn(-90)
#gehe bis zur farbenkombi
#gehe gewächshaus2
pos("wall3")
go(200)
go(650)#folge linie
turn(-90)
#Orangener Marktplatz
pos("wall3")
go(300)
turn(90)
go(-700)
go(120)
turn(90)
go(50)


#%%
''
try:
    turtle.bye()
except:
    pass 
 
#%%