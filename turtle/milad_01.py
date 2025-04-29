#%%
import turtle
tip = turtle.Pen()
colors = ["red", "yellow", "blue", "green"]
tip.reset()
 

# Set the background color 
screen = turtle.Screen ( ) 
screen.bgcolor("skyblue") 

# Creating turtle object 
 
tip.color ("black") 
tip.speed (6)
tip.pensize(5)

#%%
#tip.reset()
def square(width,color,pensize):
    tip.color(color)
    tip.pensize(pensize)
    tip.forward(width)
    tip.right(90)
    tip.forward(width)
    tip.right(90)
    tip.forward(width)
    tip.right(90)
    tip.forward(width)
    tip.right(90)

#%%
def go(x,y):
    tip.penup() 
    tip.goto(x,y) 
    tip.pendown()


go(56,-97)
square(200,"purple",5)
go(50,-150)
square(200,"purple",5)

#%%

tip.forward(50)
tip.left(90)
tip.left(45)
tip.circle(20)

tip.color ("blue")
tip.color(colors[1])
#%%


def myprint(txt, count):
    for i in range(count):
        txt = txt.lower()
        print(txt)
 
myprint("HALLO",3)
#%%
mein_neue_variable=4
print(mein_neue_variable)
#%%
names = ["milad","alina","horia"]
type(names)

for name in names:
    print(name)
# %%
 
elf= {"torhueter":"neuer", "link_v":"kimmich", "rechts_v":"suele"}

elf["torhueter"]="donaruma"

elf["rechts_v"]

# %%
import turtle
colors="red","purple","blue","green","yellow","orange"
t=turtle.Pen()
turtle.bgcolor("black")
for x in range(360):
    t.pencolor(colors[x%6])
    t.width(x/100+1)
    t.forward(x)
    t.left(59)
    t.speed(0) 
#%%
import turtle
t = turtle.Pen
for x in range(100):
    t.forward(x)
    t.left(90)

# %%
ist_gruene_erdbeere=[0, 0, 0, 0, 0, 0] 
for i in range(5, 1, -1):
    if ist_gruene_erdbeere[i] ==1:
        print(f"wasserblock muss zur position {i}")

# %%
ist_gruene_erdbeere=[1,1,0,0,1,-1]
 
anzahl_erde = ist_gruene_erdbeere.count(0)
anzahl_gruene_erdbeeren = ist_gruene_erdbeere.count(1)
print (anzahl_erde, anzahl_gruene_erdbeeren )

if anzahl_erde  == 3:
    uebrigen_felder = anzahl_erde+anzahl_gruene_erdbeeren
    for i in range(uebrigen_felder,6):
        ist_gruene_erdbeere[i] = 1
if anzahl_gruene_erdbeeren  == 3:
    uebrigen_felder = anzahl_erde+anzahl_gruene_erdbeeren
    for i in range(uebrigen_felder,6):
        ist_gruene_erdbeere[i] = 0
 
print(ist_gruene_erdbeere)
# %%
