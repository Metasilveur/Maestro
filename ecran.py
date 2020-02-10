import pygame
from colorVarCalc import *

class Ecran:
    def __init__(self, fclavier, f_mainD_toucheB, fmainD_toucheN, fmainG_toucheB, fmainG_toucheN, fterrain):
        self.font = pygame.font.SysFont("Arial", 30)
        self.fenetre = pygame.display.set_mode((1470, 750))
        self.clavier = pygame.image.load(fclavier).convert_alpha() 
        self.mainD_toucheB = pygame.image.load(f_mainD_toucheB).convert()
        self.mainD_toucheN = pygame.image.load(fmainD_toucheN).convert()
        self.mainG_toucheB = pygame.image.load(fmainG_toucheB).convert()
        self.mainG_toucheN = pygame.image.load(fmainG_toucheN).convert()
        self.terrain = pygame.image.load(fterrain).convert()
        self.active_Rectangle = pygame.Rect(0, 0, self.fenetre.get_width(), self.fenetre.get_height()- self.clavier.get_height())

    def placement_touches(self, partition):
        touches = []
        for obj in partition:
            if(int(obj.touche)%12 < 5):
                if((int(obj.touche)%12)%2 == 0):
                    touches.append(pygame.transform.scale(self.mainD_toucheB, (30,int(obj.time))))
                else:
                    touches.append(pygame.transform.scale(self.mainD_toucheN, (19,int(obj.time))))
            else:
                if((int(obj.touche)%12)%2 == 1):
                    touches.append(pygame.transform.scale(self.mainD_toucheB, (30,int(obj.time))))
                else:
                    touches.append(pygame.transform.scale(self.mainD_toucheN, (19,int(obj.time)))) 
        pygame.display.flip()
        return touches
    
    def blitter(self, touches_d, touches_g, partition_d, partition_g, taille_d, taille_g, cpt, colorvars, colorvars2):
        
        for i in range(int(taille_d/2)):
            if cpt>=partition_d[i].time_pos and partition_d[i].posy < self.fenetre.get_height()- self.clavier.get_height(): 
                if partition_d[i].posy < 100:
                    if partition_d[i].pressed == 1:
                        if partition_d[i].nature == 'blanc':
                            self.round_rect(self.fenetre, (partition_d[i].posx,partition_d[i].posy,30,partition_d[i].time), pygame.Color("white"), 8,2,  (91, 21, 142,255))
                        else:
                            self.round_rect(self.fenetre, (partition_d[i].posx,partition_d[i].posy,19,partition_d[i].time), pygame.Color("white"), 5,2,  (91, 21, 142,255))
                    else:
                        if partition_d[i].nature == 'blanc':
                            self.round_rect(self.fenetre, (partition_d[i].posx,partition_d[i].posy,30,partition_d[i].time), pygame.Color("white"), 8,2,  (91, 21, 142,255))
                        else:
                            self.round_rect(self.fenetre, (partition_d[i].posx,partition_d[i].posy,19,partition_d[i].time), pygame.Color("white"), 5,2,  (91, 21, 142,255))
                    
                elif partition_d[i].posy>=100 and partition_d[i].posy<500:
                    if partition_d[i].pressed == 1:
                        if partition_d[i].nature == 'blanc':
                            self.round_rect(self.fenetre, (partition_d[i].posx,partition_d[i].posy,30,partition_d[i].time), pygame.Color("white"), 8,2,  (91+partition_d[i].increment*colorvars.R, 21+partition_d[i].increment*colorvars.G, 142+partition_d[i].increment*colorvars.B,255))
                        else:
                            self.round_rect(self.fenetre, (partition_d[i].posx,partition_d[i].posy,19,partition_d[i].time), pygame.Color("white"), 5,2,  (91+partition_d[i].increment*colorvars.R, 21+partition_d[i].increment*colorvars.G, 142+partition_d[i].increment*colorvars.B,255))
                    else:
                        if partition_d[i].nature == 'blanc':
                            self.round_rect(self.fenetre, (partition_d[i].posx,partition_d[i].posy,30,partition_d[i].time), pygame.Color("white"), 8,2,  (91+partition_d[i].increment*colorvars.R, 21+partition_d[i].increment*colorvars.G, 142+partition_d[i].increment*colorvars.B,255))
                        else:
                            self.round_rect(self.fenetre, (partition_d[i].posx,partition_d[i].posy,19,partition_d[i].time), pygame.Color("white"), 5,2,  (91+partition_d[i].increment*colorvars.R, 21+partition_d[i].increment*colorvars.G, 142+partition_d[i].increment*colorvars.B,255))
                    partition_d[i].increment+=1
                else:
                    if partition_d[i].pressed == 1:
                        if partition_d[i].nature == 'blanc':
                            self.round_rect(self.fenetre, (partition_d[i].posx,partition_d[i].posy,30,partition_d[i].time), pygame.Color("white"), 8,2,  (33, 83, 188,255))
                        else:
                            self.round_rect(self.fenetre, (partition_d[i].posx,partition_d[i].posy,19,partition_d[i].time), pygame.Color("white"), 5,2,  (33, 83, 188,255))
                    else:
                        if partition_d[i].nature == 'blanc':
                            self.round_rect(self.fenetre, (partition_d[i].posx,partition_d[i].posy,30,partition_d[i].time), pygame.Color("white"), 8,2,  (33, 83, 188,255))
                        else:
                            self.round_rect(self.fenetre, (partition_d[i].posx,partition_d[i].posy,19,partition_d[i].time), pygame.Color("white"), 5,2,  (33, 83, 188,255))
                            
        for i in range(int(taille_g/2)):
            if cpt>=partition_g[i].time_pos and partition_g[i].posy < self.fenetre.get_height()- self.clavier.get_height(): 
                if partition_g[i].posy < 100:
                    if partition_g[i].pressed == 1:
                        if partition_g[i].nature == 'blanc':
                            self.round_rect(self.fenetre, (partition_g[i].posx,partition_g[i].posy,30,partition_g[i].time), pygame.Color("white"), 8,2,  (253, 70, 38,255))
                        else:
                            self.round_rect(self.fenetre, (partition_g[i].posx,partition_g[i].posy,19,partition_g[i].time), pygame.Color("white"), 5,2,  (253, 70, 38,255))
                    else:
                        if partition_g[i].nature == 'blanc':
                            self.round_rect(self.fenetre, (partition_g[i].posx,partition_g[i].posy,30,partition_g[i].time), pygame.Color("white"), 8,2,  (253, 70, 38,255))
                        else:
                            self.round_rect(self.fenetre, (partition_g[i].posx,partition_g[i].posy,19,partition_g[i].time), pygame.Color("white"), 5,2,  (253, 70, 38,255))
                    
                elif partition_g[i].posy>=100 and partition_g[i].posy<500:
                    if partition_g[i].pressed == 1:
                        if partition_g[i].nature == 'blanc':
                            self.round_rect(self.fenetre, (partition_g[i].posx,partition_g[i].posy,30,partition_g[i].time), pygame.Color("white"), 8,2,  (253+partition_g[i].increment*colorvars2.R, 70+partition_g[i].increment*colorvars2.G, 38+partition_g[i].increment*colorvars2.B,255))
                        else:
                            self.round_rect(self.fenetre, (partition_g[i].posx,partition_g[i].posy,19,partition_g[i].time), pygame.Color("white"), 5,2,  (253+partition_g[i].increment*colorvars2.R, 70+partition_g[i].increment*colorvars2.G, 38+partition_g[i].increment*colorvars2.B,255))
                    else:
                        if partition_g[i].nature == 'blanc':
                            self.round_rect(self.fenetre, (partition_g[i].posx,partition_g[i].posy,30,partition_g[i].time), pygame.Color("white"), 8,2,  (253+partition_g[i].increment*colorvars2.R, 70+partition_g[i].increment*colorvars2.G, 38+partition_g[i].increment*colorvars2.B,255))
                        else:
                            self.round_rect(self.fenetre, (partition_g[i].posx,partition_g[i].posy,19,partition_g[i].time), pygame.Color("white"), 5,2,  (253+partition_g[i].increment*colorvars2.R, 70+partition_g[i].increment*colorvars2.G, 38+partition_g[i].increment*colorvars2.B,255))
                    partition_g[i].increment+=1
                else:
                    if partition_g[i].pressed == 1:
                        if partition_g[i].nature == 'blanc':
                            self.round_rect(self.fenetre, (partition_g[i].posx,partition_g[i].posy,30,partition_g[i].time), pygame.Color("white"), 8,2,  (237, 0, 0,255))
                        else:
                            self.round_rect(self.fenetre, (partition_g[i].posx,partition_g[i].posy,19,partition_g[i].time), pygame.Color("white"), 5,2,  (237, 0, 0,255))
                    else:
                        if partition_g[i].nature == 'blanc':
                            self.round_rect(self.fenetre, (partition_g[i].posx,partition_g[i].posy,30,partition_g[i].time), pygame.Color("white"), 8,2,  (237, 0, 0,255))
                        else:
                            self.round_rect(self.fenetre, (partition_g[i].posx,partition_g[i].posy,19,partition_g[i].time), pygame.Color("white"), 5,2,  (237, 0, 0,255))
       
        self.fenetre.blit(self.clavier, (0, self.fenetre.get_height()- self.clavier.get_height()))
        
        pygame.display.update(self.active_Rectangle)
        
        for i in range(int(taille_d/2)):
            cropped = pygame.Surface([30, partition_d[i].time], pygame.SRCALPHA, 32)
            cropped.blit(self.terrain, (0,0), (partition_d[i].posx,partition_d[i].posy,30, partition_d[i].time))
            self.fenetre.blit(cropped, (partition_d[i].posx,partition_d[i].posy))
            
        for i in range(int(taille_g/2)):
            cropped = pygame.Surface([30, partition_g[i].time], pygame.SRCALPHA, 32)
            cropped.blit(self.terrain, (0,0), (partition_g[i].posx,partition_g[i].posy,30, partition_g[i].time))
            self.fenetre.blit(cropped, (partition_g[i].posx,partition_g[i].posy))
        
    def quit(self):
        pygame.display.quit()
        
    def render_region(self, image, rect, color, rad):
        """Helper function for round_rect."""
        corners = rect.inflate(-2*rad, -2*rad)
        for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
            pygame.draw.circle(image, color, getattr(corners,attribute), rad)
        image.fill(color, rect.inflate(-2*rad,0))
        image.fill(color, rect.inflate(0,-2*rad))

    def round_rect(self, surface, rect, color, rad=20, border=0, inside=(0,0,0,0)):
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
        self.render_region(image, zeroed_rect, color, rad)
        if border:
            zeroed_rect.inflate_ip(-2*border, -2*border)
            self.render_region(image, zeroed_rect, inside, rad)
        surface.blit(image, rect)
        