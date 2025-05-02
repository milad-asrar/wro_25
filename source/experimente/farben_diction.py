# %%
class c:
    GREEN ="g"
    WHITE ="w"
    RED="r"
    YELLOW="y"
    NONE='n'

Color=c

# W: 158 -129  29
# N: 198 -165  33
# R  268 -204  64
# N  308 - 276 28
# G  358 -316  42
# Y  552 -506  46
# N  602 562   40

farb_list_gynwnr = [
    {134: Color.NONE},
    {138: Color.NONE},
    {143: Color.NONE},
    {149: Color.GREEN},
    {154: Color.GREEN},
    {159: Color.GREEN},
    {165: Color.GREEN},
    {171: Color.GREEN},
    {176: Color.GREEN},
    {182: Color.GREEN},
    {188: Color.NONE},
    {195: Color.NONE},
    {202: Color.NONE},
    {208: Color.NONE},
    {215: Color.YELLOW},
    {221: Color.YELLOW},
    {227: Color.YELLOW},
    {233: Color.YELLOW},
    {240: Color.YELLOW},
    {246: Color.YELLOW},
    {252: Color.YELLOW},
    {259: Color.YELLOW},
    {265: Color.YELLOW},
    {271: Color.YELLOW},
    {279: Color.YELLOW},
    {285: Color.NONE},
    {290: Color.NONE},
    {297: Color.NONE},
    {302: Color.NONE},
    {307: Color.NONE},
    {314: Color.NONE},
    {320: Color.NONE},
    {327: Color.NONE},
    {333: Color.NONE},
    {340: Color.NONE},
    {347: Color.NONE},
    {353: Color.NONE},
    {359: Color.NONE},
    {365: Color.NONE},
    {371: Color.NONE},
    {377: Color.NONE},
    {383: Color.NONE},
    {389: Color.NONE},
    {397: Color.NONE},
    {404: Color.NONE},
    {411: Color.NONE},
    {417: Color.NONE},
    {422: Color.WHITE},
    {429: Color.WHITE},
    {434: Color.WHITE},
    {440: Color.WHITE},
    {446: Color.WHITE},
    {452: Color.WHITE},
    {458: Color.WHITE},
    {464: Color.WHITE},
    {471: Color.NONE},
    {478: Color.NONE},
    {484: Color.NONE},
    {491: Color.NONE},
    {497: Color.NONE},
    {503: Color.NONE},
    {509: Color.NONE},
    {516: Color.NONE},
    {522: Color.NONE},
    {528: Color.NONE},
    {534: Color.NONE},
    {541: Color.NONE},
    {548: Color.NONE},
    {554: Color.NONE},
    {560: Color.NONE},
    {567: Color.NONE},
    {573: Color.NONE},
    {578: Color.NONE},
    {584: Color.NONE},
    {590: Color.NONE},
    {596: Color.NONE},
    {602: Color.NONE},
    {608: Color.NONE},
    {615: Color.NONE},
    {621: Color.NONE},
    {629: Color.RED},
    {635: Color.RED},
    {641: Color.RED},
    {647: Color.RED},
    {653: Color.NONE},
]

farb_list_nygwrn = [
    {133: Color.NONE},
    {139: Color.NONE},
    {144: Color.NONE},
    {150: Color.NONE},
    {156: Color.NONE},
    {161: Color.NONE},
    {167: Color.NONE},
    {172: Color.NONE},
    {179: Color.NONE},
    {185: Color.NONE},
    {191: Color.NONE},
    {197: Color.NONE},
    {203: Color.NONE},
    {209: Color.NONE},
    {216: Color.NONE},
    {222: Color.YELLOW},
    {229: Color.YELLOW},
    {235: Color.YELLOW},
    {242: Color.YELLOW},
    {249: Color.YELLOW},
    {255: Color.YELLOW},
    {261: Color.YELLOW},
    {268: Color.YELLOW},
    {274: Color.YELLOW},
    {279: Color.YELLOW},
    {286: Color.NONE},
    {293: Color.NONE},
    {299: Color.NONE},
    {306: Color.NONE},
    {313: Color.NONE},
    {318: Color.NONE},
    {325: Color.GREEN},
    {330: Color.GREEN},
    {336: Color.GREEN},
    {342: Color.GREEN},
    {348: Color.GREEN},
    {354: Color.GREEN},
    {360: Color.GREEN},
    {366: Color.GREEN},
    {374: Color.NONE},
    {380: Color.NONE},
    {387: Color.NONE},
    {393: Color.NONE},
    {400: Color.NONE},
    {405: Color.NONE},
    {412: Color.NONE},
    {418: Color.NONE},
    {424: Color.WHITE},
    {431: Color.WHITE},
    {437: Color.WHITE},
    {443: Color.WHITE},
    {450: Color.WHITE},
    {456: Color.WHITE},
    {462: Color.WHITE},
    {469: Color.NONE},
    {475: Color.NONE},
    {481: Color.NONE},
    {486: Color.NONE},
    {493: Color.NONE},
    {499: Color.NONE},
    {505: Color.NONE},
    {512: Color.NONE},
    {518: Color.NONE},
    {525: Color.NONE},
    {532: Color.RED},
    {538: Color.RED},
    {544: Color.RED},
    {550: Color.RED},
    {556: Color.RED},
    {562: Color.NONE},
    {569: Color.NONE},
    {575: Color.NONE},
    {582: Color.NONE},
    {590: Color.NONE},
    {595: Color.NONE},
    {602: Color.NONE},
    {608: Color.NONE},
    {614: Color.NONE},
    {621: Color.NONE},
    {626: Color.NONE},
    {632: Color.NONE},
    {639: Color.NONE},
    {645: Color.NONE},
    {652: Color.NONE},
]

# %%
farben_gesehen:list=[]
old_color =-2
gesehene_farben:list=[]
pos = 0*4
farbe_start=0
farbe_end = 0
farb_list=farb_list_gynwnr
#farb_list=farb_list_nygwrn
for i in range(len(farb_list)): 
    d=farb_list[i]
    distance= list(d.keys())[0]
    aktuelle_farbe = list(d.values())[0]
    if old_color != aktuelle_farbe:
        farbe_end=distance
        farbe_gesehen_distanz = farbe_end-farbe_start
        print(f"{old_color}, {farbe_start}, {farbe_end} {farbe_gesehen_distanz=}")
       
        if farbe_gesehen_distanz>20 and old_color!=-2:
            farben_gesehen.append([old_color,farbe_start,farbe_end,farbe_gesehen_distanz])
        old_color=aktuelle_farbe
        farbe_start=distance

print(f"{old_color}, {farbe_start}, {farbe_end} {farbe_gesehen_distanz=}") 

print(farben_gesehen)
# %%
for i in range(len(farben_gesehen)):
    min, max = farben_gesehen[i][1:3] 
    if i ==0:
        mitte_erste_farbe = min + farben_gesehen[i][3] /2
        min_scan_bereich =mitte_erste_farbe-10
        max_scan_bereich =mitte_erste_farbe+10
        print(farben_gesehen[i][0])
    min_scan_bereich = min_scan_bereich + 100*i 
    max_scan_bereich = max_scan_bereich + 100*i 
    print(f"{min_scan_bereich=}, {max_scan_bereich} ")
    
      
        
        if min>= min_scan_bereich and max <=max_scan_bereich:
            print(farben_gesehen[i][0])
            
        
            print(farben_gesehen[i][0])
        
        
print(mitte_erste_farbe)

# %%

# print(aktuelle_farbe,distance)

print(gesehene_farben.count(Color.WHITE))
print(gesehene_farben.count(Color.GREEN))
print(gesehene_farben.count(Color.YELLOW))
print(gesehene_farben.count(Color.RED))
print(gesehene_farben.count(Color.NONE))
# %%

# eine Liste: wie oft wurde die Farbe gesehen
farbe_dict_sortiert = sorted(farb_list, key=farb_list.get, reverse=True) 
aktuelle_farbe = farbe_dict_sortiert[0]  

farb_list.count({"Color.WHITE":3})
# %%
