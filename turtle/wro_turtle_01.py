#%%

"""
17 cm = 185
1 cm = 185/17 = 10.8823
28 cm = 185
1 cm = 207/28 = 7,3929
turn 170 verzögerung
14 in cm
"""
#!/bin/python3

import turtle 

s = turtle.Screen()
t = turtle
s.bgpic('matte_measures_new.gif')
s.setup(1219, 587)
s.tracer(1)

t.shapesize(stretch_wid=10, stretch_len=7)
t.shape("turtle") 




t.setpos(0, 0) 
t.clear()
s.setup(1700, 780)
#%%
def set_pos(wohin):
    pos:dict={"start":[-750,-275,0],
    "mitte":[0,0,0]}
    #
    x=pos[wohin][0]
    y=pos[wohin][1]
    heading=pos[wohin][2]
    t.setpos(x,y)
    t.setheading(heading)


def turn(winkel,*arg):
    t.write(f"turn {winkel}")
    if winkel > 0:
        t.right(abs(winkel))
    else:
        t.left(abs(winkel))
#        
def go(strecke, *arg):
    cm=7.875
    t.write(f"go {strecke}")
    if strecke > 0:
        t.forward(abs(strecke)*cm)
    else:
        t.backward(abs(strecke)*cm)
#
def arme(*arg):
    if arg[1] == "runter":
        color = "Green"
    else:
        color = "Blue" 
    if arg[0]=='beide':
        t.dot(50, color)
    elif arg[0]=='links':
        t.dot(25, color)
    elif arg[0]=='rechts':
        t.dot(25, color)


saved_pos:dict={}


def balken():
    go(200)
    turn(-90)
    go(200)
    turn(-90)
    go(50)
    saved_pos["balken"]=t.pos()

def balken_2():
    go(-50)
    turn(180)
    go(100)
    saved_pos["balken_2"]=t.pos()

def balken_3():
    go(-100)
    turn(-90)
    go(300)
    turn(-90)
    go(50)

def balken_4():
    go(-50)
    turn(180)
    go(400)
    turn(-90)
    go(50)

def balken_5():
    go(-50)
    turn(90)
    go(600)

def balken_6():
    go(-100)
    turn(90)
    go(500)
    
    
"""

set_pos("start")
balken()
balken_2()
balken_3()
balken_4()
balken_5()
balken_6()
set_pos("start")
print(saved_pos)

"""

def mission():
    t.clear()
    set_pos("start") 


# exec(open("/wro_turtle_01").read(), globals())
 
def mission_2():
    set_pos("start") 
    x,y=[-730,-250]
    t.setpos(x,y)

    turn(-90)
    go(38.5)
    turn(90)
    go(25)
    t.position()
    turn(-90)
 

def i():
    t.color('skyblue')
    t.shapesize(stretch_wid=2, stretch_len=2)
    t.shape("arrow") 
    
#
    x,y=[-660,-290]; t.setpos(x,y)
    t.setheading(0)
    t.clear()
i()

#set_pos("start")
 
#start


# Matte: 235.5 X 114
# from PIL import Image

# im = Image.open("matte_measures.gif")#.convert("RGB")

# width, height = im.size
# dpi = im.info.get("dpi", (72, 72))
# width_cm = width / dpi[0] * 2.54
# height_cm = height / dpi[1] * 2.54
 
"""
1 cm = 7.3929

"""
 
def start_zweiter_turm():
    t.clear();x,y=[-690,-310]; t.setpos(x,y);t.setheading(0)
    go(19)
    turn(-90)
    go(75)
    turn(-90)
    go(14)

"""
t.clear();x,y=[-690,-310]; t.setpos(x,y);t.setheading(0)
go(19)
turn(-90)
go(33)
turn(90)
go(20.5)
"""


"""
python3 -i wro_turtle_01.py
"""





















# go(30)
# turn(-90)
# go(30)
# turn(90)
# go(27)
# turn(180)
# go(44)
# go(-18)
# turn(90)
# go(43)
# turn(-90)
# go(6)
# turn(180)
# go(30)
# go(35)
# turn(-90)
# turn(180)
# go(75)
# turn(-90)
# go(60)
# go(20)
# go(-40)
# turn(-90)
# go(72)
# turn(90)
# go(40)
# go(-40)
# turn(90)
# go(35)
# turn(90)
# go(20)
# turn(180)
# go(20)
# go(63)
