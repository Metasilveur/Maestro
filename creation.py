import os#pour recuperer les nom des fichiers
import pygame
from pygame.locals import *
from colorVarCalc import *
import pygame.midi
from pygame import gfxdraw
import subprocess
import time
import mido
import random
from mido import MidiFile, Message, MidiTrack, MetaMessage

pygame.midi.init()
midiOut = pygame.midi.Output(0)
mid = MidiFile(ticks_per_beat=96)
track = MidiTrack()
mid.tracks.append(track)
bpm = 60

#track.append(Message('program_change', program=12, time=0))

'''
print(mido.get_input_names())
mido.open_input('CASIO USB-MIDI 0')
'''

inport = mido.open_input('' + (mido.get_input_names()[0]))

def octave(i):
    if (i < 12):
        return 0
    elif (i < 24):
        return 1
    elif (i < 36):
        return 2
    elif (i < 48):
        return 3
    elif (i < 60):
        return 4
    elif (i < 72):
        return 5
    elif (i < 84):
        return 6
    elif (i < 96):
        return 7
    elif (i < 108):
        return 8
    elif (i < 120):
        return 9
    else:
        return 10

start = time.time()
acc = 0
tm = []
chord = ["", "", ""]
nt = ""
int_nt = 0

chords = ["", "", ""]
nb_c = 0

sorted_chord = [0, 0, 0]

existing_notes = ["C ", "C#", "D ", "Eb", "E ", "F ", "F#", "G ", "G#", "A ", "Bb", "B "]
colors = ["white", "red", "blue", "green", "cyan", "magenta", "yellow"]
color1 = ""
color2 = ""

gamme_t = 0 #Flag de gamme trouvée
gammes = ["","","","","","",""]
gammes_ecarts = [0,2,4,5,7,9,11]

gamme_def = ""
current_chord = ""

choix = ["", ""]

def gamme_finder(note):
    global gammes
    global gammes_ecarts
    for i in range(7):
        gammes[i] = note_namer(note_denamer(note) + gammes_ecarts[i])
        if (i == 0) or (i == 3) or (i == 4):
            gammes[i] = gammes[i][:2] + "maj"
        elif (i == 1) or (i == 2) or (i == 5):
            gammes[i] = gammes[i][:2] + "min"
        else:
            gammes[i] = gammes[i][:2] + "dim"
        gammes[i] = gammes[i].replace(" ", "")

def note_namer(i):
    if (i % 12 == 0):
        n = "C " + str(octave(i))
    elif (i % 12 == 1):
        n = "C#" + str(octave(i))
    elif (i % 12 == 2):
        n = "D " + str(octave(i))
    elif (i % 12 == 3):
        n = "Eb" + str(octave(i))
    elif (i % 12 == 4):
        n = "E " + str(octave(i))
    elif (i % 12 == 5):
        n = "F " + str(octave(i))
    elif (i % 12 == 6):
        n = "F#" + str(octave(i))
    elif (i % 12 == 7):
        n = "G " + str(octave(i))
    elif (i % 12 == 8):
        n = "G#" + str(octave(i))
    elif (i % 12 == 9):
        n = "A " + str(octave(i))
    elif (i % 12 == 10):
        n = "Bb" + str(octave(i))
    elif (i % 12 == 11):
        n = "B " + str(octave(i))
    return n

def note_denamer(s):
    if (s == "C#"):
        n = 1
    elif (s[:1] == "C"):
        n = 0
    elif (s[:1] == "D"):
        n = 2
    elif (s == "Eb"):
        n = 3
    elif (s[:1] == "E"):
        n = 4
    elif (s == "F#"):
        n = 6
    elif (s[:1] == "F"):
        n = 5
    elif (s == "G#"):
        n = 8
    elif (s[:1] == "G"):
        n = 7
    elif (s[:1] == "A"):
        n = 9
    elif (s == "Bb"):
        n = 10
    elif (s[:1] == "B"):
        n = 11
    else:
        print("FAIL")
        return 0
    return n

def chord_definer(ch, s_ch):
    chd = ""
    if (s_ch[1] - s_ch[0] == 4) and (s_ch[2] - s_ch[1] == 3):
        chd = (ch[0])[:-1] + " maj"
    elif (s_ch[1] - s_ch[0] == 3) and (s_ch[2] - s_ch[1] == 4):
        chd = (ch[0])[:-1] + " min"
    elif (s_ch[1] - s_ch[0] == 3) and (s_ch[2] - s_ch[1] == 3):
        chd = (ch[0])[:-1] + " dim"
    elif (s_ch[1] - s_ch[0] == 3) and (s_ch[2] - s_ch[1] == 5):
        chd = (ch[2])[:-1] + " maj"
    elif (s_ch[1] - s_ch[0] == 4) and (s_ch[2] - s_ch[1] == 5):
        chd = (ch[2])[:-1] + " min"
    elif (s_ch[1] - s_ch[0] == 3) and (s_ch[2] - s_ch[1] == 6):
        chd = (ch[2])[:-1] + " dim"
    elif (s_ch[1] - s_ch[0] == 5) and (s_ch[2] - s_ch[1] == 4):
        chd = (ch[1])[:-1] + "maj"
    elif (s_ch[1] - s_ch[0] == 5) and (s_ch[2] - s_ch[1] == 3):
        chd = (ch[1])[:-1] + " min"
    elif (s_ch[1] - s_ch[0] == 6) and (s_ch[2] - s_ch[1] == 3):
        chd = (ch[1])[:-1] + " dim"
    return chd

def nashville():
    s = 0
    global nb_c
    global chords
    global gammes
    
    if ((chords[0])[-3:] == "dim"): # Si l'accord est diminué, g+1
        s = (chords[0])[:2]
        gam = note_namer(note_denamer(s) + 1)[:-1]
    elif ((chords[2])[-3:] != "") and ((chords[1])[-3:] != "") and ((chords[0])[-3:] != ""):
        for exst_n in existing_notes:
            gamme_finder(exst_n)
            if ((chords[0].replace(" ","") in gammes) and (chords[1].replace(" ","") in gammes) and (chords[2].replace(" ","") in gammes)):
                gam = gammes[0][:-3]
                return gam
        print("Aucune gamme trouvee, veuillez recommencer")
        chords = ["", "", ""]
        nb_c = 0
        return ""
    elif ((chords[0])[-3:] == "min") and ((chords[1])[-3:] == "maj"):
        if ((note_namer(note_denamer(chords[0][:2]) + 1))[:2] == chords[1][:2]):
            s = (chords[0])[:2]
            gam = note_namer(note_denamer(s) + 8)[:-1]
        else:
            return ""
    elif ((chords[0])[-3:] == "maj") and ((chords[1])[-3:] == "min"):
        if ((note_namer(note_denamer(chords[1][:2]) + 1))[:2] == chords[0][:2]):
            s = (chords[0])[:2]
            gam = note_namer(note_denamer(s) + 7)[:-1]
        else:
            return ""
    elif ((chords[1])[-3:] == "maj") and ((chords[0])[-3:] == "maj"):
        if ((note_namer(note_denamer(chords[0][:2]) + 2))[:2] == chords[1][:2]):
            s = (chords[0])[:2]
            gam = note_namer(note_denamer(s) + 7)[:-1]
        elif ((note_namer(note_denamer(chords[1][:2]) + 2))[:2] == chords[0][:2]):
            s = (chords[0])[:2]
            gam = note_namer(note_denamer(s) + 5)[:-1]
        else:
            return ""
    elif ((chords[1])[-3:] == "min") and ((chords[0])[-3:] == "min"):
        if ((note_namer(note_denamer(chords[0][:2]) + 2))[:2] == chords[1][:2]):
            s = (chords[0])[:2]
            gam = note_namer(note_denamer(s) + 10)[:-1]
        elif ((note_namer(note_denamer(chords[1][:2]) + 2))[:2] == chords[0][:2]):
            s = (chords[0])[:2]
            gam = note_namer(note_denamer(s) + 8)[:-1]
        else:
            return ""
    elif ((chords[0])[-3:] == "maj"):
        return ""
    elif ((chords[0])[-3:] == "min"):
        return ""
    else:
        chords = ["", "", ""]
        nb_c = 0
        return ""
    gamme_finder(gam)
    return gam

def leds():
    global choix
    if (choix != ["", ""]):
        n1 = note_denamer(choix[0][:-3]) + 36
        if (choix[0][-3:] == "maj"):
            n2 = note_denamer(choix[0][:-3]) + 36 + 4
            n3 = note_denamer(choix[0][:-3]) + 36 + 7
        elif (choix[0][-3:] == "min"):
            n2 = note_denamer(choix[0][:-3]) + 36 + 3
            n3 = note_denamer(choix[0][:-3]) + 36 + 7
        elif (choix[0][-3:] == "dim"):
            n2 = note_denamer(choix[0][:-3]) + 36 + 3
            n3 = note_denamer(choix[0][:-3]) + 36 + 6
        
        n4 = note_denamer(choix[1][:-3]) + 36
        if (choix[1][-3:] == "maj"):
            n5 = note_denamer(choix[1][:-3]) + 36 + 4
            n6 = note_denamer(choix[1][:-3]) + 36 + 7
        elif (choix[1][-3:] == "min"):
            n5 = note_denamer(choix[1][:-3]) + 36 + 3
            n6 = note_denamer(choix[1][:-3]) + 36 + 7
        elif (choix[1][-3:] == "dim"):
            n5 = note_denamer(choix[1][:-3]) + 36 + 3
            n6 = note_denamer(choix[1][:-3]) + 36 + 6
    print(str(n1) + " " + str(n2) + " " + str(n3) + " / " + str(n4) + " " + str(n5) + " " + str(n6))

def T9(gams, current_chd):
    global choix
    if (current_chd in choix):
        rnd = random.choice(gams)
        for i in range(2): #On fait clignoter les leds
            while (rnd in choix) or (rnd == current_chd):
                rnd = random.choice(gams)
            choix[i] = rnd
        print(choix)
        leds()

###fontion
def _render_region(image, rect, color, rad):
    """Helper function for round_rect."""
    corners = rect.inflate(-2*rad, -2*rad)
    for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
        pygame.draw.circle(image, color, getattr(corners,attribute), rad)
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
    rect = pygame.Rect(rect)
    zeroed_rect = rect.copy()
    zeroed_rect.topleft = 0,0
    image = pygame.Surface(rect.size).convert_alpha()
    image.fill((0,0,0,0))
    _render_region(image, zeroed_rect, color, rad)
    if border:
        zeroed_rect.inflate_ip(-2*border, -2*border)
        _render_region(image, zeroed_rect, inside, rad)
    surface.blit(image, rect)


#Partie Graphique:

#action
pygame.init()
pygame.midi.init()
pygame.font.init()
pygame.mixer.init()
#fenetre = pygame.display.set_mode((1470, 750), FULLSCREEN) #plein ecran
fenetre = pygame.display.set_mode((1470, 750))

#image
fond=pygame.image.load(str("theme/brick.png")).convert()
piano=pygame.image.load(str("Images/piano.png")).convert()


font_base=pygame.font.Font("Signatra.ttf", 60)
font_base2=pygame.font.Font("Signatra.ttf", 40)
continuer =1

current_note = ""

while continuer:
    for msg in inport.iter_pending():
        #print(msg)
        #print("Acc = " + str(acc))
        #if (msg.type == 'note_on' and msg.velocity > 0 and (len(tm) < 4)):
        if (msg.type == 'note_on'):
            midiOut.note_on(msg.note,127)
        if (msg.type == 'note_on' and (len(tm) < 4)):
            tm.append(time.time() - start)
            #print("Longueur tm = " + str(len(tm)))
            
            int_nt = msg.note
            sorted_chord[acc] = int_nt
            current_note = note_namer(int_nt).replace(" ","")
            
            #gamme_finder(note_namer(int_nt)[:2])
            #print(gammes)
            
            start = time.time()
            
            if (acc == 2):
                acc = -1
                if (tm[1] + tm[2] < 0.15):
                    #print("Accord = " + chord[0] + ", " + chord[1] + ", " + chord[2])
                    sorted_chord.sort()
                    #print(str(sorted_chord[0]) + str(sorted_chord[1]) + str(sorted_chord[2]))
                    chord[0] = note_namer(sorted_chord[0])
                    chord[1] = note_namer(sorted_chord[1])
                    chord[2] = note_namer(sorted_chord[2])
                    #print(chord[0] + chord[1] + chord[2])
                    
                    current_chord = chord_definer(chord, sorted_chord)
                    
                    if (chord_definer(chord, sorted_chord) != "") and (gamme_t == 0):
                        print((chord_definer(chord, sorted_chord)).replace(" ",""))
                        chords[nb_c] = chord_definer(chord, sorted_chord)
                        nb_c = nb_c + 1
                        
                        gamme_def = nashville()
                        
                        if (gamme_def == ""):
                            print("On place l'accord dans une case...")
                        else:
                            gamme_t = 1
                            print("Gamme de " + gamme_def)
                            print("On allume les leds correspondantes :)")
                            print("On propose des accords au joueur")
                            current_chord = ""
                        
                    if (nb_c == 3):
                        nb_c = 0
                        
                    if (gamme_t == 1):
                        print(current_chord.replace(" ",""))
                        T9(gammes, current_chord.replace(" ",""))
                              
            acc = acc + 1
            
        #elif (msg.velocity == 0):
        elif (msg.type == 'note_off'):
            midiOut.note_off(msg.note,127)
            if (note_denamer(current_note[:2]) == msg.note % 12):
                current_note = ""
            if (acc > 0):
                acc = acc - 1
            if (acc == -1):
                acc = 0
            if (tm):
                tm.pop()
    
        if (msg.note == 120 and msg.type == 'note_on'):
            print("EXIT")
            
        if (msg.note == 119 and msg.type == 'note_on'):
            gamme_t = 0
            nb_c = 0
            chords = ["", "", ""]
            choix = ["", ""]
        
    #Fond
    fenetre.blit(fond, (0, 0))
    fenetre.blit(piano, (0, 600))
    
    #Rectangle
    for j in range(7):
        if (gammes[j] == choix[0]):
            round_rect(fenetre, (290,435,28,28), pygame.Color("black"), 8,2,  pygame.Color(colors[j]))#couleur propo 1
        if (gammes[j] == choix[1]):
            round_rect(fenetre, (815,435,28,28), pygame.Color("black"), 8,2,  pygame.Color(colors[j]))#couleur propo 2
    
    round_rect(fenetre, (0,535,177,65), pygame.Color("black"), 8,2,  pygame.Color("white"))#gamme de ?    
    round_rect(fenetre, (1360,535,110,65), pygame.Color("black"), 8,2,  pygame.Color("white"))#note actuel    
    round_rect(fenetre, (650,535,200,65), pygame.Color("black"), 8,2,  pygame.Color("white"))#accord    
    round_rect(fenetre, (325,430,325,85), pygame.Color("black"), 8,2,  pygame.Color("white"))#proposition 1      
    round_rect(fenetre, (850,430,325,85), pygame.Color("black"), 8,2,  pygame.Color("white"))#proposition 2
    
    #Texte
    affiche_note = font_base2.render(current_note,1,pygame.Color("red"))
    affiche_acc = font_base2.render(current_chord.replace(" ",""),1,pygame.Color("red"))    
    if (gamme_t != 1):
        affiche_gamme = font_base2.render(" Recherche...",1,pygame.Color("black"))
        affiche_acc1 = font_base.render(chords[0].replace(" ",""),1,pygame.Color("black"))    
        affiche_acc2 = font_base.render(chords[1].replace(" ",""),1,pygame.Color("black"))  
    else:
        affiche_gamme = font_base2.render("Gamme de " + gamme_def,1,pygame.Color("black"))
        affiche_acc1 = font_base.render(choix[0].replace(" ",""),1,pygame.Color("black"))    
        affiche_acc2 = font_base.render(choix[1].replace(" ",""),1,pygame.Color("black"))
        
    #Placement 
    fenetre.blit(affiche_gamme, (15,550))
    fenetre.blit(affiche_note, (1390,550))
    fenetre.blit(affiche_acc, (715,550))
    fenetre.blit(affiche_acc1, (440,440))    
    fenetre.blit(affiche_acc2, (965,440))
#ajoute 10    
#retire 10    
    for event in pygame.event.get():  
        if event.type == QUIT:     
            continuer = 0 
            inport.close()
            midiOut.close()
            
    pygame.display.flip()
    
       
pygame.display.quit()