import pygame
from pygame.locals import *
from mido import MidiFile
from mido import MetaMessage
from mido import Message, MidiTrack
import pygame.midi


pygame.init()
fenetre = pygame.display.set_mode((1500, 750))

clavier = pygame.image.load("Images/piano.png").convert_alpha() 
touche = pygame.image.load("Images/db.png").convert()
touchen = pygame.image.load("Images/dn.png").convert()
touche_n = pygame.image.load("Images/gb.png").convert()
terrain = pygame.image.load("Images/terrain.png").convert()


'''
pygame.init()
fenetre = pygame.display.set_mode((626, 626))
logo = pygame.image.load("logo.png").convert_alpha() 
mid = MidiFile('ludovico.mid')

for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)

logo_a = []

for i in range(5):
    cropped = pygame.Surface([626, 626], pygame.SRCALPHA, 32)
    cropped = cropped.convert_alpha()
    cropped.blit(logo, (0,0), (i*626,0,626,626))
    logo_a.append(cropped)
    
for i in range(3):
    cropped = pygame.Surface([626, 626], pygame.SRCALPHA, 32)
    cropped = cropped.convert_alpha()
    cropped.blit(logo, (0,0), (i*626,626,626,626))
    logo_a.append(cropped)   
'''
class Test():
    def __init__(self, touche, time_pos, time,octave, posy=0, posx=0, val=0):
        self.touche = touche
        self.time_pos = time_pos
        self.time = time
        self.octave = octave
        self.posy = posy
        self.posx = posx
        self.val = val

class conv():
    def __init__(self, type, note, time):
        self.type = type
        self.note = note
        self.time = time

mid = MidiFile('Midi_Files/ludovico.mid')

conversion = []
partition = []
touches = []

compteur = 0

for i,j in enumerate(mid.tracks):
    if i==1:
        for msg in j:
            if msg.type == 'note_on' or msg.type == 'note_off':
                conversion.append(conv(msg.type, msg.bytes()[1], msg.time))
                #print(msg.type, msg.bytes()[1], msg.time)
#print(conversion)
taille = len(conversion)
print(taille)
tempo = 0

def verif_note_on(nb):
    for i in range(nb):
        if conversion[i].type != 'note_on':
            return False
    return True
        
if verif_note_on(30):
    for i in range(len(conversion)):
        if conversion[i].type == 'note_on':
            cp = 1
            if conversion[i].note == conversion[i+cp].note:
                conversion[i+cp].type = 'note_off'
            while conversion[i].note != conversion[i+cp].note:
                cp += 1
            if cp != 1:
                conversion[i+cp].type = 'note_off'
            
#for obj in conversion:
    #print(obj.type, obj.note, obj.time)
    
for i in range(len(conversion)):
    if conversion[i].type == 'note_on':
        cp = 1
        time_on = int(conversion[i].time)
        time_off = 0
        while conversion[i].note != conversion[i+cp].note:
            cp += 1
            time_off += int(conversion[i+cp].time)
        if conversion[i].note == conversion[i+cp].note:
            time_off = int(conversion[i+cp].time)
        tempo += int(conversion[i].time)
        note_centre = int(conversion[i].note)%12
        if note_centre < 5:
            if note_centre%2 == 0:
                note_place=(note_centre/2)*43
            else:
                note_place=26+int(note_centre/2)*43
        else:
            if note_centre%2 == 1:
                note_place=(((conversion[i].note-5)%12)/2)*43+129
            else:
                note_place=(((conversion[i].note-6)%12)/2)*43+121
        nb_octave_px = (int(conversion[i].note/12)-4)*300
        partition.append(Test(conversion[i].note, tempo, time_off, int(conversion[i].note)/12, -(time_off), note_place+nb_octave_px, 0))
    else:
        tempo += int(conversion[i].time)

for obj in partition:
    print(obj.touche, obj.time_pos, obj.time)
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
            
posx = 0
posy = 0

haut=bas=gauche=droite=0

font = pygame.font.SysFont("gameovercre", 30)
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
    

    for i in range(int(taille/2)):
        if i == 0:
            if partition[0].posy+int(partition[0].time)<fenetre.get_height()- clavier.get_height() and partition[0].val==0:
                partition[0].posy+=1
            elif partition[0].val == 1:
                partition[0].posy+=1
        elif partition[i].posy+int(partition[i].time)<=partition[i-1].posy and partition[i].val == 0 and partition[i].posy+int(partition[i].time)<fenetre.get_height()- clavier.get_height():
            partition[i].posy+=1
        elif partition[i].posy+int(partition[i].time)<=partition[i-1].posy and partition[i].val == 1:
            partition[i].posy+=1
#Bon hein jvais pas tout commenté non plus zêtes des fous
    
    
    for i in range(int(taille/2)):
        if i == 0:
            if partition[0].val == 0 and score == 1:
                partition[0].val=1
                score=0
                break
        else:
            if partition[i-1].val == 1 and score == 1 and partition[i].val == 0:
                partition[i].val =1
                score=0
    
    fenetre.blit(terrain, (0,0))
    
    for i in range(int(taille/2)):
        fenetre.blit(touches[i], (partition[i].posx, partition[i].posy))
    fenetre.blit(clavier, (0, fenetre.get_height()- clavier.get_height()))
    
    write = "COUCOU %d s, score : %d,  : %d, test ; %d %d %d" % ((int(c)/100),osu, score, partition[0].val,partition[1].val,partition[2].val)
    texte = font.render(write, 1, (0,0,0))
    fenetre.blit(texte, (0,0))
    
    pygame.display.flip()

    
    
'''    
for obj in partition:
    print(obj.touche, obj.time_pos, obj.time, obj.octave)'''
'''
index=0
for i,j in enumerate(mid.tracks):
    for msg in j:
        print(index, msg)
        index +=1
 ''' 
      
'''def getNoteRangeAndTicks(files_dir, res_factor=1):
    ticks = []
    notes = []
    for file_dir in files_dir:
        file_path = "%s" %(file_dir)
        mid = MidiFile(file_path)                   
        
        for track in mid.tracks: #preprocessing: Checking range of notes and total number of ticks
            num_ticks = 0           
            for message in track:
                if not isinstance(message, MetaMessage):
                    notes.append(message.note)
                    num_ticks += int(message.time/res_factor)
            ticks.append(num_ticks)
                    
    return min(notes), max(notes), max(ticks) '''
    
#print(mid.ticks_per_beat)
    
'''continuer = 1
i = 0
clock = pygame.time.Clock()

while continuer:
    for event in pygame.event.get():  
        if event.type == QUIT:     
            continuer = 0
    i+=1
    if i == 7:
        i=0
    fenetre.blit(logo_a[i], (0,0))
    pygame.display.flip()
    clock.tick(10)'''

pygame.display.quit()
