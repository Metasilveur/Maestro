import pygame
from pygame.time import *
from pygame.locals import *
from test_temps import Time_Manager
from stats import stats
import sys

class Event:
    def __init__(self, ecran):
        self.continuer = 1
        if pygame.midi.get_default_input_id() > 0:
            self.inp = pygame.midi.Input(1)
        else:
            print("Pas de clavier detecte!")
            pygame.quit()
            sys.exit()
            
        #self.inp = pygame.midi.Input(1)
        self.touches_app = []
        self.mEcran = ecran
        self.touches_curr_memory = []
        self.stats = stats(0, 0, 0, 0)
        
    #retourne tableau des touches appuyées et relachées
    def compteurElts(self):
        vals = []
        for tchs in self.touches_app:
            for tchs2 in self.touches_app:
                if tchs.touche_press == tchs2.touche_press:
                    if tchs.time_start != tchs2.time_start:
                        vals.append(tchs)
                        vals.append(tchs2)
                        if tchs in self.touches_app:
                            self.touches_app.remove(tchs)
                        if tchs2 in self.touches_app:
                            self.touches_app.remove(tchs2)
                        
        if len(vals)>0:
            return vals
        else:
            vals.append(Time_Manager(-1, -1))
            vals.append(Time_Manager(-1, -1))
            return vals
        
    def getEvent(self, touches_actuelles, cpt):
        if self.inp.poll():
            
            for items in self.inp.read(1000):
                midi_value = items[0][0:3]
                self.touches_app.append(Time_Manager(midi_value[0], midi_value[1], midi_value[2], cpt)) 
                print('input : ', midi_value[0], midi_value[1], midi_value[2],  pygame.time.get_ticks())
                
        for event in pygame.event.get():  
            if event.type == QUIT:     
                self.continuer = 0
    
    
        
    def validationTouche(self, taille_d, taille_g, partition_d, partition_g, touches_actuelles, cpt):
        for i in range(int(taille_d/2)):
            if cpt>=partition_d[i].time_pos:
                partition_d[i].posy+=1
                
        for i in range(int(taille_d/2)):
            if partition_d[i].posy<self.mEcran.fenetre.get_height()- self.mEcran.clavier.get_height() and partition_d[i].posy+int(partition_d[i].time)>=self.mEcran.fenetre.get_height()- self.mEcran.clavier.get_height() and partition_d[i].pressed == 0:
                partition_d[i].px_appui = cpt
                partition_d[i].px_relache = partition_d[i].px_appui + partition_d[i].time
                partition_d[i].pressed =1
                touches_actuelles.append(partition_d[i])
            elif partition_d[i].posy>=self.mEcran.fenetre.get_height()- self.mEcran.clavier.get_height() :
                if partition_d[i] in touches_actuelles:
                    touches_actuelles.remove(partition_d[i])
        
        for i in range(int(taille_g/2)):
            if cpt>=partition_g[i].time_pos:
                partition_g[i].posy+=1
                
        for i in range(int(taille_g/2)):
            if partition_g[i].posy<self.mEcran.fenetre.get_height()- self.mEcran.clavier.get_height() and partition_g[i].posy+int(partition_g[i].time)>=self.mEcran.fenetre.get_height()- self.mEcran.clavier.get_height() and partition_g[i].pressed == 0:
                partition_g[i].px_appui = cpt
                partition_g[i].px_relache = partition_g[i].px_appui + partition_g[i].time
                partition_g[i].pressed =1
                touches_actuelles.append(partition_g[i])
            elif partition_g[i].posy>=self.mEcran.fenetre.get_height()- self.mEcran.clavier.get_height() :
                if partition_g[i] in touches_actuelles:
                    touches_actuelles.remove(partition_g[i])
                    
        verif_cpt = 0
        
        for item in self.touches_app:
            if item.velocity != 0:
                verif_cpt += 1
            elif item.velocity == 0:
                verif_cpt-=1
            else:
                print('touche_app error')
        
        if verif_cpt == 0:
            touches = self.compteurElts()
            for cpt in range(len(touches)-1):
                if cpt%2==0:
                    if(touches[cpt].touche_press != -1):
                        delay_pressed = touches[cpt+1].time_start - touches[cpt].time_start
                        if delay_pressed<0:
                            delay_pressed*=-1
                            print('a', touches[cpt+1].touche_press, touches[cpt].touche_press, touches[cpt+1].time_start, touches[cpt].time_start)
                            self.calc_Pourcentage_Reussite(touches[cpt+1], touches[cpt], delay_pressed)
                        else:
                            print('b', touches[cpt].touche_press, touches[cpt+1].touche_press, touches[cpt].time_start, touches[cpt+1].time_start)
                            self.calc_Pourcentage_Reussite(touches[cpt], touches[cpt+1], delay_pressed)
            self.touches_curr_memory.clear()
        else:
            for item in touches_actuelles:
                if item not in self.touches_curr_memory:
                    self.touches_curr_memory.append(item)
                         
        return touches_actuelles    
    
    def calc_Pourcentage_Reussite(self, app_start, app_end, delay_pressed):
        prec = 0
        
        for touche in self.touches_curr_memory:
            if touche.touche == app_start.touche_press:
                if touche.px_appui <= app_start.time_start and touche.px_relache >= app_end.time_start:
                    prec = (delay_pressed/(touche.px_relache - touche.px_appui)) * 100
                    if abs(touche.px_appui - app_start.time_start) > 10:
                        self.stats.tard += 1
                elif touche.px_appui > app_start.time_start and touche.px_relache > app_end.time_start:
                    prec = ((app_end.time_start - touche.px_appui)/(touche.px_relache - touche.px_appui)) * 100
                    if abs(touche.px_appui - app_start.time_start) > 10:
                        self.stats.tot += 1
                elif touche.px_appui <= app_start.time_start and touche.px_relache < app_end.time_start:
                    prec = ((touche.px_relache - app_start.time_start)/(touche.px_relache - touche.px_appui)) * 100 
                    if abs(touche.px_appui - app_start.time_start) > 10:
                        self.stats.tard += 1
                elif touche.px_appui > app_start.time_start and touche.px_relache < app_end.time_start:
                    prec = 0
                    if abs(touche.px_appui - app_start.time_start) > 10:
                        self.stats.tot += 1
                print(touche.touche,' -> ', prec)
                print('-------------------------------------')
                self.stats.prec.append(prec)
                if prec >= 80:
                    self.stats.reussi += 1
                if prec < 40:
                    self.stats.rate += 1
                return prec
            else:
                prec = -1
        return prec