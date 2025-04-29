# python3
from wro_turtle_01 import *

def get_status(*siu):
    pass
def hole_erste_erdbeeren():
    t.shape("turtle")
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
    go(-135)
    turn(93)
    go(100)
t.speed(1)
pos("start1")
hole_erste_erdbeeren()
#:
# Pos2
#: Roboter steht am Ende der langen schwarzen Linie
def gehe_zum_kompost_und_marktplatz():
    # gehe zum kompost und liefere, gelbe Erdbeere ab
    t.hideturtle()
    go(1650)
    t.showturtle()
    turn(-45)
    go(200)
    arme("links", "rauf")
    # gehe quer zurück
    go(-250)
    turn(-45)
    go(-450)
    turn(-90)
    go(450)
    turn(-90)
    arme("rechts", "rauf")
    go(120)
    go(-80)
    turn(90)
    go(660)
    turn(45)
    go(-50)
    turn(45)
    go(-400)
gehe_zum_kompost_und_marktplatz()
pos("wall1")
    # der Roboter befindet sich an der nördl. Bande
# erkenne erste erdbeere
# kleiner marktplatz mit den zwei erdbeeren
def erkenne_erdbeere_am_marktplatz(debug=False):
    """
    robot muss an der südl. Bande stehen
    """
    # der Roboter befindet sich an der nördl. Bande
    #robot.settings(straight_speed=200, turn_acceleration=200)
    if debug:
        print("erkenne_erdbeere_am_marktplatz")
    go(100)
    turn(-90)
    go(50)
    # robot sieht direkt auf die erste Erdbeere
    #erkannte_farbe = gehe_bis_zur_farben_front(farben="gelb_rot", max_distanz=300)
    """
    turn(-20)
    go(-300)
    turn(20)
    go(-250)
    turn(-90)
    """
    # liefere rote Erdbeere (2. Marktplatz) ab
    #go(70)
    #go(-110)
    #turn(-90)
# nachdem auf dem zweiten Marktplatz beide Erdbeeeren gesammelt wurden
def gehe_zum_kompost_haufen(debug=False):
    # gehe zum kompost haufen
    # die zwei erdbeeren wurden aufgesammelt
    # die rote bereits abgelegt
    #: gehe entlang des Marktplatzes
    go(600)
    turn(-90)
    # wall an der sued. Bande aus
    go(-300)
    # gehe auf den Komposthaufen zu
    go(800)
    turn(90)
    go(100)
    turn(-90)
    turn(45)
    go(250)
    arme("rechts","rauf")
    go(-350)
    turn(-135)
        # robot befindet sich auf der w. Linie
pos("gehekompost")
gehe_zum_kompost_haufen()

#: -----------------------------------------------------------------------------
# Bewässern und Erde
#: -----------------------------------------------------------------------------
def get_block_farbe(debug=False):
    """
    erkennt schwarzen / grünen Block
    schwarze blöck werden weggestossen
    """
    start_position = robot.distance()
    robot.settings(straight_speed=100, turn_acceleration=300)
    gefahrene_distanz = fahre_bis_zur_farbkombi_am_boden(
        [Color.WHITE, Color.BLACK], max_gefahrene_distanz=70, debug=True
    )
    heading_korrektur(heading_soll=0)
    gesehene_farben = []
    gefundene_farbe = gehe_bis_zur_farben_front("schwarz_gruen", max_distanz=20)
    if debug:
        print(f"get_block_farbe: gefundene_farbe: {gefundene_farbe}")
    return gefundene_farbe


#: -----------------------------------------------------------------------------
def get_battary_status(debug=False):
    voltage = hub.battery.voltage()
    battery = 0
    VMAX = 8300
    VMIN = 6000
    if voltage >= VMAX:
        print("battery is at 100%")
    elif voltage <= VMIN:
        print("battery is at 1% or less")
    else:
        battery = (voltage - VMIN) * 100 / (VMAX - VMIN)
        print(f"battery is at {round(battery)}%, volts={voltage}")
    return round(battery)




#: #############################################################################
#                                     MAIN
#: #############################################################################


def hole_wasserblock(debug=False):
    """ 
        Robot steht an der östl Bande  
    """ 
    turn(35)
    go(200)
    arme("beide","runter")
    go(-250)
    turn(-35)
    go(-250)
   

def bewaessere_und_zerstoere(debug=False):
    """
        robot befindet sich an der westl. Bande
        folgt der linie für 17 cm und dreht sich nach links, 
        erkennt die Erdbeere und bewässert oder zerstört
    """

    go(150, "gehe von der westl. Bande vor zur schwarzen Linie",debug=debug)
    folge_linie(stoppe_bei_farbmuster=[], max_gefahrene_distanz=330, end_ausrichtung=90, debug=False) 
    get_status("hole_wasserblock ende")
    zerstoer_modus = False 
    block_farbe=""

    for i in range(3):
        robot.settings(straight_speed=200, turn_acceleration=300)
        folge_linie(stoppe_bei_farbmuster=[], max_gefahrene_distanz=140, max_speed=200,  end_ausrichtung=90, debug=False) 
        turn(-90)  

        if zerstoer_modus is True:
            if debug:
                print(f"bewaessere_und_zerstoere: zerstoer_modus {zerstoer_modus}")
            block_farbe =''
            #arme("beide","runter")
            go(150, "zerstöre die Erdbeere / Erdblock",debug=debug)
            go(-150)
            heading_korrektur(heading_soll=0)
            turn(90)
        else:
            #geht von der Linie bis zum Block um die Farbe zu erkennen
            arme("beide","rauf")
            block_farbe = get_block_farbe(debug=True) #geht bis zur schwarzen linie und gibt die Blockfarbe
            
       
        if debug:
            print(f"bewaessere_und_zerstoere: block_farbe {block_farbe}")

        if block_farbe =='BLACK' or block_farbe=='NONE': 
                arme("beide","runter")
                go(-30)
                go(90, "schiebe den schw. Block weg")  
                go(-120, "gehe zurueck auf die wieße Linie") 
                ## ma: heading_korrektur(heading_soll=0) 
                turn(90) 
        elif block_farbe == "GREEN":
            if debug:
                print("bewaessere_und_zerstoere: Gruenen Block erkannt")
            go(-20)
            turn(-30)
            go(-150)
            arme("beide","runter")
            #go(-150, "gehe zurueck, um den Wasserblock nach vorne zu schieben",debug=debug)
            # wasserblock liegt vor dem Robot arme runter und vor um ihn zum g. Block zu schieben   
            #arme("beide","runter") 
            #turn(20)
            go(140, "gehe wieder vor um den WB nach vorne zu schieben",debug=debug)  
            go(-40,"zurueck auf die weiße Linie",debug=debug) 
            turn(120) # drehe richtung Komposthaufen
            zerstoer_modus = True
    get_status("bewaessere_und_zerstoere ende")



#: #############################################################################
def main(starte_ab=10, debug=False):
    """

    """
#: #############################################################################
    # zeige die Prozent der Battie auf dem Display
    if starte_ab <=10:
        battery_prozent = get_battary_status()
        hub.display.number(battery_prozent)
    
    if starte_ab <=20:
        reset(angle=0)
        get_status("start - hole_erste_erdbeeren")
        hole_erste_erdbeeren()
        get_status("vor der schwarzen Linie")

    if starte_ab <=30:
        robot.settings(straight_speed=200)
        gefahrene_distanz = folge_linie(
            ["BLACK", "GREEN"], max_gefahrene_distanz=1550
        )  # 1630 ist die gesamt schwarze linie
        heading_korrektur(90, comment="nach der langen Linie")
    get_status("gehe_zum_kompost_und_marktplatz")

    if starte_ab <=40:
        gehe_zum_kompost_und_marktplatz()

    # robot befindet sich an d. südl. Bande
    #: -----------------------------------------------------------------------------
    # zweiter Marktplatz
    #: -----------------------------------------------------------------------------
    # richte_robot_auf_die_erdbeeren
    # jetzt muß der Roboter genau auf die Erdbeere am Marktplatz schauen, max. 30 cm entfernt
    if starte_ab <=50:
        get_status("erkenne_erdbeere_am_marktplatz")
        erkenne_erdbeere_am_marktplatz()
    if starte_ab <=60:
        get_status("gehe_zum_kompost_haufen")
        gehe_zum_kompost_haufen()
    
    if starte_ab <=70:
        #robot hat das 2. beim Kompost abgeliefert und steht auf der w. Linie
        #reset(-90)
        folge_linie(
        stoppe_bei_farbmuster=[],
        max_gefahrene_distanz=1700,
        end_ausrichtung=-90,
        debug=False,
        )
        turn(180)
        go(-100)
        print(zeiten) 

    if starte_ab <=80:
        hole_wasserblock()

    if starte_ab <=90:
        #Robot steht an der west. Bande
        #reset(90)
        bewaessere_und_zerstoere(debug=False) 

    if starte_ab <=100:
        #reset(90)
        arme("beide","runter")
        go(480)
        turn(-90)
        go(150)
        turn(90)
        go(500)
    
    get_status("main ende")
 
# MAiN - ENDE
#: #############################################################################
#  pybricksdev run ble --name "mimi" wro_mimi.py
 


if __name__ == "__main__": 

    starte_ab=10
    if starte_ab <1000:
        main(starte_ab)

    if starte_ab >=1001:
        reset(90)
        gefahrene_distanz = folge_linie(["BLACK", "GREEN"],  max_gefahrene_distanz=1000, telemetrie=True)

    print(zeiten)
    get_status("ENDE")
