# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 16:17:57 2023

@author: Gauthier Guyaz
"""


from tkinter import*
from math import*
from random import*


# =============================================================================
#               I PARTIE, GESTION GENERALE DE L'AUTOMATE
# =============================================================================

###---Fonction dessinant la matrice---###
    
def dam():
    #-double boucle parcourant chaque cellule du canvas-#
    for y in range(0, side, cell):
        for x in range(0, side, cell):
            #-création d'une cellule associée à une position-#
            can.create_rectangle(x, y, x + cell, y + cell, outline="black", fill="")
            #-initialisation de la cellule à 0 dans le dictionnaire-#
            dico[x/cell, y/cell] = 0 
   
    
###---Fonction modifiant l'état de la cellule cliquée---###

def click_gauche(event):
    global dico
    x = event.x -(event.x%cell)     #prise de coordonnée x par la soustraction du modulo
    y = event.y -(event.y%cell)     #prise de coordonnée y par la soustraction du modulo
    #-si la cellule a déjà un état, annihilation et dico à 0-#
    if dico[x/cell,y/cell] == 1 or dico[x/cell,y/cell] == 2:
        can.create_rectangle(x, y, x + cell, y + cell, outline = "black", fill=backgroud_color)
        dico[x/cell,y/cell] = 0
    #-si la cellule n'a pas d'état, création d'une case verte et dico à 1-#
    elif dico[x/cell,y/cell] == 0:
        can.create_rectangle(x, y, x+cell, y+cell, fill='darkgreen')
        dico[x/cell,y/cell] = 1
  
    
###---Fonction mettant le feu à la cellule cliquée---###    

def click_droit(event): 
    x = event.x -(event.x%cell)     #prise de coordonnée x par la soustraction du modulo
    y = event.y -(event.y%cell)     #prise de coordonnée x par la soustraction du modulo
    #-création d'une case rouge et dico à 2-#
    can.create_rectangle(x, y, x+cell, y+cell, fill ='red')
    dico[x/cell,y/cell]=2           


###---Fonction remplissant les carrés selon la liste temporaire---###

def draw():
    can.delete(ALL)  # supression de l'ancien Canvas
    dam()            # recréation via fonction de la matrice neutre
    
    #-parcours des coordonnées dans le dictionnaire temp-#
    for x, y in temp:
        fill = ""   #remplissage vide par défaut
        #-forêt-#
        if temp[x, y] == 1:   
            fill = "darkgreen"
        #-feu-#    
        elif temp[x, y] == 2: 
            fill = "red"
        #-cendre-#    
        elif temp[x, y] == 3: 
            fill = "grey"
            
        can.create_rectangle(cell * x, cell * y, cell * x + cell, cell * y + cell, fill=fill) 
    #-remplacement du dictionnaire par le temporaire (relais)-#   
    dico.update(temp)  
    
      
###---Fonction calculant les cellules touchées par le feu---###    

import WindVector  #importation d'un fichier annexe 

def calculer():
    global temp, gen_count
    
    #-Rasterisation d'un vecteur à partir de l'angle et de la vitesse par la fonction Angle2Vector -#
    wind_coord = WindVector.Angle2Vector(curseur_angle.get(), curseur_speed.get())
    
    #-remplacement du dictionnaire temporaire par le principal (relais)-#
    temp.update(dico)
    
    #-liste des cellules limitrophes directes-#
    neighbors = [(-1, 0), (0, -1), (0, +1), (+1, 0)]
    
    #-parcours des coordonnées dans le dictionnaire principal-#
    for x, y in dico:
        if dico[x, y] == 2: # cellule en feu
            temp[x, y] = 3  # devient en cendre
            
            #-analyse du premier voisinage (limitrophe direct)-#
            for coord in neighbors:
                #-si une cellule limitrophe est verte, elle brûle-#
                if dico.get((x + coord[0], y + coord[1]), 0) == 1:
                    temp[x + coord[0], y + coord[1]] = 2
                    
                    
            #-analyse du second voisinage (vent)-#
            for coord in wind_coord:
                #-si une cellule verte est touchée par cette liste, elle brûle-#
                if dico.get((x + coord[0], y + coord[1]), 0) == 1:
                    temp[x + coord[0], y + coord[1]] = 2
     
    #-gestion du comptage des générations-#    
    gen_count += 1      
    gen.set(gen_count)
    
    draw()  #dessin de la nouvelle génération
    
    

# =============================================================================
#               II PARTIE, MODULES D'INTERACTION UTILISATEUR
# =============================================================================

###---Fonctions gérant la répétition des générations selon le temps---###

def withtime():
    global flag
    flag = 1
    update_calculs()
        
def update_calculs():
    calculer()
    if flag == 1:
            fen.after(100, update_calculs)
        
def stop():
    global flag
    flag = 0


###---Fonction permettant de recommencer un nouveau germe---###

def reset():
    global temp, dico, gen_count
    gen_count = 0
    gen.set(gen_count)
    temp = {}
    draw()
    
    
###---Fonction permettant de quitter la fenêtre---###
    
def destroy():
    fen.destroy()     
    
###---Fonction permettant de créer un germe aléatoire---###
def alea():
    propo = curseur_propo.get()
    dicoPropo = {}
    for x in range(0, side//cell):
        for y in range(0, side//cell):
            r = randint(1,100)
            if r <= propo:
                dicoPropo[x,y] = 1
    temp.update(dicoPropo)
    draw()    
    
    
###---Ajout de la MAP raster---###

def MapLidar():
    global temp
    temp.update(dico)
    temp.update(dicoLAS)
    draw()    
    
    
###---Importation du raster---###    

from PIL.Image import*

i = open("image.png")

(width,height) = i.size     
dicoLAS = {}

for x in range(0, width):
    for y in range(0, height):
        c = Image.getpixel(i, (x, y)) 
        if c == 42:     
            dicoLAS[x,y] = 1


# =============================================================================
#             III PARTIE, VARIABLES ET CONSTANTES GLOBALES
# =============================================================================

side = 500                         #taille du côté du canvas carré dans lequel l'automate se développe (entre 500-650)
cell = 5                           #nombre de pixel pour le côté d'une cellule
dico = {}                          #dictionaire principal contenant comme clé la position (x,y) et comme valeur son état (1,2,3)
temp = {}                          #idem mais temporaire afin de gérer la transition vers un nouveau dictionaire principal
backgroud_color = "#FFFFFF"        #couleur de fond du canvas principal (#D4E6F1)
gen_count = 0
# Reste du biome  = 0  ==> None
# arbre = 1            ==> vert
# feu = 2              ==> rouge
# cendre = 3           ==> gris

# =============================================================================
#            IV PARTIE, GESTIONNAIRE GRAPHISME AVEC TKINTER    
# =============================================================================

fen = Tk()
fen.title('SIMULATION WINDOW')
fen.resizable(False, False)

###---Création du Frame contenant les boutons latéraux---###

frame2 = Frame(fen)
frame2.pack(side = RIGHT, fill = "both",padx = 10, pady = 30)

#-Création des boutons-#
b1 = Button(frame2, text='next gen', command= calculer )
b2 = Button(frame2, text='start', command = withtime )
b3 = Button(frame2, text='stop', command = stop)
b6 = Button(frame2, text='reset', command = reset)
b7 = Button(frame2, text='quit', command = destroy)

#-Empilement boutons-#
b1.pack(side = TOP, padx=5, pady=5)
b2.pack(side = TOP, padx=5, pady=5)
b3.pack(side = TOP, padx=5, pady=5)
b6.pack(side = TOP, padx=5, pady=5)
b7.pack(side = TOP, padx=5, pady=5)

###---Création du "sous-frame" contenant le gestionnaire du vent---###

frame2_1 = Frame(frame2, borderwidth=2, relief=GROOVE)
frame2_1.pack(side = TOP, fill = "both", pady = 7)

#-Labels informatifs pour les curseurs-#
wind = Label(frame2_1, text = "WIND")
speed_angle = Label(frame2_1, text = "speed" + " "*10 + "angle")   

wind.pack(side = TOP, padx = 5)
speed_angle.pack(side = TOP)

#-Curseurs-#
curseur_speed = Scale(frame2_1, from_=0, to=30, orient=VERTICAL, length=330, width=15, sliderlength=20)
curseur_angle = Scale(frame2_1, from_=0, to=360, orient=VERTICAL, length=330, width=15, sliderlength=20)
curseur_speed.pack(side = LEFT)
curseur_angle.pack(side = RIGHT)

###---Création du Frame contenant le canvas et les informations sur la simulation---###

frame = Frame(fen)
frame.pack(fill="both", padx = 5)

#-Titre simulation-#
Title = Label(frame, text ='Forest Fire',font = ("Helvetica", 12))
Title.pack(padx=7, pady=5)

#-Création du canvas principal (simulation)-#
can = Canvas(frame, width = side, heigh = side, bg = backgroud_color) 
can.pack(side=TOP, padx=10, pady=0)
can.bind("<Button-1>", click_gauche)
can.bind("<Button-3>", click_droit)

#-Création des boutons permettant de générer des germes-#
b4 = Button(frame, text='input Lidar file', command = MapLidar) 
b5 = Button(frame, text='input propo', command = alea) 
b4.pack(side = LEFT, padx=5, pady=5)
b5.pack(side = LEFT, padx=5, pady=5)

#-Curseur pour gérer la proportion du germe aléatoire-#
curseur_propo = Scale(frame, from_=0, to=100, orient=HORIZONTAL, length=200, width=20, sliderlength=20, tickinterval=25)
curseur_propo.set(50)
curseur_propo.pack(side = LEFT)

#-Affichage du nombre de génération-#
generationtxt = Label(frame, text= "Generation :")
generationtxt.pack(side = LEFT, padx = 20)

gen = IntVar()
generation = Label(frame, textvariable = gen )
generation.pack(side = LEFT)


#####-----Préparation interface de base-----#####

dam()
fen.mainloop()


