# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 15:12:45 2022

@author: gauth
"""
from math import*

def WindVector(X,Y,X1,Y1):
    #--gestion des symétries pour atteindre chaque cadrans du système d'axe--#
    signX, signY = 1, 1
    if X1 < 0: 
        signX = -1
    if Y1 > 0:
        signY = -1
    X1 = abs(X1)   
    Y1 = abs(Y1)    
    Y0 = Y
    Rvct_list = [(X,Y)] 
    m = (Y1-Y)/(X1-X + 1/1000)          #ajout d'une petite variable afin d'éviter la division par 0
    print("la pente (m) est égal à :", m)
    if m <= 1:
        for k in range(1, round(X1) + 1):
            X = X + 1
            Y = Y0  + k*m
            Rvct_list += [(signX*X,signY*floor(Y))]
    if m > 1:
        for k in range(1, round(Y1) + 1):
            X = X + 1/m
            Y = Y + 1
            Rvct_list += [(signX*floor(X),signY*Y)]
    return(Rvct_list)

###---Fonction permetant de définir la coordonée du "bout" du vecteur---###
def Angle2Vector(angle, speed):
    y = speed*cos(radians(angle))
    print("y est égal à :", y)
    x = sqrt(speed**2-y**2)
    print("x est égal à :", x)
    #return(WindVector(1, 1, x+1, y+1))
    #return(WindVector(1, 1, x, y))
    return(WindVector(0, 0, x, y))
    