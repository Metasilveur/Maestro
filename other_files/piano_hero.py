import pygame
from pygame.locals import *
import pygame.midi

pygame.init()
pygame.midi.init()

fenetre = pygame.display.set_mode((1500, 750))
clavier = pygame.image.load("piano.png").convert_alpha()
touche = pygame.image.load("db.png").convert()
terrain = pygame.image.load("terrain.png").convert()

fichier = open("droite.txt","r")


class Test():
    def __init__(self, touche, time_pos, time, posy=0, posx=0, val=0, ok=0):
        self.touche = touche
        self.time_pos = time_pos
        self.time = time
        self.posy = posy
        self.posx = posx
        self.val = val
        self.ok = ok

n=0
for line in fichier:
    n+=1
    
fichier.seek(0)

touches = []

partition = []

for line in fichier:
    extr = line.split()
    partition.append(Test(extr[0], extr[1], extr[2], -int(extr[2]),(int(extr[0])-62)*43, 0, 0))
    
for obj in partition:
    touches.append(pygame.transform.scale(touche, (43,int(obj.time))))

#for obj in partition:
#   print(obj.touche, obj.time_pos, obj.time)
    
fichier_midi = open("test.mid","rb")

#ligne = fichier.readline()

#print(ligne)

#for line in fichier:
#    for word in line.split():
#        print("test ",word)

#for line in fichier_midi:
#    print(line)

print(fichier_midi.readline())

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

#inp = pygame.midi.Input(1)

midivalues = []

while continuer:
    c+=1
    
    '''if inp.poll():
        midi_value = inp.read(1000)[0][0][1]
        score=1
        print(midi_value)'''
     
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
                score=0
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
            
        #if score == 1:
        #    surface=pygame.Surface((45,int(partition[i].time)))
        #    surface.fill((0,0,255))
        #    surface.set_alpha(score_t)
        #    fenetre.blit(surface,(partition[i].posx, partition[i].posy) )
        
    fenetre.blit(clavier, (0, fenetre.get_height()- clavier.get_height()))
    
    write = "%d s, score : %d, combo : %d" % ((int(c)/100),osu, combo)
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
#fichier_midi.close()
#inp.close()
pygame.display.quit()