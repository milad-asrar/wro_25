 

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

farb_list=[{Color.GREEN: 123}, {Color.WHITE: 129}, {Color.WHITE: 134}, {Color.WHITE: 140}, {Color.WHITE: 146}, {Color.WHITE: 152}, {Color.WHITE: 158}, 
           {Color.NONE: 165}, {Color.NONE: 171}, {Color.NONE: 178}, {Color.NONE: 185}, {Color.NONE: 192}, {Color.NONE: 198}, 
           {Color.RED: 204}, {Color.RED: 211}, {Color.RED: 217}, {Color.RED: 224}, {Color.RED: 231}, {Color.RED: 237}, {Color.RED: 244}, {Color.RED: 252}, {Color.RED: 260}, {Color.RED: 268}, 
           {Color.NONE: 276}, {Color.NONE: 284}, {Color.NONE: 291}, {Color.NONE: 300}, {Color.NONE: 308}, 
           {Color.GREEN: 316}, {Color.GREEN: 324}, {Color.GREEN: 334}, {Color.GREEN: 342}, {Color.GREEN: 350}, {Color.GREEN: 358},
           {Color.NONE: 366}, {Color.NONE: 375}, {Color.NONE: 383}, {Color.NONE: 392}, {Color.NONE: 402}, {Color.NONE: 412}, {Color.NONE: 421}, 
           {Color.NONE: 431}, {Color.NONE: 440}, {Color.NONE: 450}, {Color.NONE: 461}, {Color.NONE: 470}, {Color.NONE: 480}, {Color.NONE: 489}, {Color.NONE: 498}, 
           {Color.YELLOW: 506}, {Color.YELLOW: 515}, {Color.YELLOW: 524}, {Color.YELLOW: 533}, {Color.YELLOW: 542}, {Color.YELLOW: 552}, 
           {Color.NONE: 562}, {Color.NONE: 572}, {Color.NONE: 584}, {Color.NONE: 593}, {Color.NONE: 602}]

old_color = ''
gesehene_farben:list=[]
pos = 0*4

for d in farb_list[0:20]:
    gesehene_farben.append(d)
    k = list(d.keys())[0]
    v = list(d.values())[0]
    if v>0:
        gesehene_farben.append(k)
    print(k,v)

print(gesehene_farben.count(Color.WHITE))
print(gesehene_farben.count(Color.GREEN))
print(gesehene_farben.count(Color.YELLOW))
print(gesehene_farben.count(Color.RED))

# eine Liste: wie oft wurde die Farbe gesehen
farbe_dict_sortiert = sorted(farb_list, key=farb_list.get, reverse=True) 
aktuelle_farbe = farbe_dict_sortiert[0]  

farb_list.count({"Color.WHITE":3})