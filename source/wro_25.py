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
robot = DriveBase(left, right, wheel_diameter=88, axle_track=160)
robot.use_gyro(True) 
 

turn=robot.turn 
go=robot.straight
drive_speed = 400
side_cs = ColorSensor(Port.F)
line_cs = ColorSensor(Port.D)
line_cs.color(surface=True)
 

farb_parameter:dict={"rw":[Color.RED,Color.WHITE]
                ,'wr':[Color.WHITE, Color.RED]
                ,'wb':[Color.WHITE, Color.BLACK]
                ,'bw':[Color.BLACK,Color.WHITE]
                ,'br':[Color.BLACK,Color.RED]
                ,'rb':[Color.RED,Color.BLACK]
                }

def log( message="",log_level=1):
    timestamp = int(watch.time())
    log_string = f"{timestamp:,} - {message}"
    
    if log_level>=3:
        print(log_string)  # Output to the console
 
   
 
 
gesehene_farben_linie=[Color.NONE,Color.NONE] #hilfs Liste


def get_farbe_am_boden(log_level=1):
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
         log(f"{berechnete_farbe=}, {hsv=}, {reflection=} ",log_level=1)
 
    log(f"{berechnete_farbe=}, {hsv=}, {reflection=} ",log_level=log_level)
 
    return berechnete_farbe
################################################################################  
################################################################################

 
#:
def fahre_bis_zur_farbkombi(stoppe_bei_farbmuster=[Color.RED,Color.WHITE], 
                            max_gefahrene_distanz=300, log_level=1):
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
                max_gefahrene_distanz=500, max_v=500, end_ausrichtung=90,   \
                algo_bis_distanz=500, log_level=1): 
    """ Kann NUR LINKS von der schwarzen Linie fahren, in beiden RICHTUNGEN 
    """
    white_reflection = 50
    black_reflection = 8 

    threshold = (white_reflection - black_reflection) / 2 
    gesehene_farben_linie=[Color.NONE,Color.NONE]
    gesehene_boden_farben=[Color.NONE,Color.NONE]

 
    last_color=Color.NONE
    
    start_distance = robot.distance()
    distanz_auf_der_linie_start = 0
    correction_unter_threshold_anzahl = 0
    correction_ueber_threshold_anzahl = 0
    weisse_linie_beruehrt = 0
    schwarze_linie_beruehrt = 0
    winkel_korrektur=0
    is_robot_ausgerichtet = False
    letzer_durchlauf = watch.time()

    # 50 um die Linie sicher zu finden
    # später fahren wir schneller
    integral = 0
    last_error = 0
    Kp, Ki, Kd = 0.65, 0.0002, 1.0

    slow_v= int(max_v *0.75) if max_v > 100 else 50
    drive_speed=max_v
    v,v_agg,t,t_agg = robot.settings()
    print(slow_v)
    robot.settings(slow_v,slow_v,100,500)
  
    while True:
        aktuelle_farbe = get_farbe_am_boden(log_level=1)  
        gesehene_farben_linie.append(aktuelle_farbe)
        error = line_cs.reflection() - threshold 

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
        
        
        heading = int(hub.imu.heading())   
        integral += error
        derivative = error - last_error 
        correction = Kp * error + Ki * integral + Kd * derivative
        last_error = error
         #: ab algo_bis_distanz  soll der Roboter geradeaus fahren  
        if robot.distance() - start_distance >=  algo_bis_distanz :
            turn_rate = heading*-1 
            log(f"\t\tTURNRATE auf {heading=} gesetzt {correction}",log_level=log_level )

        if abs(correction) <= 2:
            correction_unter_threshold_anzahl = correction_unter_threshold_anzahl + 1
        else:
            correction_ueber_threshold_anzahl=correction_ueber_threshold_anzahl+1

        turn_rate = correction   
        gefahrene_distanz = robot.distance()- start_distance

        if gesehene_boden_farben[-1] != aktuelle_farbe:
            gesehene_boden_farben.append(aktuelle_farbe)
            gesehene_farben_linie=[]

            log(f"folge_linie:\tNeue Farbe gefunden:  {aktuelle_farbe=} / {str(line_cs.hsv())=}  / reflection: {str(line_cs.reflection())} /  {error=}, heading: {heading}\n\t\t\tgesehene {gesehene_boden_farben[-2:]}  {stoppe_bei_farbmuster=}",log_level=log_level )  
        
        if gesehene_boden_farben[-2:] == stoppe_bei_farbmuster:  
            log(f"\tStoppe Motor FARBMUSTER: {gesehene_boden_farben[-2:]}, {gefahrene_distanz=}",log_level=log_level)
            log(f"\t{is_robot_ausgerichtet}, {schwarze_linie_beruehrt=}, {weisse_linie_beruehrt=}",log_level=log_level) 
            break 
        elif  gefahrene_distanz >= max_gefahrene_distanz: 
            log("\tstoppe Motor (Distanz): {gefahrene_distanz} ",log_level=log_level)
            break
           

        if aktuelle_farbe in [Color.WHITE, Color.BLACK]: 
            drive_speed = max_v if is_robot_ausgerichtet else max_v*0.75

            if correction_unter_threshold_anzahl>5 and is_robot_ausgerichtet is False:
                robot.stop() 
                robot.use_gyro(False)
                hub.imu.reset_heading(0)
                robot.use_gyro(True)
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
                log(f"\tandere Farberals B/W gefunden, nach is_robot_ausgerichtet {gesehene_boden_farben[-2:]}   {stoppe_bei_farbmuster}",log_level=log_level)  
                hub.speaker.beep() 
                robot.stop()
                log(f"\tw SUCHE WEIßE LINIE",log_level=log_level)
                
                break
            log(f"\tw SUCHE WEIßE LINIE",log_level=log_level)  
            robot.stop()  
            robot.use_gyro(False)
            hub.imu.reset_heading(0)
            robot.use_gyro(True)    
            robot.settings(straight_speed=200,turn_acceleration=200)
            aktuelle_farbe=get_farbe_am_boden()
            while  aktuelle_farbe not in [Color.BLACK,Color.WHITE]:
                while  aktuelle_farbe not in [Color.BLACK,Color.WHITE]:
                    robot.drive(int(40),  int(100))
                    wait(30)
                    aktuelle_farbe=get_farbe_am_boden(log_level=log_level)
                robot.stop() 
                go(80,then=Stop.NONE)   
                w_l_turn_rate=hub.imu.heading() *-1
                log(f"\t SUCHE WEIßE LINIE: auf Weiss/BLack gelandet:  {w_l_turn_rate=}",log_level=log_level)  
                turn( w_l_turn_rate,then=Stop.BRAKE)
                aktuelle_farbe=get_farbe_am_boden()
            
            # annhame das suchen der w. linie kostet 5cm
            start_distance = robot.distance()
            max_gefahrene_distanz=max_gefahrene_distanz-100 
     
            
        if watch.time()- letzer_durchlauf>1000 :
            log(f"\t{is_robot_ausgerichtet=}, {schwarze_linie_beruehrt=}, {weisse_linie_beruehrt=}, {correction=}, {correction_unter_threshold_anzahl=} \n\t\t\t\t/ {correction_ueber_threshold_anzahl=}, {gefahrene_distanz=}",log_level=log_level) 
            letzer_durchlauf=watch.time()      
        wait(15) # ms 15 
    robot.stop() 
    robot.settings( v,v_agg,t,t_agg)
    return gefahrene_distanz
 

 
def reset_robot( angle=0 ):
    #robot.settings(straight_speed=400)
    #motor_l.reset_angle(0)
    #motor_r.reset_angle(0)
    robot.reset() # reset angle AND heading 
  
    
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

def heber2_reset(log_level=1):
    heber2.run_until_stalled(-200)
    settings = heber2.settings()
    heber2.reset_angle(0)
    angle = heber2.angle()
    log(f"{settings=}, {angle=}",log_level)

def get_status(kommentar="",log_level=3):
    vergangene_zeit = int(watch.time()/1000)
    #hub.display.number(vergangene_zeit)
    heading= int(hub.imu.heading())
    color  = line_cs.color()
    color_get_farbe_am_boden = get_farbe_am_boden()
    hsv  = line_cs.hsv()
    reflection = line_cs.reflection()
    side_color=side_farbe(log_level=1)
    distance = robot.distance()
    settings = robot.settings()
    state = robot.state()
    angle = robot.angle()
    anggular_velocity= hub.imu.angular_velocity()
    status = (f"""{kommentar=}:  {heading=} / {color=} /{color_get_farbe_am_boden=} / {hsv=}/ {reflection=} / {distance=} / {settings=} / {state=} /  {angle=} / {side_color} """)
    log(status,log_level) 
    return status

def side_farbe(log_level=1):
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
    
    log(f"{reflection=}, {berechnete_farbe=}, {hsv=}",log_level=log_level)
    return berechnete_farbe,reflection
################################################################################
## TESTS
################################################################################
def test_boden_farben():
    robot.reset()
    robot.distance()
    gesehene_farben:dict={}
    while robot.distance() < 180:
        aktuelle_farbe = get_farbe_am_boden(log_level=3)  
        gesehene_farben[aktuelle_farbe] = gesehene_farben.get(aktuelle_farbe,0)+1
        robot.drive(100, 0) 
        wait(15)
    print (f"{gesehene_farben=}, erwartet ca 'Color.RED: 70, Color.WHITE: 35, Color.BLACK: 12'")
    robot.stop()

def test_proben_farben():
    robot.reset()
    robot.distance()
    robot.settings(150,200,200,200)
    proben_pos:list=[]
    for i in range (5):
        berechnete_farbe,probe_reflektion=side_farbe()
        proben_pos.append(berechnete_farbe)
        go(100)
    print(proben_pos)


def wall(distanz=200): 
    go(distanz*-1,then=Stop.BRAKE)
    robot.use_gyro(False)
    robot.reset()
    robot.use_gyro(True)
#: #############################################################################
  
def drive_distanz(turn_rate,distanz,speed=100):
    start_distanz = robot.distance()
    while  robot.distance()-start_distanz <=distanz:
        robot.drive(speed,  turn_rate)
        wait(10)
    robot.stop()

#:    
def interactive():
    
    user_input_history:list=[]
 
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
            go(int(parameter))
            get_status()

        if cmd in ['turn','t']:
            turn(int(parameter))
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

        if cmd in ['folge_linie','fl']:
            robot.reset()
            watch.reset()
            try:
                distanz = int(parameter)
            except:
                distanz=300
            folge_linie( max_gefahrene_distanz=distanz,end_ausrichtung=90, max_v=100, log_level=3) 
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
            folge_linie(stoppe_bei_farbmuster=farb_parameter[farb_muster],max_v=100, max_gefahrene_distanz=max_distanz,end_ausrichtung=90,algo_bis_distanz=100, log_level=1) 



        if cmd in ["heber2_reset",'h2_reset']:
            heber2.run_until_stalled(-200)
            hub.speaker.volume(25)
            hub.speaker.beep()
         
        
        if cmd in ['farb_combi','fb']: 

            if ',' in parameter:
                farb_muster,max_distan    # # probe_pos_1=1

                max_distanz=int(max_distanz)
            else:
                farb_muster=parameter
                max_distanz=500
           
            fahre_bis_zur_farbkombi(stoppe_bei_farbmuster=farb_parameter[farb_muster],  max_gefahrene_distanz=max_distanz, log_level=1)

        if cmd=='get_farbe_am_boden':
            print(get_farbe_am_boden())
        
        if cmd=='curve':
            radius,angle = parameter.split(",")
            robot.curve(int(radius), angle=int(angle), then=Stop.COAST_SMART)


        if cmd=="drive":
            speed=100
            try:
                turn_rate,distanz = parameter.split(",")
                distanz=int(distanz)
                turn_rate=int(turn_rate)
            except:
                turn_rate,distanz = 0,60
            drive_distanz(turn_rate,distanz) 
            
 
           
        if cmd in ['heber1_reset',"h1_reset"]:
            reset_heber()

        if cmd in ['heber1','h1']:
            if ',' in parameter:
                v,grad = parameter.split(",")
                v=int(v)
                grad=int(grad)
            else:
                v=200 
                grad=int(parameter)  
            heber.run_angle(int(v),int(grad))
            settings = heber.settings()
            angle = heber.angle()
            log(f"{settings=}, {angle=}")
   

        if cmd in ["heber2_reset",'h2_reset']:
            heber2_reset()

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
            v, v_acc, t, t_acc =100,100,100,500
            
            if "," in parameter:
                v, v_acc, t, t_acc = parameter.split(",")
            
            robot.settings(int(v),int(v_acc), int(t),int(t_acc))
            print(robot.settings())
        
        if cmd=="wall":
            try:
                distanz=int(parameter) 
            except:
                distanz=150
            go(distanz*-1,then=Stop.COAST_SMART) 
            robot.reset()
      


        if cmd=='ss':
            berechnete_farbe,probe_reflektion=side_farbe(log_level=3)

        if cmd=="proben_lesen":

            fahre_bis_zur_farbkombi(stoppe_bei_farbmuster=farb_parameter["wr"],max_gefahrene_distanz=500, log_level=3)
            v, v_acc, t, t_acc =100,100,40,40
            robot.settings(int(v),int(v_acc), int(t),int(t_acc))
            go(180)
            turn(90)
            wall(100)
            proben_aufstellung_lesen(log_level=3)
        if cmd=='p':
            test_proben_farben()

        if cmd =='pl':
            try:
                pos_1, pos_2 = parameter.split(",")
            except:
                pos_1=0
                pos_2=1
            probe_stehe_links(int(pos_1),int(pos_2)) 
            go(0,then=Stop.COAST_SMART)
            get_status()

        if cmd=="proben_1":
            farb_muster="br"
            folge_linie(stoppe_bei_farbmuster=farb_parameter[farb_muster],max_v=50, max_gefahrene_distanz=300,end_ausrichtung=90,algo_bis_distanz=100) 
            v, v_acc, t, t_acc =100,100,40,40
            robot.settings(int(v),int(v_acc), int(t),int(t_acc))
            turn(30)
            #hier kommt eine variable Strecke hinzu, abhängig, ob das nächste Feld frei ist oder nicht +10cm
            go(50) 
            turn(-30)
            go(50)
            turn (-40)
        if cmd=='ml':
            grad=int(parameter)
            left.run_angle(100,grad)
        if cmd=='mr':
            grad=int(parameter)
            right.run_angle(100,grad)
            
    log(f"{aktuelle_farbe=}, {hsv=}, {reflection=} ",log_level=log_level)
#:
################################################################################

#: ############################################################################
def fahre_zum_wasserturm():
    #steht am Start
    robot.settings(300,300,200,500)
    #go(150)
    #folge_linie(stoppe_bei_farbmuster=[Color.WHITE,Color.RED], max_gefahrene_distanz=200, max_v=200)
    #go(40,then=Stop.COAST_SMART)
    go(320)
    turn(-90,then=Stop.COAST_SMART)
    # entlang der langen Linie
    robot.settings(200,200,150,150)
    folge_linie(max_gefahrene_distanz=320, max_v=200) 
    turn(90,then=Stop.COAST_SMART)
    #wallen
    robot.settings(200,200,150,150)
    go(-200,then=Stop.COAST_SMART) 
    folge_linie(max_gefahrene_distanz=150, max_v=200)
    heber.run_until_stalled(200, duty_limit=50)

    # hole die beiden Bälle
    go(-100,then=Stop.COAST_SMART)
    
    robot.settings(500,900,100,100)

    go(50,then=Stop.COAST_SMART) 
    go(-70,then=Stop.COAST_SMART)
    robot.settings(200,200,100,100)
    go(100,then=Stop.COAST_SMART)
    heber.run_angle(50,-25,wait=False)
 

def fahre_vom_wasserturm_zum_lager(): 
    robot.settings(200,200,150,100)
    turn(-90,Stop.BRAKE)
    folge_linie(stoppe_bei_farbmuster=[Color.WHITE,Color.RED],max_v=200, max_gefahrene_distanz=400)
    go(30)
    turn(-90)
    # öffnen des lagers
    go(-40)
    heber2.run_angle(300,165)
    go(60)
    heber2.run_angle(70,-60)
    go(80)
    heber2.run_angle(100,-20) 
 

def rein():
    heber.run_angle(100,-140)
    go(-50)
    heber2.run_angle(100,55)
    go(-200)


 

def wasser_holen(log_level=1):
    heber2.run_until_stalled(-800, duty_limit=50) 
    heber.run_until_stalled(-800, duty_limit=50)

    fahre_zum_wasserturm() 
    fahre_vom_wasserturm_zum_lager() 
    rein()




def gehe_vom_wasserturm_zu_den_proben(log_level=3):
    """
        steht vor dem Wasserlager auf der w. Linie
    """ 
 
    robot.settings(300,300,100,100)
    turn(-90)
    wall(200)
    go(50)
    turn(-90) 
    go(300)
    fahre_bis_zur_farbkombi(stoppe_bei_farbmuster=farb_parameter["wr"],max_gefahrene_distanz=500, log_level=3) 
    robot.settings(200,200,100,100)
    go(180)
    turn(90)
    wall(100)
    heber2.run_until_stalled(-400,duty_limit=50)

def proben_holen_und_liefern():
    """
        steht bei der weißen Linie und bringt alle Proben ins rechte labor
    """
    wall(100)
    robot.reset()
    robot.settings(100,100,100,100)
    go(70)
    robot.arc(145,65)  
    robot.arc(-90,100) 
    #go(60)
    #robot.arc(145,75) 

    heading =hub.imu.heading()
    heading_turn = 90 -  heading  

    # h1 ist oben 
    

    robot.settings(200,200,100,100)
    #turn(heading_turn)
    print(f"{heading=} {heading_turn=}")
    go(500)
    heber2.run_until_stalled(-500,duty_limit=50)
    heber2.run_angle(400,150)
    get_status()
    turn(-145)
    wall(400)
    go(200), 
    turn(90)
    robot.settings(400,400,200,200)
    go(200)
    fahre_bis_zur_farbkombi(stoppe_bei_farbmuster=farb_parameter["rb"],max_gefahrene_distanz=500, log_level=3) 
    go(40)
    folge_linie(stoppe_bei_farbmuster=farb_parameter["br"],max_v=200, max_gefahrene_distanz=220, algo_bis_distanz=150) 
    go(60)
    heber2.run_angle(400,-100) 
    go(-600)
    turn(-90)
    wall(300)

 
def drohne():
    # ist gewallt rechts
    wall(100)
    robot.settings(500,500,300,300)
    heber.run_until_stalled(-400)
    go(150)
    turn(90)
    heber.run_angle(150,200,wait=False)
    go(-1150,then=Stop.COAST_SMART)
    heber.run_until_stalled(-400)
    go(50,then=Stop.COAST_SMART)
     

def rover():
    """
        drohne abgeliefert und steht vor der weiß-schwarzen Linie
    """
    fahre_bis_zur_farbkombi(stoppe_bei_farbmuster=farb_parameter["wr"],max_gefahrene_distanz=500, log_level=3)
    go(240)
    turn(-90)
    fahre_bis_zur_farbkombi(stoppe_bei_farbmuster=farb_parameter["wr"],max_gefahrene_distanz=500, log_level=3)
    heber.run_until_stalled(-400,duty_limit=50)
 
    heber.reset_angle(0)
    go(200)
    turn(-50)
    #heber2.run_angle(200,50)
    heber.run_angle(200,170) 
    turn(45,then=Stop.COAST_SMART)
    print("Rover Ende")
 
#: HAUPTPROGRAMM für den ersten Teil
def wro_25():
    wasser_holen(log_level=1) 
    log(f"vergangene Zeit: { main_watch.time()-start_ts}", log_level=3) 
    heber2.run_until_stalled(-800, duty_limit=50) 
    

    robot.settings(500,500,200,200)
    gehe_vom_wasserturm_zu_den_proben()
    log(f"vergangene Zeit: { main_watch.time()-start_ts}",log_level=3)
    proben_holen_und_liefern()
    
    drohne()
    log(f"drohne vergangene Zeit: { main_watch.time()-start_ts}",log_level=3) 
    heber2.run_until_stalled(-800, duty_limit=50) 
    heber.run_until_stalled(-800, duty_limit=50) 

    rover() 
    log(f"rover vergangene Zeit: { main_watch.time()-start_ts}",log_level=3) 

    # gehe vom Rover zum Ziel
    # steht links vom rover in 5° 
    get_status()
    robot.settings(500,600,400,400)
    go(100)
    turn(95) 
    go(600)
    turn(90) 
    go(120)
    turn(-90)
    folge_linie(stoppe_bei_farbmuster=farb_parameter["br"],max_v=200, max_gefahrene_distanz=220, algo_bis_distanz=100) 
    turn(180)
    robot.settings(200,200,200,200)
    go(-900) 

    log(f"vergangene Zeit: { main_watch.time()-start_ts}",log_level=3) 

if __name__ == "__main__":
   
    main_watch=StopWatch()
    start_ts=main_watch.time() 

    #test_boden_farben()
    #test_proben_farben()
    wro_25() 
    #interactive() 
   