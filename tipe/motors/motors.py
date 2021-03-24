# -*- coding: utf-8 -*-

#THIS ONLY WORKS WITH PYTHON 2.7

import time
import datetime as dt
import nxt
import os
import csv
import nxt.usbsock
from nxt.motor import *
import pandas as pd


os.chdir(os.path.dirname(__file__))

b = nxt.locator.find_one_brick(debug=True)
print("Brick connected")

power = 20
gear_ratio = 3
m_right = Motor(b, PORT_C)
m_left = Motor(b, PORT_A)


day = dt.datetime.now()

def get_instruction(file_name):
    instructions = []
    #Instructions [type de rotation (z = azimuth, x = orientation), valeur de rotation] 
    #2 listes par indice pour les 2 positions
    with open(file_name, 'r') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            try:
                instructions.append([["x", float(row[1])],["z", float(row[2])]])
            except:
                pass
    
    return instructions

today = get_instruction("data/position_th/%s.csv" % str(day)[:10])


def get_init(L):
    #Coordonées dès que l'élevation est vers 0° (matin et soir)
    for i in range(len(L)-1):
        elevation = L[i][0][1]
        if elevation > 0:
            i_matin = i-1
            break
    
    for j in range(i_matin+1,len(L)-1):
        elevation = L[j][0][1]
        if elevation < 0:
            i_soir = j+1
            break

    print(i_matin,i_soir)
    return L[i_matin:i_soir]

today_instructions = get_init(today) # A definir avec fonction du dessus

def move_elevation(angle):
    global angle_adapt

    compen_angle = 1
    #Compensation pour l'élevation

    power = 20
    corr_angle = round(gear_ratio*angle)
    #print "elevation", corr_angle
    if corr_angle < 0:
        corr_angle = -corr_angle
        power = -power
    m_right.turn(power, corr_angle+compen_angle)

    position = ((m_right.get_tacho().__dict__["rotation_count"] + angle_adapt) / gear_ratio)
    print(corr_angle+compen_angle, m_right.get_tacho().__dict__["rotation_count"] + angle_adapt)
    angles_right.append(position)

def move_azimuth(angle):
    global angle_adapt
    power = 20
    corr_angle = round(gear_ratio*angle)
    #print "azimuth", corr_angle
    if corr_angle < 0:
        corr_angle = -corr_angle
        power = -power
    angle_adapt	= round(angle_adapt + corr_angle)
    m_left.turn(power, corr_angle)
    m_right.turn(-power, corr_angle)

    position = (m_left.get_tacho().__dict__["rotation_count"]) / gear_ratio
    #print(angle, position)
    angles_left.append(position)

#Etalonage de la position

e0,a0 = today_instructions[0][0][1],today_instructions[0][1][1]

angles_th_right = [e0]
angles_th_left = [a0]
angles_right = []
angles_left = []

angle_adapt = 0
#Correction de l'angle moteur droit à cause de la correction due à la rotation du moteur gauche

m_left.reset_position(relative=False)
m_right.reset_position(relative=False)

move_azimuth(a0)
move_elevation(e0)

#print(m_left.get_tacho().__dict__["rotation_count"])

Lt = [0]

time.sleep(1)

for i in range(1,len(today_instructions)-1):
    angle_azi = today_instructions[i][1][1]-today_instructions[i-1][1][1]
    angle_elev = today_instructions[i][0][1]-today_instructions[i-1][0][1]

    angles_th_right.append(today_instructions[i][0][1])
    angles_th_left.append(today_instructions[i][1][1])

    print(today_instructions[i][0][1])

    move_elevation(angle_elev)
    move_azimuth(angle_azi)
    
    Lt.append(i)

    time.sleep(1)

a_file_name = "data/position_exp/Azimuth{}.csv".format(str(day)[:10])
dfa = pd.DataFrame(list(zip(angles_th_left, angles_left)), columns =['Azimuth théorique','Rotation moteur gauche'])
dfa.to_csv(a_file_name)

e_file_name = "data/position_exp/Elevation{}.csv".format(str(day)[:10])
dfe = pd.DataFrame(list(zip(angles_th_right, angles_right)), columns =['Elevation théoriqe','Rotation moteur droit'])
dfe.to_csv(e_file_name)

m_right.idle()
m_left.idle()
