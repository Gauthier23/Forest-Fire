# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 16:17:57 2023

@author: Gauthier Guyaz
"""

import tkinter as tk        #gestion graphismes
from random import randint  #germe aléatoire
import WindVector           #importation d'un fichier annexe 
from PIL import Image       #gestion du raster


# =============================================================================
#             I PARTIE, VARIABLES ET CONSTANTES GLOBALES
# =============================================================================

SIDE = 600                     #taille du côté de la grille (entre 500-650)
CELL = 4                       #taille du côté d'une cellule
BACKGROUND_COLOR = "#FFFFFF"   #couleur de fond du canvas principal
dico = {}                      #dictionaire principal: clé = position (x,y), valeur = état (1,2,3)
temp = {}                      #idem mais temporaire (relai du dico pour génération n+1)
gen_count = 0

#-les états (alphabet) de l'automate-#
# Reste du biome = 0  ==> None
# arbre = 1           ==> vert
# feu = 2             ==> rouge
# cendre = 3          ==> gris


# =============================================================================
#               II PARTIE, GESTION GENERALE DE L'AUTOMATE
# =============================================================================

###---Fonction dessinant la matrice---###
    
def dam():
    #-double boucle parcourant chaque cellule du canvas-#
    for y in range(0, SIDE, CELL):
        for x in range(0, SIDE, CELL):
            #-création d'une cellule associée à une position-#
            can.create_rectangle(x, y, x + CELL, y + CELL, outline="black", fill="")
            #-initialisation de la cellule à 0 dans le dictionnaire-#
            dico[int(x/CELL), int(y/CELL)] = 0 
    
###---Fonction modifiant l'état de la cellule cliquée---###

def click_gauche(event):
    global dico
    x = event.x -(event.x%CELL)     #prise de coordonnée x par la soustraction du modulo
    y = event.y -(event.y%CELL)     #prise de coordonnée y par la soustraction du modulo
    #-si la cellule a déjà un état, annihilation et dico à 0-#
    if dico[x/CELL,y/CELL] == 1 or dico[x/CELL,y/CELL] == 2:
        can.create_rectangle(x, y, x + CELL, y + CELL, outline = "black", fill=BACKGROUND_COLOR)
        dico[int(x/CELL),int(y/CELL)] = 0
    #-si la cellule n'a pas d'état, création d'une case verte et dico à 1-#
    elif dico[x/CELL,y/CELL] == 0:
        can.create_rectangle(x, y, x+CELL, y+CELL, fill='darkgreen')
        dico[int(x/CELL),int(y/CELL)] = 1
  
    
###---Fonction mettant le feu à la cellule cliquée---###    

def click_droit(event): 
    x = event.x -(event.x%CELL)     #prise de coordonnée x par la soustraction du modulo
    y = event.y -(event.y%CELL)     #prise de coordonnée x par la soustraction du modulo
    #-création d'une case rouge et dico à 2-#
    can.create_rectangle(x, y, x+CELL, y+CELL, fill ='red')
    dico[int(x/CELL),int(y/CELL)]=2           


###---Fonction remplissant les carrés selon la liste temporaire---###

def draw():
    can.delete(tk.ALL)  # supression de l'ancien Canvas
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
            
        can.create_rectangle(CELL * x, CELL * y, CELL * x + CELL, CELL * y + CELL, fill=fill) 
    #-remplacement du dictionnaire par le temporaire (relais)-#   
    dico.update(temp)  
    
      
###---Fonction calculant les cellules touchées par le feu---###    

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
#               III PARTIE, MODULES D'INTERACTION UTILISATEUR
# =============================================================================

###---Fonctions gérant la répétition des générations selon le temps---###

def withtime():
    global flag
    flag = 1
    update_calculs()
        
def update_calculs():
    calculer()
    if flag == 1:
            fen.after(200, update_calculs)
        
def stop():
    global flag
    flag = 0


###---Fonction permettant de recommencer un nouveau germe---###

def reset():
    global temp, gen_count
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
    #-boucles parcourant chaque cellule-#
    for x in range(0, SIDE//CELL):
        for y in range(0, SIDE//CELL):
            #-si les probabilité appartiennent à notre pourcentage-#
            if randint(1,100) <= propo:
                #-ajout d'un arbre-#
                dicoPropo[x,y] = 1
    temp.update(dicoPropo)
    draw()    
    
    
###---Ajout de la MAP raster---###

def mapLidar():
    global temp
    temp.update(dicoLAS)
    draw()    
    
    
###---Importation du raster---###    

img = Image.open("OGGIOMVP.png")

(width,height) = img.size

#-dictionnaire vide pour stocker les infos de l'image-#
dicoLAS = {} 

#-boucles pour parcourir tous les pixels de l'image-#
for x in range(0, width):
    for y in range(0, height):
        
        #-récupération de la valeur du pixel à la position (x, y)-#
        pixel = img.getpixel((x, y)) 
        
        #-si la valeur du pixel est égale à 31 (arbre)-#
        if pixel == 31:       
            #-ajout de la position (x, y) dans le dicoLAS avec la valeur 1-#
            dicoLAS[x,y] = 1
        
# ATTENTION, pour utiliser un fichier lidar dis "rasterisé" disponible, mettre SIDE = 600 et CELL = 4

# =============================================================================
#            IV PARTIE, GESTIONNAIRE GRAPHISME AVEC TKINTER    
# =============================================================================

fen = tk.Tk()
fen.title('SIMULATION WINDOW')
fen.resizable(False, False)

###---Création du Frame contenant les boutons latéraux---###

frame2 = tk.Frame(fen)
frame2.pack(side = tk.RIGHT, fill = "both",padx = 10, pady = 30)

#-Création des boutons-#
b1 = tk.Button(frame2, text='next gen', command= calculer )
b2 = tk.Button(frame2, text='start', command = withtime )
b3 = tk.Button(frame2, text='stop', command = stop)
b6 = tk.Button(frame2, text='reset', command = reset)
b7 = tk.Button(frame2, text='quit', command = destroy)

#-Empilement boutons-#
b1.pack(side = tk.TOP, padx=5, pady=5)
b2.pack(side = tk.TOP, padx=5, pady=5)
b3.pack(side = tk.TOP, padx=5, pady=5)
b6.pack(side = tk.TOP, padx=5, pady=5)
b7.pack(side = tk.TOP, padx=5, pady=5)

###---Création du "sous-frame" contenant le gestionnaire du vent---###

frame2_1 = tk.Frame(frame2, borderwidth=2, relief=tk.GROOVE)
frame2_1.pack(side = tk.TOP, fill = "both", pady = 7)

#-Labels informatifs pour les curseurs-#
wind = tk.Label(frame2_1, text = "WIND")
speed_angle = tk.Label(frame2_1, text = "speed" + " "*10 + "angle")   

wind.pack(side = tk.TOP, padx = 5)
speed_angle.pack(side = tk.TOP)

#-Curseurs-#
curseur_speed = tk.Scale(frame2_1, from_=0, to=30, orient=tk.VERTICAL, length=330, width=15, sliderlength=20)
curseur_angle = tk.Scale(frame2_1, from_=0, to=360, orient=tk.VERTICAL, length=330, width=15, sliderlength=20)
curseur_speed.pack(side = tk.LEFT)
curseur_angle.pack(side = tk.RIGHT)

###---Création du Frame contenant le canvas et les informations sur la simulation---###

frame = tk.Frame(fen)
frame.pack(fill="both", padx = 5)

#-Titre simulation-#
Title = tk.Label(frame, text ='Forest Fire',font = ("Helvetica", 12))
Title.pack(padx=7, pady=5)

#-Création du canvas principal (simulation)-#
can = tk.Canvas(frame, width = SIDE, heigh = SIDE, bg = BACKGROUND_COLOR) 
can.pack(side=tk.TOP, padx=10, pady=0)
can.bind("<Button-1>", click_gauche)
can.bind("<Button-3>", click_droit)

#-Création des boutons permettant de générer des germes-#
b4 = tk.Button(frame, text='input Lidar file', command = mapLidar) 
b5 = tk.Button(frame, text='input propo', command = alea) 
b4.pack(side = tk.LEFT, padx=5, pady=5)
b5.pack(side = tk.LEFT, padx=5, pady=5)

#-Curseur pour gérer la proportion du germe aléatoire-#
curseur_propo = tk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL, length=200, width=20, sliderlength=20, tickinterval=25)
curseur_propo.set(50)
curseur_propo.pack(side = tk.LEFT)

#-Affichage du nombre de génération-#
generationtxt = tk.Label(frame, text= "Generation :")
generationtxt.pack(side = tk.LEFT, padx = 20)

gen = tk.IntVar()
generation = tk.Label(frame, textvariable = gen )
generation.pack(side = tk.LEFT)


#####-----Préparation interface de base et boucle générale-----#####

dam()
fen.mainloop()
