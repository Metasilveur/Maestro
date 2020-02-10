import pygame
from pygame.locals import *
from mido import MidiFile
from mido import MetaMessage
from mido import Message, MidiTrack
import pygame.midi
import pygame as pg
from pygame import gfxdraw

import serial

arduino = serial.Serial('COM9', 9600, timeout=.1)

pygame.init()
fenetre = pygame.display.set_mode((1470, 750), DOUBLEBUF)

continuer = 1

class Test():
    def __init__(self, touche, time_pos, time, posx=0, posy=0):
        self.touche = touche
        self.time_pos = time_pos
        self.time = time
        self.posy = posy
        self.posx = posx
            
File = open("TEST.txt","r")

partition = []

for line in File:
    Split = line.split(" ")
    partition.append(Test(int(Split[0]),int(Split[1]),int(Split[2]),Split[3],int(Split[4])))

taille = len(partition)

Limite = 596
    
Compteur = 0

clock = pygame.time.Clock()

nombre = ' '

while continuer:
    
    dt = clock.tick(161)
    
    Compteur += 1
    
    for event in pygame.event.get():  
        if event.type == QUIT:     
            continuer = 0
        if event.type == KEYDOWN:
            if event.key == K_r:
                nombre = '5'
                arduino.write(nombre.encode('ascii'))
                
    for i in range(taille):
        if Compteur > partition[i].time_pos:
            partition[i].posy += 1
        if partition[i].posy+partition[i].time == Limite:
            print("Allumer : %d " % (partition[i].touche))
            nombre = str(partition[i].touche-40)
            print(nombre)
            arduino.write(nombre.encode('ascii'))
            pygame.time.wait(15)
            
        elif partition[i].posy == Limite:
            print("Eteindre : %d " % (partition[i].touche))
            nombre = str(partition[i].touche-40)
            print(nombre)
            arduino.write(nombre.encode('ascii')) 
            pygame.time.wait(15)
            
    
    pygame.display.flip()
    
pygame.display.quit()
File.close()
            
print("Terminé")
        

    