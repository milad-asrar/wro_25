python3

from wro_turtle_01 import *

# bewässere
t.clear() 
t.up()
pos ("start2")
t.down()

def gehe_zur_schw_linie():
    turn(-40)
    go(150)
    turn(35)
gehe_zur_schw_linie()    

# call bewäsere+zerstöre

# gehe zur west_bande
t.speed(3)

# schaut nach westen nach bewässern und zer
pos("b+z")
def gehe_zur_west_wand():
    turn(-200)
    turn(20)
    go(900)
    turn(180)
    go(-190)
    
gehe_zur_west_wand()    
pos_west_bande_bei_1_erdbeeren = t.position() # (304, 550)
t.up()
t.setposition(1186, -200)
t.setheading(180)
t.down()

t.speed(9)

def hole_4_erdbeeren():
    # steht an der west. Bande
    go(30)
    turn(-90)
    arme("beide","rauf")
    go(180)
    arme("beide","runter")
    go(-200)
    turn(90)
    go(180)
    turn(-90)
    # steht 18cm vor der zweiten Erdbeere
    arme("beide","rauf")
    go(180)
    arme("beide","runter")
    

hole_4_erdbeeren()


pos_sued_bande_links_vom_2_mp= t.position() # (304, 550)
t.up()
t.setposition(957, 550)
t.setheading(270)
t.down()
def liefere_erste_rote_erdbeeren_ab():
    go(-860)
    # steht an der südl Wand
    go(250)
    turn(90)
    go(800)
    turn(90)
    go(150)
    arme("rechts","rauf")
    go(-140)
    turn(90)
    go(200)
    turn(90)
    go(-320)

t.position() # (304, 550)
t.up()
t.setposition(86,441); t.setheading(90)



# steht an d. südl Wand vor den 2. Erdbeeren
pos_suedlich_wand_erdbeere_2 = t.position() # (304, 550)
t.up()
t.setposition(304, 550)
t.down()
go(100)
turn(-90)
# call funktion erkenne Erdbeeren

pos("gehekompost")
go(750)
turn(-90)
go(-230)
pos_suedlich_wand_vor_kompost = t.position() # (304, 550)
t.setposition(-816, 544)
go(650)
turn(90)
turn(-45)
go(250)
arme("beide","rauf")
go(-300)