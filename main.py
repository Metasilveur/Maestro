import sys
import pygame
import pygame.midi
import statistics

from pygame.time import *

from midi_reader import Midi_Reader
from ecran import Ecran
from ecran import vecColor
from event import Event
from inputToMidi import InputToMidi
from colorVarCalc import *

 
def main(argv):
    pygame.init()
    pygame.midi.init()
    ecran_actif = Ecran("Images/piano.png", "Images/db.png", "Images/dn.png", "Images/gb.png", "Images/gn.png", "Images/terrain.png")
    py_event = Event(ecran_actif)
    
    fichier = open("prefs.txt", "r")
    fic_content = fichier.readline()
    content = fic_content.split()

    color1 = vecColor(91,21,142)
    color2 = vecColor(33,83,188)
    colorvars = computeVarColor(color1, color2, 400)

    color1 = vecColor(253, 70, 38)
    color2 = vecColor(237, 0, 0)
    colorvars2 = computeVarColor(color1, color2, 400)
    
    fichier.close()

    if len(content) == 15:

        color1 = vecColor(int(content[2], 10),int(content[3], 10),int(content[4], 10))
        color2 = vecColor(int(content[5], 10),int(content[6], 10),int(content[7], 10))
        colorvars = computeVarColor(color1, color2, 400)

        color1 = vecColor(int(content[9], 10),int(content[10], 10),int(content[11], 10))
        color2 = vecColor(int(content[12], 10),int(content[13], 10),int(content[14], 10))
        colorvars2 = computeVarColor(color1, color2, 400)
    
    if len(content) == 15:
        mdfl = 'Midi_Files/storm.mid'
    else:
        mdfl = 'fichier_midi/' + content[0]
        print(mdfl)
    readerTest = Midi_Reader(mdfl)
    readerTest.check_midi_file_struct();
    ecran_actif.fenetre.blit(ecran_actif.clavier, (0, ecran_actif.fenetre.get_height()- ecran_actif.clavier.get_height()))  

    partition_droite = readerTest.to_graphic_process(0)
    partition_gauche = readerTest.to_graphic_process(1)
    taille_droite = len(readerTest.conversion_droite)
    taille_gauche = len(readerTest.conversion_gauche)
    touches_droite = ecran_actif.placement_touches(partition_droite)
    touches_gauche = ecran_actif.placement_touches(partition_gauche)
    touches_actuelles = []
    clock = pygame.time.Clock()
    cpt = 0
    ecran_actif.fenetre.blit(ecran_actif.terrain, (0, 0))
    
    while py_event.continuer:
        cpt+=1
        py_event.getEvent(touches_actuelles, cpt)
        ecran_actif.blitter(touches_droite, touches_gauche, partition_droite, partition_gauche, taille_droite, taille_gauche, cpt, colorvars, colorvars2)
        touches_actuelles = py_event.validationTouche(taille_droite, taille_gauche, partition_droite, partition_gauche, touches_actuelles, cpt)
        
        clock.tick((125))
    
    if py_event.stats.tot!=0:
        print(statistics.mean(py_event.stats.prec))
    ecran_actif.quit()
    pygame.quit()
    
    pass
    

if __name__ == "__main__":
    main(sys.argv)