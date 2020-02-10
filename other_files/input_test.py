import pygame
from pygame.locals import *
import pygame.midi

pygame.init()
pygame.midi.init()

fenetre = pygame.display.set_mode((1500, 750))

clavier = pygame.image.load("Images/piano.png").convert_alpha()

touche = pygame.image.load("Images/db.png").convert()
touchen = pygame.image.load("Images/dn.png").convert()
touche_n = pygame.image.load("Images/gb.png").convert()
touchen_n = pygame.image.load("Images/gn.png").convert()

terrain = pygame.image.load("Images/terrain.png").convert()

fichier = open("txt_files/EliseDroite.txt","r")
fichier2 = open("txt_files/gauche.txt","r")

class Touche_Info():
    def __init__(self, touche, time_pos, time,octave, posy=0, posx=0, pressed=0):
        self.touche = touche
        self.time_pos = time_pos
        self.time = time
        self.octave = octave
        self.posy = posy
        self.posx = posx
        self.pressed = pressed

n=0
for line in fichier:
    n+=1
    
n2=0
for line in fichier2:
    n2+=1
    
fichier.seek(0)
fichier2.seek(0)

touches = []
touches2 = []

partition = []
partition2 = []


for line in fichier:
    extr = line.split()
    if(int(extr[0])%12 == 0):
        partition.append(Touche_Info(extr[0], extr[1], extr[2], int(extr[0])/12 ,-int(extr[2]),(int((int(extr[0])/12))-5)*300, 0))
    elif(int(extr[0])%12 == 2):
        partition.append(Touche_Info(extr[0], extr[1], extr[2], int(extr[0])/12 ,-int(extr[2]),43+(int((int(extr[0])/12))-5)*300, 0))
    elif(int(extr[0])%12 == 4):
        partition.append(Touche_Info(extr[0], extr[1], extr[2], int(extr[0])/12 ,-int(extr[2]),2*43+(int((int(extr[0])/12))-5)*300, 0))
    elif(int(extr[0])%12 ==1):
        partition.append(Touche_Info(extr[0], extr[1], extr[2], int(extr[0])/12 ,-int(extr[2]),26+(int((int(extr[0])/12))-5)*300, 0))
    elif(int(extr[0])%12 == 3):
        partition.append(Touche_Info(extr[0], extr[1], extr[2], int(extr[0])/12 ,-int(extr[2]),52+26+(int((int(extr[0])/12))-5)*300, 0))
    elif(int(extr[0])%12 == 5):
        partition.append(Touche_Info(extr[0], extr[1], extr[2], int(extr[0])/12 ,-int(extr[2]),3*43+(int((int(extr[0])/12))-5)*300, 0))
    elif(int(extr[0])%12 == 7):
        partition.append(Touche_Info(extr[0], extr[1], extr[2], int(extr[0])/12 ,-int(extr[2]),4*43+(int((int(extr[0])/12))-5)*300, 0))
    elif(int(extr[0])%12 == 9):
        partition.append(Touche_Info(extr[0], extr[1], extr[2], int(extr[0])/12 ,-int(extr[2]),5*43+(int((int(extr[0])/12))-5)*300, 0))
    elif(int(extr[0])%12 == 11):
        partition.append(Touche_Info(extr[0], extr[1], extr[2], int(extr[0])/12 ,-int(extr[2]),6*43+(int((int(extr[0])/12))-5)*300, 0))
    elif(int(extr[0])%12 == 6):
        partition.append(Touche_Info(extr[0], extr[1], extr[2], int(extr[0])/12 ,-int(extr[2]),77+52+26+(int((int(extr[0])/12))-5)*300, 0))
    elif(int(extr[0])%12 == 8):
        partition.append(Touche_Info(extr[0], extr[1], extr[2], int(extr[0])/12 ,-int(extr[2]),77+2*52+26+(int((int(extr[0])/12))-5)*300, 0))
    elif(int(extr[0])%12 == 10):
        partition.append(Touche_Info(extr[0], extr[1], extr[2], int(extr[0])/12 ,-int(extr[2]),77+3*52+26+(int((int(extr[0])/12))-5)*300, 0))


for obj in partition:
    if(int(obj.touche)%12 < 5):
        if((int(obj.touche)%12)%2 == 0):
            touches.append(pygame.transform.scale(touche, (44,int(obj.time))))
        else:
            touches.append(pygame.transform.scale(touchen, (26,int(obj.time))))
    else:
        if((int(obj.touche)%12)%2 == 1):
            touches.append(pygame.transform.scale(touche, (44,int(obj.time))))
        else:
            touches.append(pygame.transform.scale(touchen, (26,int(obj.time))))        
    

    
for line in fichier2:
    extr2 = line.split()
    partition2.append(Touche_Info(extr2[0], extr2[1], extr2[2], -int(extr2[2]),(int(extr2[0])-44)*43, 0, 0))
    
for obj in partition2:
    touches2.append(pygame.transform.scale(touche_n, (44,int(obj.time))))
    

#for obj in partition:
#   print(obj.touche, obj.time_pos, obj.time)
    
#fichier_midi = open("test.mid", "rb")

#ligne = fichier.readline()

#print(ligne)

#for line in fichier:
#    for word in line.split():
#        print("test ",word)

#for line in fichier_midi:
#    print(line)

posx = 0
posy = 0

pygame.display.flip()
#pygame.key.set_repeat(400,30)

haut=bas=gauche=droite=0

font = pygame.font.SysFont("gameovercre", 30)

#texte = font.render("Salut, gros FDP", 1, (0,0,0))

continuer = 1
c=0
score=0
score_t=0
combo=0

osu=0

fail=0

touche_actuelle = partition[0].touche

inp = pygame.midi.Input(1)

print(n)

while continuer:
    if inp.poll():
        midi_value = inp.read(1000)[0][0][0:2]
        print(midi_value)
        print(touche_actuelle)
        if midi_value == [144, int(touche_actuelle)]:
            score=1
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
            if partition[0].posy+int(partition[0].time)<fenetre.get_height()- clavier.get_height() and partition[0].pressed==0:
                partition[0].posy+=1
            if partition[0].pressed == 1:
                partition[0].posy+=1
        elif partition[i].posy+int(partition[i].time)<=partition[i-1].posy and partition[i].pressed == 0 and partition[i].posy+int(partition[i].time)<fenetre.get_height()- clavier.get_height():
            partition[i].posy+=1
        elif partition[i].posy+int(partition[i].time)<=partition[i-1].posy and partition[i].pressed == 1:
            partition[i].posy+=1
            '''
        if i == 0:
            if partition2[0].posy+int(partition2[0].time)<fenetre.get_height()- clavier.get_height() and partition2[0].val==0:
                partition2[0].posy+=1
            if partition2[0].val == 1:
                partition2[0].posy+=1
        elif partition2[i].posy+int(partition2[i].time)<=partition2[i-1].posy and partition2[i].val == 0 and partition2[i].posy+int(partition2[i].time)<fenetre.get_height()- clavier.get_height():
            partition2[i].posy+=1
        elif partition2[i].posy+int(partition2[i].time)<=partition2[i-1].posy and partition2[i].val == 1:
            partition2[i].posy+=1
            '''
            

    for i in range(n):
        if i == 0:
            if partition[0].pressed == 0 and score == 1:
                partition[0].pressed=1
                #partition2[0].pressed=1
                touche_actuelle = partition[1].touche
                score=0
                break
        else:
            if partition[i-1].pressed == 1 and score == 1 and partition[i].pressed == 0:
                partition[i].pressed =1
                #partition2[i].val =1
                touche_actuelle = partition[i+1].touche
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
        #fenetre.blit(touches2[i], (partition2[i].posx, partition2[i].posy))
    
    
    
    
    
    
    
    
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
    
    write = "%d s, score : %d,  : %d, test ; %d %d %d" % ((int(c)/100),osu, score, partition[0].pressed,partition[1].pressed,partition[2].pressed )
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
inp.close()
pygame.display.quit()