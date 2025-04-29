from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Axis
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.parameters import Icon
watch = StopWatch()
hub = PrimeHub()

left = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right = Motor(Port.B)
heber = Motor(Port.E)
heber2 = Motor(Port.C)
robot = DriveBase(left, right, wheel_diameter=88, axle_track=160) #276
robot.use_gyro(True) 
 

turn=robot.turn 
go=robot.straight
drive_speed = 400
#go(-200)
side_cs = ColorSensor(Port.F)


line_cs = ColorSensor(Port.D)
line_cs.color(surface=True)
 
 
def log( message="",log_level=3):
    timestamp = int(watch.time()/1000)
    log_string = f"{timestamp} - {log_level} - {message}"
    
    if log_level>=3:
        print(log_string)  # Output to the console
 
   
 
 
gesehene_farben_linie=[Color.NONE,Color.NONE] #hilfs Liste


def get_farbe_am_boden(log_level=3):
    """
    return: letzten drei Farben, NUR für die Erkennung der Farben entlang der Linie,
    da schwarz und weiß sonst nicht gut erkannt werden, dazwischen wird es als grün erkannt !!!!
    #Color.RED =  Color(h=353, s=77, v=57)
    #Color.WHITE =  Color(h=213, s=15, v=84)
    #Color.BLACK= Color(h=240, s=15, v=17)
    """ 
    reflection = line_cs.reflection() 
    hsv = line_cs.hsv()
    if hsv.h==0 and hsv.h==0 and hsv.v==0:
        berechnete_farbe=Color.NONE

    elif hsv.h>300 or hsv.h<10:
        berechnete_farbe=Color.RED
    elif hsv.h>25 and hsv.h<80:
        berechnete_farbe=Color.YELLOW
    elif (hsv.s>40 and hsv.s<90) and (hsv.h >150 and hsv.h<200):
        berechnete_farbe=Color.GREEN
    elif hsv.v<30 and hsv.s<30 :
        berechnete_farbe=Color.BLACK
    elif hsv.s<40 and hsv.h>180 : 
        berechnete_farbe=Color.WHITE
    else:
         berechnete_farbe=Color.NONE
         log(f"{berechnete_farbe=}, {hsv=}, {reflection=} ",log_level=3)
 
    log(f"{berechnete_farbe=}, {hsv=}, {reflection=} ",log_level=log_level)
 
    return berechnete_farbe
################################################################################  
################################################################################
 
 
#:
def fahre_bis_zur_farbkombi(stoppe_bei_farbmuster=[Color.RED,Color.WHITE], 
                            max_gefahrene_distanz=100, log_level=1):
    #
    #
    gesehene_boden_farben=[Color.NONE,Color.NONE]
    start_distance = robot.distance()
    heading = int(hub.imu.heading())
    if log_level>=3:
        log(f"{stoppe_bei_farbmuster=}")

    while True:
        aktuelle_farbe = get_farbe_am_boden(log_level=1)  

        gefahrene_distanz = robot.distance() - start_distance
        if  gefahrene_distanz >= max_gefahrene_distanz:
            robot.stop()
            log(f"Stoppe Motor (Distanz): {gefahrene_distanz}")
            break

        robot.drive(100, 0)  

        if gesehene_boden_farben[-1] != aktuelle_farbe:
            gesehene_boden_farben.append(aktuelle_farbe) 
   
        if gesehene_boden_farben[-2:] == stoppe_bei_farbmuster : 
            robot.stop()
            log(f"Stoppe Motor (Farben): {gesehene_boden_farben[-2:]}, Distanz: {gefahrene_distanz}")
            return gefahrene_distanz 
        wait(100) 
    log(f"Stoppe Motor (Farben): {gesehene_boden_farben[-4:]}, Distanz: {gefahrene_distanz}")


#: 
def folge_linie(stoppe_bei_farbmuster=[Color.BLACK,Color.RED],              \
                max_gefahrene_distanz=500, max_v=200, end_ausrichtung=90,   \
                drive_speed=100, algo_bis_distanz=500, debug=2): 
    """ Kann NUR LINKS von der schwarzen Linie fahren, in beiden RICHTUNGEN 
    """
    white_reflection = 62
    black_reflection = 8 

    threshold = (white_reflection - black_reflection) / 2 
    gesehene_farben_linie=[Color.NONE,Color.NONE]
    gesehene_boden_farben=[Color.NONE,Color.NONE]

    PROPORTIONAL_GAIN = 0.5 
    last_color=Color.NONE
    
    start_distance = robot.distance()
    distanz_auf_der_linie_start = 0
    correction_unter_0_5_anzahl = 0
    correction_ueber_0_5_anzahl = 0
    weisse_linie_beruehrt = 0
    schwarze_linie_beruehrt = 0
    winkel_korrektur=0
    is_robot_ausgerichtet = False
    letzer_durchlauf = watch.time()
    # 50 um die Linie sicher zu finden
    # später fahren wir schneller
    slow_v= 60
    drive_speed=slow_v
    robot.settings(straight_speed=drive_speed)
  
    while True:
        aktuelle_farbe = get_farbe_am_boden(log_level=1)  
        gesehene_farben_linie.append(aktuelle_farbe)
        deviation = line_cs.reflection() - threshold 
        try:
            gesehene_farben_linie=gesehene_farben_linie[-3:]
        except:
            continue
            wait(10)

        farbe_dict={Color.BLACK:0, Color.RED:0, Color.WHITE:0} 
        farbe_dict[Color.BLACK]=gesehene_farben_linie.count(Color.BLACK)
        farbe_dict[Color.RED]=gesehene_farben_linie.count(Color.RED)
        farbe_dict[Color.WHITE]=gesehene_farben_linie.count(Color.WHITE)
 
        # eine Liste: wie oft wurde die Farbe gesehen
        farbe_dict_sortiert = sorted(farbe_dict, key=farbe_dict.get, reverse=True) 
        aktuelle_farbe = farbe_dict_sortiert[0]  
        
        if gesehene_boden_farben[-1] != aktuelle_farbe:
            gesehene_boden_farben.append(aktuelle_farbe)
            gesehene_farben_linie=[]

            print(f"folge_linie: Neue Farbe gefunden:  {aktuelle_farbe=} / {line_cs.hsv()=}  /reflection: {line_cs.reflection()} /  {deviation=}, ,heading: {int(hub.imu.heading())}, /", \
            f"/gesehene {gesehene_boden_farben[-2:]}  {stoppe_bei_farbmuster=} " )  
        
        Kp = 0.5 
        correction = Kp * deviation
         #: ab algo_bis_distanz  soll der Roboter geradeaus fahren, dh 
        if robot.distance() - start_distance >=  algo_bis_distanz :
            turn_rate = 0
            log(f"TURNRATE auf 0 gesetzt {heading=} {correction}" )

        if abs(correction) <= 1:
            correction_unter_0_5_anzahl = correction_unter_0_5_anzahl + 1
        else:
            correction_ueber_0_5_anzahl=correction_ueber_0_5_anzahl+1

        turn_rate = correction  
        heading = int(hub.imu.heading())    
        
        gefahrene_distanz = robot.distance()- start_distance
        
        if gesehene_boden_farben[-2:] == stoppe_bei_farbmuster: 
            robot.stop()
            
            log(f"folge_linie: Stoppe Motor FARBMUSTER: {gesehene_boden_farben[-2:]}, {gefahrene_distanz=}")
            log(f"{is_robot_ausgerichtet}, {schwarze_linie_beruehrt=}, {weisse_linie_beruehrt=}")
            #:           
            break
            return gefahrene_distanz
        elif  gefahrene_distanz >= max_gefahrene_distanz:
            robot.stop()
            log("folge_linie: stoppe Motor (Distanz): {gefahrene_distanz} ")
            return gefahrene_distanz

        if aktuelle_farbe in [Color.WHITE, Color.BLACK]: 
            drive_speed = max_v if is_robot_ausgerichtet else slow_v

            if correction_unter_0_5_anzahl>5 and is_robot_ausgerichtet is False:
                robot.reset()
                is_robot_ausgerichtet=True
                schwarze_linie_beruehrt=0
                weisse_linie_beruehrt=0
            #:
            robot.drive(drive_speed, turn_rate) 
            #:
            if aktuelle_farbe in [Color.WHITE]:
                white_reflection_aktuell = line_cs.reflection()
                weisse_linie_beruehrt =weisse_linie_beruehrt + 1 
            if aktuelle_farbe in [Color.BLACK]:
                schwarze_linie_beruehrt =schwarze_linie_beruehrt + 1 
                black_reflection_aktuell = line_cs.reflection() 

        else: 
            if is_robot_ausgerichtet:
                log(f"folge_linie: andere Farber als B/W gefunden, nach is_robot_ausgerichtet {gesehene_boden_farben[-2:]}   {stoppe_bei_farbmuster}")  
                hub.speaker.beep() 
                robot.stop()
                break
            log(f"folge_linie: SUCHE WEIßE LINIE")  
            robot.stop()
            drive_speed = 30
            n_weisse_linie_gesucht=0
            aktuelle_farbe=get_farbe_am_boden()
            while  aktuelle_farbe not in [Color.WHITE, Color.BLACK]:
                n_weisse_linie_gesucht=n_weisse_linie_gesucht+1
                turn(7)
                go(20) 
                log(f"folge_linie: suche weiße Linie  {n_weisse_linie_gesucht=}  / {aktuelle_farbe=}")  
                aktuelle_farbe=get_farbe_am_boden()
            turn(n_weisse_linie_gesucht*-1*2.5)
            
        if watch.time()- letzer_durchlauf>1000 :
            log(f"{is_robot_ausgerichtet=}, {schwarze_linie_beruehrt=}, {weisse_linie_beruehrt=}, {correction=}, {correction_unter_0_5_anzahl=} / {correction_ueber_0_5_anzahl=}") 
            letzer_durchlauf=watch.time()      
        wait(15) # ms 15 
 

#fahre_bis_zur_farbkombi(stoppe_bei_farbmuster=[Color.RED,Color.WHITE])
#fahre_bis_zur_farbkombi(stoppe_bei_farbmuster=[Color.WHITE,Color.BLACK],max_gefahrene_distanz=300)
# fahre_bis_zur_farbkombi(stoppe_bei_farbmuster=[Color.BLACK,Color.RED])

# go(120)
# turn(-90)
# folge_linie(stoppe_bei_farbmuster=[Color.WHITE, Color.RED], max_gefahrene_distanz=175,end_ausrichtung=90, debug=True)
# turn(90)
# folge_linie(stoppe_bei_farbmuster=[Color.WHITE, Color.RED], max_gefahrene_distanz=400,end_ausrichtung=90, debug=True)
# go(30)
# turn(90)
# go(270)

# go(-400)

"""

['go 30', 'turn -30', 'settings', 'settings 200,200,200,200', 'go 30', 'go 30', 't -90', 'go 40', 'go 400', 'go 200', 'fl_s br', 'go 50', 'g -200', 'hist']
"""
def reset_robot( angle=0, debug=0):
    #robot.settings(straight_speed=400)
    #motor_l.reset_angle(0)
    #motor_r.reset_angle(0)
    robot.reset() # reset angle AND heading

  
    if debug:
        print("heading: ",abs(round(hub.imu.heading(),1)))
        
def reset(angle=0):
    get_status("reset") 
    reset_robot(angle=angle) 
    #get_status("Start") 

def reset_heber(debug=False):
    """
    arme gehen runter, dann wird der Winkel gesetzt
    damit wir später wissen, ob der Arm ganz unten ist
    """
    heber.run_until_stalled(200, duty_limit=50)  
    heber.reset_angle(82) 
    if debug:
        print (f"heber.angle: {heber.angle()}  }")

def get_status(kommentar=""):
    vergangene_zeit = int(watch.time()/1000)
    #hub.display.number(vergangene_zeit)
    heading= int(hub.imu.heading())
    color  = line_cs.color()
    color_get_farbe_am_boden = get_farbe_am_boden(log_level=3)
    hsv  = line_cs.hsv()
    reflection = line_cs.reflection()
    distance = robot.distance()
    settings = robot.settings()
    state = robot.state()
    angle = robot.angle()
    anggular_velocity= hub.imu.angular_velocity()
    status = (f"""{kommentar=}:  {heading=} / {color=} /{color_get_farbe_am_boden=} / {hsv=}/ {reflection=} / {distance=} / {settings=} / {state=} /  {angle=} """)
    print(status) 
    return status

def side_farbe(log_level=3):
    reflection = side_cs.reflection() 
    berechnete_farbe=Color.NONE
    hsv = side_cs.hsv()   
    """
        ROT: h>300 or h < 10
        YELLOW: h> 25 and h<80
        GREEN: s>35 and s<70 and h <150 and h<200
        WHITE: s<30/ Color(h=300, s=9, v=13)
    """
    if hsv.h==0 and hsv.h==0 and hsv.v==0:
        berechnete_farbe=Color.NONE 
    elif hsv.h>300 or hsv.h<10 and hsv.s>75:
        berechnete_farbe=Color.RED
    elif hsv.h>25 and hsv.h<80:
        berechnete_farbe=Color.YELLOW
    elif (hsv.s>40 and hsv.s<90) and (hsv.h >=110 and hsv.h<200):
        berechnete_farbe=Color.GREEN
    elif hsv.s<40: 
        berechnete_farbe=Color.WHITE
    
    log(f"{reflection=}, {berechnete_farbe=}, {hsv=}",log_level=log_2level)
    return berechnete_farbe

## TESTS
def test_boden_farben():
    robot.reset()
    robot.distance()
    gesehene_farben:dict={}
    while robot.distance() < 180:
        aktuelle_farbe = get_farbe_am_boden(log_level=1)  
        gesehene_farben[aktuelle_farbe] = gesehene_farben.get(aktuelle_farbe,0)+1
        robot.drive(100, 0) 
        wait(15)
    print (f"{gesehene_farben=}, erwartet ca ''")
    robot.stop()

def test_proben_farben():
    robot.reset()
    robot.distance()
    robot.settings(150,200,200,200)
    proben_pos:list=[]
    for i in range (5):
        berechnete_farbe=side_farbe()
        proben_pos.append(berechnete_farbe)
        go(100)
    print(proben_pos)

def test_proben_farben_2():
    robot.reset()
    robot.distance()
    gesehene_farben:dict={}
    watch.reset()
    
    while robot.distance() < 500:
        aktuelle_farbe=side_farbe() 
        gesehene_farben[aktuelle_farbe] = gesehene_farben.get(aktuelle_farbe,0)+1
        robot.drive(100, 0) 
        wait(20)
    print (f"{gesehene_farben=}")
    robot.stop()

    

#hub.speaker.volume(50)
#folge_linie(stoppe_bei_farbmuster=[Color.WHITE, Color.RED], max_gefahrene_distanz=300,end_ausrichtung=90, debug=True) 
def interactive():
    
    user_input_history:list=[]
    farb_parameter:dict={"rw":[Color.RED,Color.WHITE]
                    ,'wr':[Color.WHITE, Color.RED]
                    ,'wb':[Color.WHITE, Color.BLACK]
                    ,'bw':[Color.BLACK,Color.WHITE]
                    ,'br':[Color.BLACK,Color.RED]
                    ,'rb':[Color.RED,Color.BLACK]
                    }
    while True:
        user_input = input("command:")
        user_input_history.append(user_input)
        parameter=""
        try: 
            cmd, parameter = user_input.split(" ")
        except:
            cmd = user_input

        #print(f"{cmd=} {parameter=}")
        if cmd in ['exit','quit']:
            return 0
        
        if cmd in ['test_boden_farben']: 
            test_boden_farben()

        if cmd in ['hist','h']:
            print (user_input_history)

        if cmd in ['go','g']:
            drive_speed=200
            robot.settings(straight_speed=drive_speed)
            go(int(parameter),Stop.COAST_SMART)
            get_status()

        if cmd in ['turn','t']:
            turn(int(parameter),Stop.COAST_SMART)
            get_status()

        if cmd in ['info', 'i']:
            get_status()

        if cmd in ['reset_robot','rs']:
            try:
                angle = int(parameter)
            except:
                angle=0
            reset_robot(angle)
            drive_speed=200
            robot.settings(straight_speed=drive_speed)
            get_status()

        if cmd in ['folge_linie','fl','fls']:
            robot.reset()
            watch.reset()
            try:
                distanz = int(parameter)
            except:
                distanz=400
            folge_linie( max_gefahrene_distanz=distanz,end_ausrichtung=90, debug=True) 
            get_status()
            #hub.speaker.beep()

        if cmd in ['folge_linie_stoppe','fl_s']:
            watch.reset()
            
            if ',' in parameter:
                farb_muster,max_distanz = parameter.split(",")
                max_distanz=int(max_distanz)
            else:
                farb_muster=parameter
                max_distanz=500
            folge_linie(stoppe_bei_farbmuster=farb_parameter[farb_muster],max_v=50, max_gefahrene_distanz=max_distanz,end_ausrichtung=90,algo_bis_distanz=100, debug=True) 



        if cmd in ["heber2_reset",'h2_reset']:
            heber2.run_until_stalled(-200)
            hub.speaker.volume(25)
            hub.speaker.beep()
         
        
        if cmd in ['farb_combi','fb']: 

            if ',' in parameter:
                farb_muster,max_distanz = parameter.split(",")
                max_distanz=int(max_distanz)
            else:
                farb_muster=parameter
                max_distanz=500
           
            fahre_bis_zur_farbkombi(stoppe_bei_farbmuster=farb_parameter[farb_muster],  max_gefahrene_distanz=max_distanz, log_level=1)

        if cmd=='get_farbe_am_boden':
            print(get_farbe_am_boden())
        
        if cmd=='curve':
            radius,angle = parameter.split(",")
            robot.curve(int(radius), angle=int(angle))

        if cmd == 'rh':
            reset_heber()
        if cmd in ['heber','h']:
            v,grad = parameter.split(",")
            heber.run_angle(int(v),int(grad))
            settings = heber.settings()
            angle = heber.angle()
            log(f"{settings=}, {angle=}")
   

        if cmd in ["heber2_reset",'h2_reset']:
            heber2.run_until_stalled(-200)
            settings = heber2.settings()
            heber2.reset_angle(0)
            angle = heber2.angle()
            log(f"{settings=}, {angle=}")

        if cmd in ["heber2",'h2']:
            if ',' in parameter:
                v,grad = parameter.split(",")
                v=int(v)
                grad=int(grad)
            else:
                v=200 
                grad=int(parameter)  
            
            heber2.run_angle(v,grad)
            #heber2.settings(2000)
            settings = heber2.settings()
            angle = heber2.angle()
            log(f"{settings=}, {angle=}")
        
        if cmd =="h2_check":
            heber2.run_angle(100,-20,wait=False) 

            while not heber2.done() : 
                if heber2.stalled():
                    heber2.stop()
                    log(f"heber2 stalled, gehe 2cm zurück")
                    go(-20)
                wait(100)
            print("heber nicht stalled")
                
        if cmd=="settings":
            v, v_acc, t, t_acc =200,200,50,50
            
            if "," in parameter:
                v, v_acc, t, t_acc = parameter.split(",")
            
            robot.settings(int(v),int(v_acc), int(t),int(t_acc))
            print(robot.settings())
        
        if cmd=="wall":
            go(-50)
            robot.use_gyro(False)
            robot.reset()
            robot.use_gyro(True)


        if cmd=='ss':
            berechnete_farbe=side_farbe()

        if cmd=='p':
            test_proben_farben()

        if cmd=="proben_1":
            farb_muster="br"
            folge_linie(stoppe_bei_farbmuster=farb_parameter[farb_muster],max_v=50, max_gefahrene_distanz=300,end_ausrichtung=90,algo_bis_distanz=100, debug=True) 
            v, v_acc, t, t_acc =100,100,40,40
            robot.settings(int(v),int(v_acc), int(t),int(t_acc))
            go(30)
            turn(30)
            go(50)
            turn (-30)
            go(30) 
            turn(-96) 
            v, v_acc, t, t_acc =300,200,40,40
            robot.settings(int(v),int(v_acc), int(t),int(t_acc))
            go(600)
            folge_linie(stoppe_bei_farbmuster=farb_parameter[farb_muster],max_v=50, max_gefahrene_distanz=300,end_ausrichtung=90,algo_bis_distanz=100, debug=True) 
            robot.settings(int(v),int(v_acc), int(t),int(t_acc))
            go(70)
            go(-920)
            turn(90)
            go(-100)

            
    log(f"{aktuelle_farbe=}, {hsv=}, {reflection=} ",log_level=log_level)
 
 
interactive()
 
#heber2.run_until_stalled(200)
#heber2.run_angle(100,-180)
#folge_linie(stoppe_bei_farbmuster=[Color.BLACK, Color.RED],max_v=50, max_gefahrene_distanz=300,end_ausrichtung=90, debug=True) s

#heber2.run_angle(50,30)
#heber2.run_angle(100,65)
#heber2.run_angle(100,-65)
"""

 'wall', 'fl_s br', 'go 30', 'turn 30', 'go 50', 'turn -30', 'go 30', 'turn -90', 'hist']

# mission linie zu den Proben
fl_s_wr
reset_robot
g 100
t 90
go 450
fb wr
g 180
t 90
g 60
p


# von der linie Proben aufheben
fl_s br
g -50
h2_reset
h2 -160
t 10
go 70

"""
robot.settings(200,200,200,200)
def wasserturm():
    go(30)
    folge_linie(stoppe_bei_farbmuster=[Color.WHITE,Color.RED], max_gefahrene_distanz=200, end_ausrichtung=90,drive_speed=600, debug=2)
    go(40)
    turn(-90)
    folge_linie(stoppe_bei_farbmuster=[Color.GREEN,Color.NONE], max_gefahrene_distanz=330, end_ausrichtung=90,drive_speed=100, debug=2)
    turn(90)
    folge_linie(stoppe_bei_farbmuster=[Color.GREEN,Color.NONE], max_gefahrene_distanz=50, end_ausrichtung=90,drive_speed=100, debug=2)
    turn(-25)
    go(-70)
    turn(25)
    heber.run_angle(100,165)

def hole():
    go(-160)
    go(80)
    go(-180)
    go(150)


def lager():
    heber.run_angle(100,-25)

    go(100)

    heber2.run_angle(100,165)
    go(-140)
    heber2.run_angle(100,-165)
    turn(-90)

def weg():
    folge_linie(stoppe_bei_farbmuster=[Color.WHITE,Color.RED], max_gefahrene_distanz=400, end_ausrichtung=90,drive_speed=100, debug=2)
    go(30)
    turn(-90)
    
def offen():
    go(-150)
    heber2.run_angle(100,160)
    go(160)
    heber2.run_angle(100,-50)
    go(80)
    heber2.run_angle(100,-20)
def rein():
    heber.run_angle(100,-140)
    go(-50)
    heber2.run_angle(100,50)

def drohne():
    go(-100)
    turn(-90)
    heber2.run_angle(100,-120)
    heber.run_angle(100,-15)
    go(-200)
    go(30)
    turn(-90)
    go(800)
    turn(90)
    go(850)
    turn(90)
    go(900)
    

# wasserturm()
# hole()
# weg()
# # lager()
# offen()
# rein()
# drohne()
# go(100)
# heber2.run_angle(100,35)