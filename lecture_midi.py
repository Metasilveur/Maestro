import pygame
from pygame.locals import *
from mido import MidiFile
from mido import MetaMessage
from mido import Message, MidiTrack
import pygame.midi
import pygame as pg
from pygame import gfxdraw

from colour import Color

def main2(argv):
    pygame.init()
    pygame.midi.init()
    fenetre = pygame.display.set_mode((1470, 750), DOUBLEBUF)
    
    fenetre.set_alpha(None)
    fond = pygame.image.load("Images/fond3.png").convert_alpha()
    
    clavier = pygame.image.load("Images/clavier7.png").convert_alpha() 
    touche = pygame.image.load("Images/db.png").convert()
    touchen = pygame.image.load("Images/dn.png").convert()
    touche_n = pygame.image.load("Images/gb.png").convert()
    terrain = pygame.image.load("Images/terrain.png").convert()
    
    appuie = pygame.image.load("Images/appuie.png").convert()
    appuie2 = pygame.image.load("Images/appuie2.png").convert()
    
    fond1 = pygame.image.load("Images/fond.png").convert()
    
    red = Color("red")
    colors = list(red.range_to(Color("green"),10))
    
    midiOut = pygame.midi.Output(0)
    
    class Test():
        def __init__(self, touche, time_pos, time,octave, posy=0, posx=0, val=0, nature='ok',increment=0):
            self.touche = touche
            self.time_pos = time_pos
            self.time = time
            self.octave = octave
            self.posy = posy
            self.posx = posx
            self.val = val
            self.nature = nature
            self.increment = increment
            
    class conv():
        def __init__(self, type, note, time):
            self.type = type
            self.note = note
            self.time = time
            
    path = "fichier_midi/"
    Fpath = path + argv
    mid = MidiFile(Fpath)
    
    print("a")
    conversion = []
    conversion2 = []
    partition = []
    partition2 = []
    
    gris = []
    
    for i in range(88):
        gris.append(0)
        
    
    
    compteur = 0
    
    fichier = open("midi.txt","w")
    
    for i,j in enumerate(mid.tracks):
        for msg in j:
            fichier.write("%s %s %s\n" % (msg.type,msg.bytes()[1],msg.time))
    
    p1 = 0
    ok =0
    ligne = 0
    for i,j in enumerate(mid.tracks):
        for msg in j:
            if (msg.type == 'note_on' or msg.type == 'note_off') and (p1 == 0 or p1==2):
                conversion.append(conv(msg.type, msg.bytes()[1], int(msg.time*1.7)))
                #print("%s, %s, %s" % (msg.type, msg.bytes()[1], msg.time))
            if msg.type == 'end_of_track' and len(conversion) == 0:
                p1 = 2
            elif msg.type == 'end_of_track' and len(conversion)>0:
                p1=1
            if (msg.type == 'note_on' or msg.type == 'note_off') and p1 == 1:
                conversion2.append(conv(msg.type, msg.bytes()[1], int(msg.time*1.7)))   
                #print("Droite : %s, %s, %s" % (msg.type, msg.bytes()[1], msg.time))
    
    

    taille = len(conversion)
    taille2 = len(conversion2)
    print(taille2)
    tempo = 0
    
    def _render_region(image, rect, color, rad):
        """Helper function for round_rect."""
        corners = rect.inflate(-2*rad, -2*rad)
        for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
            pg.draw.circle(image, color, getattr(corners,attribute), rad)
        image.fill(color, rect.inflate(-2*rad,0))
        image.fill(color, rect.inflate(0,-2*rad))
    
    def round_rect(surface, rect, color, rad=20, border=0, inside=(0,0,0,0)):
        """
        Draw a rect with rounded corners to surface.  Argument rad can be specified
        to adjust curvature of edges (given in pixels).  An optional border
        width can also be supplied; if not provided the rect will be filled.
        Both the color and optional interior color (the inside argument) support
        alpha.
        """
        rect = pg.Rect(rect)
        zeroed_rect = rect.copy()
        zeroed_rect.topleft = 0,0
        image = pg.Surface(rect.size).convert_alpha()
        image.fill((0,0,0,0))
        _render_region(image, zeroed_rect, color, rad)
        if border:
            zeroed_rect.inflate_ip(-2*border, -2*border)
            _render_region(image, zeroed_rect, inside, rad)
        surface.blit(image, rect)
    
    def verif_note_on(nb):
        for i in range(nb):
            if conversion[i].type != 'note_on':
                return False
        return True
            
    if verif_note_on(10):
        for i in range(len(conversion)):
            if conversion[i].type == 'note_on':
                cp = 1
                if conversion[i].note == conversion[i+cp].note:
                    conversion[i+cp].type = 'note_off'
                while conversion[i].note != conversion[i+cp].note:
                    cp += 1
                if cp != 1:
                    conversion[i+cp].type = 'note_off'
        for i in range(len(conversion2)):
            if conversion2[i].type == 'note_on':
                cp = 1
                if conversion2[i].note == conversion2[i+cp].note:
                    conversion2[i+cp].type = 'note_off'
                while conversion2[i].note != conversion2[i+cp].note:
                    cp += 1
                if cp != 1:
                    conversion2[i+cp].type = 'note_off'
            
                
    #for obj in conversion:
    #    print(obj.type, obj.note, obj.time)
                    
    def verif_blanc(touche):
        if(int(touche)%12 < 5):
            if((int(touche)%12)%2 == 0):
                return True
            else:
                return False
        else:
            if((int(touche)%12)%2 == 1):
                return True
            else:
                return False
        
    for i in range(len(conversion)):
        if conversion[i].type == 'note_on':
            cp = 1
            time_on = int(conversion[i].time)
            time_off = 0
            while conversion[i].note != conversion[i+cp].note:
                time_off += int(conversion[i+cp].time)
                cp += 1
            time_off += int(conversion[i+cp].time)
            tempo += int(conversion[i].time)
            note_centre = int(conversion[i].note)%12
            if note_centre < 5:
                if note_centre%2 == 0:
                    note_place=(note_centre/2)*30
                else:
                    note_place=19+(note_centre/2)*30
            else:
                if note_centre%2 == 1:
                    note_place=(((conversion[i].note-5)%12)/2)*30+3*30
                else:
                    note_place=(((conversion[i].note-6)%12)/2)*30+108
            nb_octave_px = (int(conversion[i].note/12)-2)*210
            if verif_blanc(conversion[i].note):
                partition.append(Test(conversion[i].note, int(tempo/10), int(time_off/10), int(conversion[i].note)/12, -int(time_off/10), note_place+nb_octave_px, 0, 'blanc'))
            else:
                partition.append(Test(conversion[i].note, int(tempo/10), int(time_off/10), int(conversion[i].note)/12, -int(time_off/10), note_place+nb_octave_px, 0, 'noir'))
        else:
            tempo += int(conversion[i].time)
            
    tempo = 0
            
    for i in range(len(conversion2)):
        if conversion2[i].type == 'note_on':
            cp = 1
            time_on = int(conversion2[i].time)
            time_off = 0
            while conversion2[i].note != conversion2[i+cp].note:
                time_off += int(conversion2[i+cp].time)
                cp += 1
            time_off += int(conversion2[i+cp].time)
            tempo += int(conversion2[i].time)
            note_centre = int(conversion2[i].note)%12
            if note_centre < 5:
                if note_centre%2 == 0:
                    note_place=(note_centre/2)*30
                else:
                    note_place=19+(note_centre/2)*30
            else:
                if note_centre%2 == 1:
                    note_place=(((conversion2[i].note-5)%12)/2)*30+3*30
                else:
                    note_place=(((conversion2[i].note-6)%12)/2)*30+108
            nb_octave_px = (int(conversion2[i].note/12)-2)*210
            if verif_blanc(conversion2[i].note):
                partition2.append(Test(conversion2[i].note, int(tempo/10), int(time_off/10), int(conversion2[i].note)/12, -int(time_off/10), note_place+nb_octave_px, 0, 'blanc'))
            else:
                partition2.append(Test(conversion2[i].note, int(tempo/10), int(time_off/10), int(conversion2[i].note)/12, -int(time_off/10), note_place+nb_octave_px, 0, 'noir'))
        else:
            tempo += int(conversion2[i].time)
            
            
    for obj in partition:
        print(obj.touche, obj.time_pos, obj.time, obj.posx, obj.posy)
                
    
    partitionFinal = []
    
    for obj in partition:
        partitionFinal.append(Test(obj.touche, obj.time_pos, obj.time, obj.posx, obj.posy))
        
    for obj in partition2:
        partitionFinal.append(Test(obj.touche, obj.time_pos, obj.time, obj.posx, obj.posy))
        
    partitionFinal.sort(key=lambda x: x.time_pos, reverse=False)
    
    #for obj in partitionFinal:
    #    print(obj.touche, obj.time_pos, obj.time, obj.posx, obj.posy)
        
        
    posx = 0
    posy = 0
    
    haut=bas=gauche=droite=0
    
    font = pygame.font.SysFont("gameovercre", 30)
    continuer = 1
    c=0
    score = 0
    
    touche_actuelle = []
    
    
    touche_actuelle.append(partitionFinal[0])
        
    index = 0
    
    while partitionFinal[index].time_pos == partitionFinal[index+1].time_pos:
        touche_actuelle.append(partitionFinal[index+1])
        index += 1
    
    
    
        

    #touche_actuelle = [partition[0],partition[1]]
    
    #print(len(touche_actuelle))
    
    tps_actuel=tps_precedent=0
    start =1
    stop =0
    
    fenetre.blit(fond, (0,0))
    
    index = 0
    
    class vecColor:
        def __init__(self, r, g, b):
            self.R = r
            self.G = g
            self.B = b
            
    
    def computeVarColor(first, second, shades):
        toReturn = vecColor(0.0, 0.0, 0.0)
        
        toReturn.R = abs(first.R - second.R)/shades
        if first.R>second.R:
            toReturn.R = -1*toReturn.R
        toReturn.G = abs(first.G - second.G)/shades
        if first.G>second.G:
            toReturn.G = -1*toReturn.G
        toReturn.B = abs(first.B - second.B)/shades
        if first.B>second.B:
            toReturn.B = -1*toReturn.B
        
        return toReturn
    
    
    color1 = vecColor(132,176,217)
    color2 = vecColor(33,112,187)
    
    
    colorvars = computeVarColor(color1, color2, 200)
    
   # for i in range(300):
   #     print("%d %d %d" % (color1.R + i*colorvars.R, color1.G + i*colorvars.G, color1.B + i*colorvars.B))
    
    inp = pygame.midi.Input(1)
    
    #compteurDroite = 0  
    #compteurGauche = 0
    
    while continuer:
        if inp.poll():
            for items in inp.read(1000):
                
                #midi_value = items[0][1:3]
                
                
                #if midi_value[1] != 0:
                #    midiOut.note_on(midi_value[0],127)
                #elif midi_value[1] == 0:
                #    midiOut.note_off(midi_value[0],127)
                    
                midi_value = items[0][0:3]
                
                if midi_value[0] == 144:
                    midiOut.note_on(midi_value[1],127)
                elif midi_value[0] != 144:
                    midiOut.note_off(midi_value[1],127)                
                
                
                for elem in touche_actuelle:
                    print("%d %d %d" % (elem.touche, elem.time_pos, elem.posy))
                    
                print(midi_value)
                print(partition2[0].val)
                
                if len(touche_actuelle) == 1 and touche_actuelle[0].posy+touche_actuelle[0].time>=531:
                    #♦if midi_value[0] == int(touche_actuelle[0].touche) and midi_value[1] != 0:
                    if midi_value[1] == int(touche_actuelle[0].touche) and midi_value[0] == 144 and midi_value[2] != 0:
                        
                        touche_actuelle[0].val =1
                        
                        for i in range(int(taille/2)):
                            if touche_actuelle[0].touche == partition[i].touche and touche_actuelle[0].time_pos == partition[i].time_pos:
                                partition[i].val = 1
                        for i in range(int(taille2/2)):
                            if touche_actuelle[0].touche == partition2[i].touche and touche_actuelle[0].time_pos == partition2[i].time_pos:
                                partition2[i].val = 1                        
                        '''if touche_actuelle[0].touche == partition[compteurDroite].touche and touche_actuelle[0].time_pos == partition[compteurDroite].time_pos:
                            partition[compteurDroite].val = 1
                            compteurDroite+=1
                        elif touche_actuelle[0].touche == partition2[compteurGauche].touche and touche_actuelle[0].time_pos == partition2[compteurGauche].time_pos:
                            partition2[compteurGauche].val = 1
                            compteurGauche+=1'''
                        
                        index+=1
                        
                        del touche_actuelle[:]
                        
                        plus = 0
                        
                        touche_actuelle.append(partitionFinal[index])
                        
                        while partitionFinal[index+plus].time_pos == partitionFinal[index+1+plus].time_pos:
                            touche_actuelle.append(partitionFinal[index+1+plus])
                            plus+=1
                    '''else:
                        touche_actuelle[0].val =2
                        index+=1
                        del touche_actuelle[:]
                        if partition[index].time_pos == partition[index+1].time_pos:
                            touche_actuelle.append(partition[index])
                            touche_actuelle.append(partition[index+1])
                        else:
                            touche_actuelle.append(partition[index])'''
                else:
                    for elem in touche_actuelle:
                        if elem.posy+elem.time>=531:
                            #if midi_value[0] == int(elem.touche) and midi_value[1] != 0:
                            if midi_value[1] == int(elem.touche) and midi_value[0] == 144 and midi_value[2] != 0:
                                elem.val = 1
                                
                                for i in range(int(taille/2)):
                                    if elem.touche == partition[i].touche and elem.time_pos == partition[i].time_pos:
                                        partition[i].val = 1
                                for i in range(int(taille2/2)):
                                    if elem.touche == partition2[i].touche and elem.time_pos == partition2[i].time_pos:
                                        partition2[i].val = 1   
                                '''if elem.touche == partition[compteurDroite].touche and elem.time_pos == partition[compteurDroite].time_pos:
                                    partition[compteurDroite].val = 1
                                    compteurDroite+=1
                                elif elem.touche == partition2[compteurGauche].touche and elem.time_pos == partition2[compteurGauche].time_pos:
                                    partition2[compteurGauche].val = 1
                                    compteurGauche+=1'''
                    ok = 1
                    for elem in touche_actuelle:
                        if elem.val == 1 or elem.val == 2:
                            ok *= 1
                        else:
                            ok *=0
                    if ok ==1:
                        index += len(touche_actuelle)
                        del touche_actuelle[:]
                        plus = 0
                        
                        touche_actuelle.append(partitionFinal[index])
                        
                        while partitionFinal[index+plus].time_pos == partitionFinal[index+1+plus].time_pos:
                            touche_actuelle.append(partitionFinal[index+1+plus])
                            plus+=1
                
                
                        
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
                    '''if touche_actuelle.posy+touche_actuelle.time>=531:
                        score=1'''
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
        '''
        c+=1
        for i in range(int(taille/2)):
            if i == 0:
                if partition[0].posy+int(partition[0].time)<fenetre.get_height()- clavier.get_height() and partition[0].val==0:
                    partition[0].posy+=1
                elif partition[0].val == 1:
                    partition[0].posy+=1
            elif partition[i].posy+int(partition[i].time)<=partition[i-1].posy and partition[i].val == 0 and partition[i].posy+int(partition[i].time)<fenetre.get_height()- clavier.get_height():
                partition[i].posy+=1
            elif partition[i].posy+int(partition[i].time)<=partition[i-1].posy and partition[i].val == 1:
                partition[i].posy+=1'''
        
        tps_actuel = pygame.time.get_ticks()
    
        if start == 1:
            c+=1
            
        if len(touche_actuelle) == 1:
            if touche_actuelle[0].posy+int(touche_actuelle[0].time) < fenetre.get_height()- clavier.get_height():
                start=1
            elif touche_actuelle[0].posy+int(touche_actuelle[0].time) >= fenetre.get_height()- clavier.get_height():
                start = 0
        else:
            ok = 1
            for elem in touche_actuelle:
                if elem.posy+int(elem.time) < fenetre.get_height()- clavier.get_height():
                    ok*=1
                    #tps_precedent=tps_actuel
                elif elem.posy+int(elem.time) >= fenetre.get_height()- clavier.get_height():
                    ok*=0
                    #tps_precedent=tps_actuel
            if ok == 1:
                start=1
            else:
                start=0
                
        #fenetre.blit(fond, (0,0))
    
        
                    
        for i in range(int(taille/2)):
            cropped = pygame.Surface([44, partition[i].time], pygame.SRCALPHA, 32)
            cropped.blit(fond, (0,0), (partition[i].posx,partition[i].posy,44, partition[i].time))
            fenetre.blit(cropped, (partition[i].posx,partition[i].posy))
            if c>=partition[i].time_pos and start==1:
                partition[i].posy+=1
                
        for i in range(int(taille2/2)):
            cropped = pygame.Surface([44, partition2[i].time], pygame.SRCALPHA, 32)
            cropped.blit(fond, (0,0), (partition2[i].posx,partition2[i].posy,44, partition2[i].time))
            fenetre.blit(cropped, (partition2[i].posx,partition2[i].posy))
            if c>=partition2[i].time_pos and start==1:
                partition2[i].posy+=1
                
        for i in range(int(len(partitionFinal)/2)):
            if c>=partitionFinal[i].time_pos and start==1:
                partitionFinal[i].posy+=1            
                
            
        '''for i in range(int(taille/2)):
            if i == 0:
                if partition[0].val == 0 and score == 1:
                    #partition[0].val=1
                    del touche_actuelle[:]
                    touche_actuelle.append(partition[1])
                    score=0
                    break
            else:
                if partition[i-1].val == 1 and score == 1 and partition[i].val == 0:
                    #partition[i].val =1
                    if partition[i].time_pos == partition[i+1].time_pos:
                        del touche_actuelle[:]
                        touche_actuelle.append(partition[i])
                        touche_actuelle.append(partition[i+1])
                    score=0'''
        
        for i in range(int(taille/2)):
            
            '''if c>=partition[i].time_pos and partition[i].posy+partition[i].time-1 == fenetre.get_height()- clavier.get_height():
                midiOut.note_on(partition[i].touche,127)
                
            if c>=partition[i].time_pos and partition[i].posy == fenetre.get_height()- clavier.get_height():
                midiOut.note_off(partition[i].touche,127)'''
                
            if c>=partition[i].time_pos and partition[i].posy < fenetre.get_height()- clavier.get_height(): 
                if partition[i].val == 1:
                    if partition[i].nature == 'blanc':
                        round_rect(fenetre, (partition[i].posx,partition[i].posy,30,partition[i].time), pg.Color("blue"), 8,2,  (132,176,217,255))
                    else:
                        round_rect(fenetre, (partition[i].posx,partition[i].posy,19,partition[i].time), pg.Color("blue"), 5,2,  (33,112,187,255))
                elif partition[i].val == 0:
                    if partition[i].nature == 'blanc':
                        round_rect(fenetre, (partition[i].posx,partition[i].posy,30,partition[i].time), pg.Color("white"), 8,2,  (132,176,217,255))
                    else:
                        round_rect(fenetre, (partition[i].posx,partition[i].posy,19,partition[i].time), pg.Color("white"), 5,2,  (33,112,187,255))
                else:
                    if partition[i].nature == 'blanc':
                        round_rect(fenetre, (partition[i].posx,partition[i].posy,30,partition[i].time), pg.Color("red"), 8,2,  (132,176,217,255))
                    else:
                        round_rect(fenetre, (partition[i].posx,partition[i].posy,19,partition[i].time), pg.Color("red"), 5,2,  (33,112,187,255))
                        
        for i in range(int(taille2/2)):
            if c>=partition2[i].time_pos and partition2[i].posy < fenetre.get_height()- clavier.get_height(): 
                if partition2[i].val == 1:
                    if partition2[i].nature == 'blanc':
                        round_rect(fenetre, (partition2[i].posx,partition2[i].posy,30,partition2[i].time), pg.Color("blue"), 8,2,  (132,0,217,255))
                    else:
                        round_rect(fenetre, (partition2[i].posx,partition2[i].posy,19,partition2[i].time), pg.Color("blue"), 5,2,  (33,0,187,255))
                elif partition2[i].val == 0:
                    if partition2[i].nature == 'blanc':
                        round_rect(fenetre, (partition2[i].posx,partition2[i].posy,30,partition2[i].time), pg.Color("white"), 8,2,  (132,0,217,255))
                    else:
                        round_rect(fenetre, (partition2[i].posx,partition2[i].posy,19,partition2[i].time), pg.Color("white"), 5,2,  (33,0,187,255))
                
                #fenetre.blit(touches[i], (partition[i].posx, partition[i].posy))
        fenetre.blit(clavier, (0, fenetre.get_height()- clavier.get_height()))
        
        #write = "COUCOU %d s, score : %d,  : %d, test ; %d %d %d" % (int(c/100),osu, score, partition[0].val,partition[1].val,partition[2].val)
        write = "Compteur : %d Start : %d" % (c, start)
        #texte = font.render(write, 1, (0,0,0))
        texte = font.render(" ", 1, (0,0,0))
        fenetre.blit(texte, (0,0))
        
        #round_rect(fenetre, (500,250,44,200), pg.Color("black"), 10,3, (0,0,0,0))
        
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
    
    inp.close()
    pygame.display.quit()

if __name__ == "__main__":
    main2("test")