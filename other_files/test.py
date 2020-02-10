import pygame
from pygame.locals import *

'''
from midiutil import MIDIFile

degrees  = [60, 62, 64, 65, 67, 69, 71, 72] # MIDI note number
track    = 0
channel  = 0
time     = 0   # In beats
duration = 1   # In beats
tempo    = 60  # In BPM
volume   = 100 # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                     # automatically created)
MyMIDI.addTempo(track,time, tempo)

for pitch in degrees:
    MyMIDI.addNote(track, channel, pitch, time, duration, volume)
    time = time + 1

with open("major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
'''

pygame.init()
#Initialisation de la bibliothéques Pygame

fenetre = pygame.display.set_mode((1500, 750))
#On définit la largeur et la longueur de la fenêtre en pixels

clavier = pygame.image.load("piano.png").convert_alpha() 
touche = pygame.image.load("db.png").convert()
touche_n = pygame.image.load("gb.png").convert()
terrain = pygame.image.load("terrain.png").convert()
#Chargement des images

fichier = open("droite.txt","r")
fichier2 = open("gauche.txt","r")
#Chargement des fichiers textes

class Test():
    def __init__(self, touche, time_pos, time, posy=0, posx=0, val=0, ok=0):
        self.touche = touche
        self.time_pos = time_pos
        self.time = time
        self.posy = posy
        self.posx = posx
        self.val = val
        self.ok = ok
#Création d'une classe qui va contenir les infos de la partition
#touche = numéro de la touche, time_pos timing de la touche
#(a quel moment on appuie dessus quoi), time, le temps durant lequel 
#on reste appuyé sur la touche, posy et posx la position de la touche sur 
#la fénêtre, et val, la variable qui permet de passer d'une touche à l'autre

n=0
for line in fichier:
    n+=1
n2=0
for line in fichier2:
    n2+=1
#On compte le nombre de lignes pour les deux partitions
    
fichier.seek(0)
fichier2.seek(0)

touches = []
touches2 = []

partition = []
partition2 = []

for att in dir(Test):
    print (att, getattr(Test,att))

#Création de tableau vide, qui vont contenir les éléments de la structure

for line in fichier:
    extr = line.split()
    partition.append(Test(extr[0], extr[1], extr[2], -int(extr[2]),(int(extr[0])-44)*43, 0, 0))
#On place les éléments du fichiers textes dans nos tableaux
    
for obj in partition:
    touches.append(pygame.transform.scale(touche, (44,int(obj.time))))
#On définit les tailles des touches en fonction de la partition
    
print(partition[0].__dict__)
    
    
for line in fichier2:
    extr2 = line.split()
    partition2.append(Test(extr2[0], extr2[1], extr2[2], -int(extr2[2]),(int(extr2[0])-44)*43, 0, 0))
    
for obj in partition2:
    touches2.append(pygame.transform.scale(touche_n, (44,int(obj.time))))

posx = 0
posy = 0

pygame.display.flip()
#pygame.key.set_repeat(400,30)

haut=bas=gauche=droite=0

font = pygame.font.SysFont("gameovercre", 30)
#On définit une police 

continuer = 1
c=0
score=0
score_t=0
combo=0

osu=0

fail=0

while continuer:
    c+=1
    for event in pygame.event.get():  
        if event.type == QUIT:     
            continuer = 0
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                bas=1
            if event.key == K_UP:
                haut=1
            if event.key == K_RIGHT:
                droite=1
                score=1
            if event.key == K_LEFT:
                gauche=1
        if event.type == KEYUP:
            if event.key == K_DOWN:
                bas=0
            if event.key == K_UP:
                haut=0
            if event.key == K_RIGHT:
                droite=0
                #score=0
            if event.key == K_LEFT:
                gauche=0
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                posx = event.pos[0]
                posy = event.pos[1]
    if droite == 1:
        posx+=1
    if gauche == 1:
        posx-=1
    if haut == 1:
        posy-=1
    if bas == 1:
        posy+=1
    
        
    for i in range(n):
        if i == 0:
            if partition[0].posy+int(partition[0].time)<fenetre.get_height()- clavier.get_height() and partition[0].val==0:
                partition[0].posy+=1
            elif partition[0].val == 1:
                partition[0].posy+=1
        elif partition[i].posy+int(partition[i].time)<=partition[i-1].posy and partition[i].val == 0 and partition[i].posy+int(partition[i].time)<fenetre.get_height()- clavier.get_height():
            partition[i].posy+=1
        elif partition[i].posy+int(partition[i].time)<=partition[i-1].posy and partition[i].val == 1:
            partition[i].posy+=1
        if i == 0:
            if partition2[0].posy+int(partition2[0].time)<fenetre.get_height()- clavier.get_height() and partition2[0].val==0:
                partition2[0].posy+=1
            if partition2[0].val == 1:
                partition2[0].posy+=1
        elif partition2[i].posy+int(partition2[i].time)<=partition2[i-1].posy and partition2[i].val == 0 and partition2[i].posy+int(partition2[i].time)<fenetre.get_height()- clavier.get_height():
            partition2[i].posy+=1
        elif partition2[i].posy+int(partition2[i].time)<=partition2[i-1].posy and partition2[i].val == 1:
            partition2[i].posy+=1
#Bon hein jvais pas tout commenté non plus zêtes des fous
            

    for i in range(n):
        if i == 0:
            if partition[0].val == 0 and score == 1:
                partition[0].val=1
                partition2[0].val=1
                score=0
                break
        else:
            if partition[i-1].val == 1 and score == 1 and partition[i].val == 0:
                partition[i].val =1
                partition2[i].val =1
                score=0
                print(i)
    '''          
    for i in range(n):
        if i == 0:
            if partition2[0].val == 0 and score == 1:
                partition2[0].val=1
                score=0
                break
        else:
            if partition2[i-1].val == 1 and score == 1 and partition2[i].val == 0:
                partition2[i].val =1
                score=0
                print(i)
    '''
    fenetre.blit(terrain, (0,0))
    
    for i in range(n):
        fenetre.blit(touches[i], (partition[i].posx, partition[i].posy))
        fenetre.blit(touches2[i], (partition2[i].posx, partition2[i].posy))
    
    
    '''
    for i in range(n):
        if int(partition[i].time_pos)<c:
            partition[i].posy+=1
    
    fenetre.blit(terrain, (0,0))
    
    for i in range(n):
        if score==1 and partition[i].posy>fenetre.get_height()- clavier.get_height()-int(partition[i].time) and partition[i].posy<fenetre.get_height()- clavier.get_height():
            touches[i].fill((0,0,255,255),special_flags=BLEND_RGBA_MULT)
            if partition[i].ok == 0:
                partition[i].val=1
                #if partition[i-1].ok == 1:
                #    combo+=1
        fenetre.blit(touches[i], (partition[i].posx, partition[i].posy))
        
    for i in range(n):
        if partition[i].val == 1:
            osu+=300
            partition[i].val=0
            partition[i].ok =1
            if partition[i-1].ok == 1:
                combo+=1
        if partition[i-1].ok == 0:
            fail=1
    
    if fail==1:
        combo=0
        fail=0
    '''
            
        #if score == 1:
        #    surface=pygame.Surface((45,int(partition[i].time)))
        #    surface.fill((0,0,255))
        #    surface.set_alpha(score_t)
        #    fenetre.blit(surface,(partition[i].posx, partition[i].posy) )
        
    fenetre.blit(clavier, (0, fenetre.get_height()- clavier.get_height()))
    
    write = "%d s, score : %d,  : %d, test ; %d %d %d" % ((int(c)/100),osu, score, partition[0].val,partition[1].val,partition[2].val )
    texte = font.render(write, 1, (0,0,0))
    
    '''
    if score==1:
        score_t+=1
        if score_t>=300:
            score_t=0
            score=0
        text = font.render("DE QUOI !",1,(0,0,0))
        surface=pygame.Surface((150,30))
        surface.fill((255,255,255))
        surface.blit(text, pygame.Rect(0,0,10,10))
        surface.set_alpha(score_t)
        fenetre.blit(surface, pygame.Rect(100,score_t/3,10,10))
    '''
    
    fenetre.blit(texte, (0,0))
    
    pygame.display.flip()
    
fichier.close()
fichier2.close()
#fichier_midi.close()
pygame.display.quit()