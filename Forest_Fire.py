"""
Created on Thu Oct 13 13:01:25 2022

@author: Gauthier Guyaz, Lycée Blaise-Cendrars, 3H

Github : https://github.com/Gauthier23
"""

from tkinter import*

###---Fonction dessinant la matrice---###
def dam():
    x, y, i = 0, 0, 0
    while x < side and y < side:    #tant qu'on a pas atteinds la dernière cellule en bas à droite
        can.create_rectangle(x, y, x + c, y + c, outline = "black", fill="")  #fill = "" ==> transparent
        dico[x/c,y/c]=0         
        x += c
        i += 1
        if i == side/c:             #quand "i" est égal à la longueur alors, on fait la ligne du dessous
            y += c
            x, i = 0, 0             #variables à zero pour recommancer la ligne
    
###---Fonction---###
def click_gauche(event):
    global dico
    x = event.x -(event.x%c)
    y = event.y -(event.y%c)
    if dico[x/c,y/c] == 1 or dico[x/c,y/c] == 2:
        can.create_rectangle(x, y, x + c, y + c, outline = "black", fill=backgroud_color)
        dico[x/c,y/c] = 0
    elif dico[x/c,y/c] == 0:   
        can.create_rectangle(x, y, x+c, y+c, fill='darkgreen')
        dico[x/c,y/c] = 1
    
###---Fonction---###    
def click_droit(event): 
    x = event.x -(event.x%c)
    y = event.y -(event.y%c)
    can.create_rectangle(x, y, x+c, y+c, fill ='red')
    dico[x/c,y/c]=2    
            
          
###---Fonction---###

def calcul_proxi(x,y):                #coordonnés de la cellule (X,Y) comme entrée 
    proxi = None                  
    
    if dico.get((x-1, y), 0) == 2:        
        proxi = "feu"
        
    if dico.get((x, y-1), 0) == 2:       
        proxi = "feu"
        
    if dico.get((x, y+1), 0) == 2:        
        proxi = "feu"
              
    if dico.get((x+1, y), 0) == 2:        
        proxi = "feu"
        
    return proxi               

###---Fonction ... selon les indications de la liste temporaire---###
def draw():
    global temp
    can.delete(ALL)                     #on supprime tout l'ancien Canvas
    dam()                               #recréation via fonction de la matrice neutre
    for y in range(0, int(side/c)):     #on parcours chaque coordonné Y
        for x in range(0, int(side/c)): #puis chaque X selon le Y
            if temp[x,y] == 1:          
                can.create_rectangle(c*x, c*y, c*x + c, c*y + c, fill="darkgreen")  
            elif temp[x,y] == 2:
                can.create_rectangle(c*x, c*y, c*x + c, c*y + c, fill="red")  
            elif temp[x,y] == 3: 
                can.create_rectangle(c*x, c*y, c*x + c, c*y + c, fill="grey") 
    dico.update(temp)                   #on remplace notre dictionnaire par le temporaire
    
def calculer():
    global temp
    temp.update(dico)
    for y in range(0, int(side/c)):     #on parcours chaque coordonné Y
        for x in range(0, int(side/c)): #puis chaque X selon le Y
            proxi = calcul_proxi(x,y) 
            
            if dico[x,y] == 1 and proxi == "feu": 
                temp[x,y] = 2 
            
            if dico[x,y] == 2:
                temp[x,y] = 3 
    draw()

###---Fonction gérant la répétition des générations selon le temps---###

def withtime():
    global flag
    flag = 1
    update_calculs()
        
def update_calculs():
    calculer()
    if flag == 1:
            fen.after(500, update_calculs)
        
def stop():
    global flag
    flag = 0
    
#####-----Variables et Constantes-----#####
c = 20                              #nombre de pixel pour le côté d'une cellule
side = 600                          #taille du côté du canvas carré dans lequel l'automate se développe
dico = {}                           #dictionaire principal contenant comme clé la position (x,y) et comme valeur son état (0 ou 1)
temp = {}                           #idem mais temporaire afin de gérer la transition vers un nouveau dictionaire principal
backgroud_color = "#FFFFFF"         #couleur de fond du canvas principal "#D4E6F1"

# None
# vert = 1
# rouge = 2
# cendre = 3

#####-----Gestionnaire du graphisme Tkinter-----#####    
  
fen = Tk()
fen.title('SIMULATION WINDOW')
Title = Label(text ='Forest Fire',font = ("Helvetica", 10))
Title.pack(padx=7, pady=12)
can = Canvas(fen, width = side, heigh = side, bg = backgroud_color) 
b1 = Button(fen, text='Lancer une étape', command=calculer )
can.pack(side=TOP, padx=20, pady=10)
b1.pack(side = LEFT, padx=5, pady=5)
can.bind("<Button-1>", click_gauche)
can.bind("<Button-3>", click_droit)
b2 = Button(fen, text='Lancer', command = withtime )
b3 = Button(fen, text='Stop', command = stop)
b2.pack(side = LEFT, padx=5, pady=5)
b3.pack(side = LEFT, padx=5, pady=5)

#####-----Préparation interface de base-----#####
dam()
fen.mainloop()
