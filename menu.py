import os#pour recuperer les nom des fichiers
import pygame
from pygame.locals import *
from colorVarCalc import *
import pygame.midi
from pygame import gfxdraw
import subprocess

from main import *
from lecture_midi import *
from accomp import *
from mainDroite import *
from mainGauche import *

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

###fontion
def fadeIn(surf, image):
    for i in range(255):
        surf.fill((0,0,0))    
        image.set_alpha(i)
        surf.blit(image, (0,0))
        pygame.display.flip()
        
def fadeOut(surf, image):
    for i in range(255):
        surf.fill((0,0,0))    
        image.set_alpha(255-i)
        surf.blit(image, (0,0))
        pygame.display.flip()
        
def upImg(surf, image, back, disque):
    compteur = 0
    while compteur > -750:
        surf.fill((0,0,0)) 
        surf.blit(back, (0, 0))
        surf.blit(disque, (-590, -200))        
        surf.blit(image, (0, compteur))        
        pygame.time.delay(5)
        compteur-=10
        #pygame.display.flip()
        pygame.display.update()
        
def downImg(surf, image, back, disque):#a tester
    compteur = -750
    while compteur <0:
        surf.blit(back, (0, 0))
        surf.blit(disque, (-590, -200)) 
        surf.blit(image, (0, compteur))        
        pygame.time.delay(5)
        compteur+=10
        pygame.display.update()
def upImg2(surf, image, back, disque):#a tester
    compteur = 750
    while compteur > 0:
        surf.blit(back, (0, 0))
        surf.blit(disque, (-590, -200)) 
        surf.blit(image, (0, compteur))        
        pygame.time.delay(5)
        compteur-=10
        pygame.display.update()
        
def downImg2(surf, image, back, disque):#a tester
    compteur = 0
    while compteur <750:
        surf.blit(back, (0, 0))
        surf.blit(disque, (-590, -200)) 
        surf.blit(image, (0, compteur))        
        pygame.time.delay(5)
        compteur+=10
        pygame.display.update()
          
def blitRotate(surf, image, pos, originPos, angle):

    # calcaulate the axis aligned bounding box of the rotated image
    w, h       = image.get_size()
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot 
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)





#action
pygame.init()
pygame.midi.init()
pygame.font.init()
pygame.mixer.init()
#fenetre = pygame.display.set_mode((1470, 750), FULLSCREEN) #plein ecran
fenetre = pygame.display.set_mode((1470, 750))


###########################      Main ###################"

list_song =[]#creation d'une liste contenant le nom des fichier midi
for element in os.listdir('./fichier_midi'):#Mettre les fichiers midi dans ce fichier ou changer de repertoire
    #verification que ce soit bien un fichier midi
    if element.endswith('.mid'):
        list_song.append(element)#récupération des noms des fichiers
        


#theme
logo=pygame.image.load(str("theme/demarrage.png")).convert()

fond=pygame.image.load(str("theme/fond.png")).convert()
disk=pygame.image.load(str("theme/disk.png")).convert_alpha()

menu1=pygame.image.load(str("theme/menu1.png")).convert_alpha()
menu2=pygame.image.load(str("theme/menu2.png")).convert_alpha()

select= pygame.image.load(str("Images/white.png")).convert_alpha()


continuer =1
choix=1;

#Concernant l'affichage des musiques
font2=pygame.font.Font(None, 12)
font1=pygame.font.Font(None, 24)
font0=pygame.font.Font(None, 46)
font_base=pygame.font.Font(None, 56)
valeur_a=len(list_song)
valeur_a -=1


##apparittion du logo
fadeIn(fenetre, logo) 

pygame.time.delay(50)#attent
fenetre.blit(logo, (0,0))     
pygame.display.flip() 
  
##disparition du logo
fadeOut(fenetre, logo)


couleurMainG_H = vecColor(91,21,142)
couleurMainG_B = vecColor(33,83,188)
couleurMainD_H = vecColor(253, 70, 38)
couleurMainD_B = vecColor(237, 0, 0)

vec_couleur_gauche = computeVarColor(couleurMainG_H, couleurMainG_B, 400)
vec_couleur_droite = computeVarColor(couleurMainD_H, couleurMainD_B, 400)

visu_couleur = pygame.image.load(str("Images/terrain_menu.png")).convert()
piano_menu = pygame.image.load(str("Images/piano_menu.png")).convert()
cle_sol = pygame.image.load(str("Images/cle_sol.png")).convert_alpha()

fichier = open("prefs.txt", "r")
fic_content = fichier.readline()
content = fic_content.split(" ")

musique_selection=0
color_selec_mode = 0
cpt_gauche = 0
cpt_droite = 0
couleur_choisie_g = -1
couleur_choisie_d = -1

select_mode = 0

if len(content) == 15:
    cpt_gauche = int(content[1], 10)
    cpt_droite = int(content[8], 10)
    
if cpt_gauche > 0:
    couleur_choisie_g = cpt_gauche
if cpt_droite > 0:
    couleur_choisie_d = cpt_droite
    
while continuer:
    #print(musique_selection)
    if musique_selection==0:####Menu Principale
        fenetre.blit(fond, (0, 0))
        fenetre.blit(menu1,(0,0))
        fenetre.blit(disk, (-590,-200))
        if select_mode == 0:
            fenetre.blit(select,(590,155))
        elif select_mode == 1:
            fenetre.blit(select,(590,250))
        elif select_mode == 2:
            fenetre.blit(select,(590,345))
        elif select_mode == 3:
            fenetre.blit(select,(590,440))
                
                
                
    if musique_selection==1:####Menu de Selection
        fenetre.blit(fond, (0, 0))
        fenetre.blit(menu2,(0,0))
        fenetre.blit(disk, (-590,-200))

        affiche0= font0.render(str(list_song[choix])[:-4],1,(255, 255, 255))
            
        if choix+2>valeur_a:
            affichep_2= font2.render(" ",1,(0, 0, 0))
        else:            
            affichep_2= font2.render(str(list_song[choix+2])[:-4],1,(255, 255, 255))
        
        if choix+1>valeur_a:
            affichep_1= font1.render(" ",2,(0, 0, 0))
        else:
            affichep_1= font1.render(str(list_song[choix+1])[:-4],1,(255, 255, 255))
        
        if choix-2<0:
            affichem_2= font2.render(" ",3,(0, 0, 0))
        else:
            affichem_2= font2.render(str(list_song[choix-2])[:-4],1,(255, 255, 255))
        
        if choix-1<0:
            affichem_1= font1.render(" ",4,(0, 0, 0))
        else:
            affichem_1= font1.render(str(list_song[choix-1])[:-4],1,(255, 255, 255))        
    
        fenetre.blit(affichem_2, (830,180))
        fenetre.blit(affichem_1, (830,280))
        fenetre.blit(affiche0, (830,380))
        fenetre.blit(affichep_1, (830,480))
        fenetre.blit(affichep_2, (830,580))
        
    if musique_selection==3:####Menu de Selection
        fenetre.blit(fond, (0, 0))
        fenetre.blit(menu2,(0,0))
        fenetre.blit(disk, (-590,-200))

        affiche0= font0.render(str(list_song[choix])[:-4],1,(255, 255, 255))
            
        if choix+2>valeur_a:
            affichep_2= font2.render(" ",1,(0, 0, 0))
        else:            
            affichep_2= font2.render(str(list_song[choix+2])[:-4],1,(255, 255, 255))
        
        if choix+1>valeur_a:
            affichep_1= font1.render(" ",2,(0, 0, 0))
        else:
            affichep_1= font1.render(str(list_song[choix+1])[:-4],1,(255, 255, 255))
        
        if choix-2<0:
            affichem_2= font2.render(" ",3,(0, 0, 0))
        else:
            affichem_2= font2.render(str(list_song[choix-2])[:-4],1,(255, 255, 255))
        
        if choix-1<0:
            affichem_1= font1.render(" ",4,(0, 0, 0))
        else:
            affichem_1= font1.render(str(list_song[choix-1])[:-4],1,(255, 255, 255))        
    
        fenetre.blit(affichem_2, (830,180))
        fenetre.blit(affichem_1, (830,280))
        fenetre.blit(affiche0, (830,380))
        fenetre.blit(affichep_1, (830,480))
        fenetre.blit(affichep_2, (830,580))
        
    if musique_selection==2:####Menu Couleurs
        fenetre.blit(fond, (0, 0))
        fenetre.blit(disk, (-590,-200))
        
        if(color_selec_mode == 0):
            fenetre.blit(font0.render("Selectionner le theme",1,(255, 255, 255)), (720,200))
            
            fenetre.blit(font0.render("Espace",1,(255, 255, 255)), (720,300))
            fenetre.blit(font0.render("Feu",1,(255, 255, 255)), (720,400))
            fenetre.blit(font0.render("Sunset",1,(255, 255, 255)), (720,500))
            fenetre.blit(font0.render("Floral",1,(255, 255, 255)), (720,600))
            fenetre.blit(font0.render("Aqua",1,(255, 255, 255)), (720,700))
            
            fenetre.blit(font0.render("Espace",1,(255, 255, 255)), (1080,300))
            fenetre.blit(font0.render("Feu",1,(255, 255, 255)), (1080,400))
            fenetre.blit(font0.render("Sunset",1,(255, 255, 255)), (1080,500))
            fenetre.blit(font0.render("Floral",1,(255, 255, 255)), (1080,600))
            fenetre.blit(font0.render("Aqua",1,(255, 255, 255)), (1080,700))
            
            print(cpt_gauche, cpt_droite)
            
            if cpt_gauche == 0:
                fenetre.blit(cle_sol, (691,300))
                couleurMainG_H = vecColor(91,21,142)
                couleurMainG_B = vecColor(33,83,188)
                couleur_choisie_g = 0
            elif cpt_gauche == 1:
                fenetre.blit(cle_sol, (691,400))
                couleurMainG_H = vecColor(255, 150, 0)
                couleurMainG_B = vecColor(237, 0, 0)
                couleur_choisie_g = 1
            elif cpt_gauche == 2:
                fenetre.blit(cle_sol, (691,500))
                couleurMainG_H = vecColor(255,255,0)
                couleurMainG_B = vecColor(91,21,142)
                couleur_choisie_g = 2
            elif cpt_gauche == 3:
                fenetre.blit(cle_sol, (691,600))
                couleurMainG_H = vecColor(68, 170, 0)
                couleurMainG_B = vecColor(205, 135, 222)
                couleur_choisie_g = 3
            elif cpt_gauche == 4:
                fenetre.blit(cle_sol, (1051,700))
                couleurMainG_H = vecColor(21, 250, 211)
                couleurMainG_B = vecColor(0, 152, 193)
                couleur_choisie_g = 4
                
            if cpt_droite == 0:
                fenetre.blit(cle_sol, (1051,300))
                couleurMainD_H = vecColor(91,21,142)
                couleurMainD_B = vecColor(33,83,188)
                couleur_choisie_d = 0
            elif cpt_droite == 1:
                fenetre.blit(cle_sol, (1051,400))
                couleurMainD_H = vecColor(255, 234, 0)
                couleurMainD_B = vecColor(237, 0, 0)
                couleur_choisie_d = 1
            elif cpt_droite == 2:
                fenetre.blit(cle_sol, (1051,500))
                couleurMainD_H = vecColor(255,255,0)
                couleurMainD_B = vecColor(91,21,142)
                couleur_choisie_d = 2
            elif cpt_droite == 3:
                fenetre.blit(cle_sol, (1051,600))
                couleurMainD_H = vecColor(68, 170, 0)
                couleurMainD_B = vecColor(205, 135, 222)
                couleur_choisie_d = 3
            elif cpt_droite == 4:
                fenetre.blit(cle_sol, (691,700))
                couleurMainD_H = vecColor(21, 250, 211)
                couleurMainD_B = vecColor(0, 152, 193)
                couleur_choisie_d = 4
                
            vec_couleur_gauche = computeVarColor(couleurMainG_H, couleurMainG_B, 400)
            vec_couleur_droite = computeVarColor(couleurMainD_H, couleurMainD_B, 400)
                
        
        if(color_selec_mode == 1):
            #MGCHR = Main Gauche Couleur Haut Rouge 
            MGCHR = font1.render("R:  " + str(couleurMainG_H.R),1,(255, 255, 255))
            MGCHG = font1.render("G:  " + str(couleurMainG_H.G),1,(255, 255, 255))
            MGCHB = font1.render("B:  " + str(couleurMainG_H.B),1,(255, 255, 255))
            
            MGCBR = font1.render("R:  " + str(couleurMainG_B.R),1,(255, 255, 255))
            MGCBG = font1.render("G:  " + str(couleurMainG_B.G),1,(255, 255, 255))
            MGCBB = font1.render("B:  " + str(couleurMainG_B.B),1,(255, 255, 255))
            
            MDCHR = font1.render("R:  " + str(couleurMainD_H.R),1,(255, 255, 255))
            MDCHG = font1.render("G:  " + str(couleurMainD_H.G),1,(255, 255, 255))
            MDCHB = font1.render("B:  " + str(couleurMainD_H.B),1,(255, 255, 255))
            
            MDCBR = font1.render("R:  " + str(couleurMainD_B.R),1,(255, 255, 255))
            MDCBG = font1.render("G:  " + str(couleurMainD_B.G),1,(255, 255, 255))
            MDCBB = font1.render("B:  " + str(couleurMainD_B.B),1,(255, 255, 255))
            
            vec_couleur_gauche = computeVarColor(couleurMainG_H, couleurMainG_B, 400)
            vec_couleur_droite = computeVarColor(couleurMainD_H, couleurMainD_B, 400)
            
            fenetre.blit(font0.render("Main Gauche",1,(255, 255, 255)), (720,200))
            fenetre.blit(font0.render("Haut",1,(255, 255, 255)), (720,250))
            fenetre.blit(MGCHR, (720,300))
            fenetre.blit(MGCHG, (720,340))
            fenetre.blit(MGCHB, (720,380))
            
            fenetre.blit(font0.render("Bas",1,(255, 255, 255)), (720,430))
            fenetre.blit(MGCBR, (720,480))
            fenetre.blit(MGCBG, (720,530))
            fenetre.blit(MGCBB, (720,580))
            
            fenetre.blit(font0.render("Main Droite",1,(255, 255, 255)), (1080,200))
            fenetre.blit(font0.render("Haut",1,(255, 255, 255)), (1080,250))
            fenetre.blit(MDCHR, (1080,300))
            fenetre.blit(MDCHG, (1080,340))
            fenetre.blit(MDCHB, (1080,380))
            
            fenetre.blit(font0.render("Bas",1,(255, 255, 255)), (1080,430))
            fenetre.blit(MDCBR, (1080,480))
            fenetre.blit(MDCBG, (1080,530))
            fenetre.blit(MDCBB, (1080,580))
        
        fenetre.blit(visu_couleur, (0,0))
        
        #taille d'une touche : largeur 43, hauteur 132
        #Main gauche
        round_rect(fenetre, (0,0,43,132), pygame.Color("white"), 8,2,  (couleurMainG_H.R,couleurMainG_H.G,couleurMainG_H.B,255))
        round_rect(fenetre, (0,133,43,132), pygame.Color("white"), 8,2,  ((couleurMainG_H.R+150*vec_couleur_gauche.R)%256,(couleurMainG_H.G+150*vec_couleur_gauche.G)%256,(couleurMainG_H.B+150*vec_couleur_gauche.B)%256,255))
        round_rect(fenetre, (0,266,43,132), pygame.Color("white"), 8,2,  ((couleurMainG_H.R+300*vec_couleur_gauche.R)%256,(couleurMainG_H.G+300*vec_couleur_gauche.G)%256,(couleurMainG_H.B+300*vec_couleur_gauche.B)%256, 255))
        round_rect(fenetre, (0,398,43,132), pygame.Color("white"), 8,2,  (couleurMainG_B.R,couleurMainG_B.G,couleurMainG_B.B,255))
        
        #Main droite
        round_rect(fenetre, (301,0,43,132), pygame.Color("white"), 8,2,  (couleurMainD_H.R,couleurMainD_H.G,couleurMainD_H.B,255))
        round_rect(fenetre, (301,133,43,132), pygame.Color("white"), 8,2,  ((couleurMainD_H.R+150*vec_couleur_droite.R)%256,(couleurMainD_H.G+150*vec_couleur_droite.G)%256,(couleurMainD_H.B+150*vec_couleur_droite.B)%256,255))
        round_rect(fenetre, (301,266,43,132), pygame.Color("white"), 8,2,  ((couleurMainD_H.R+300*vec_couleur_droite.R)%256,(couleurMainD_H.G+300*vec_couleur_droite.G)%256,(couleurMainD_H.B+300*vec_couleur_droite.B)%256,255))
        round_rect(fenetre, (301,398,43,132), pygame.Color("white"), 8,2,  (couleurMainD_B.R,couleurMainD_B.G,couleurMainD_B.B,255))

        fenetre.blit(piano_menu, (0,529))


    
    for event in pygame.event.get():  
        if event.type == QUIT:     
            continuer = 0       
   
        if event.type == KEYDOWN:
            
            if musique_selection==0:####Menu Principal
#                if event.key == K_RETURN:#Retour
#                    continuer = 0 
                    
                    
                if event.key == K_SPACE and select_mode == 0:
                    upImg(fenetre, menu1, fond, disk)
                    for i in range(90):#tourne le disque
                        fenetre.blit(fond, (0, 0))
                        blitRotate(fenetre, disk, (0,393), (590,593),i*9)
                        pygame.display.flip()
                    upImg2(fenetre, menu2, fond, disk)
                    musique_selection=1
                    
                if event.key == K_SPACE and select_mode == 1:
                    upImg(fenetre, menu1, fond, disk)
                    for i in range(90):#tourne le disque
                        fenetre.blit(fond, (0, 0))
                        blitRotate(fenetre, disk, (0,393), (590,593),i*9)
                        pygame.display.flip()
                    upImg2(fenetre, menu2, fond, disk)
                    musique_selection=3
                    
                if event.key == K_SPACE and select_mode == 2:
                    upImg(fenetre, menu1, fond, disk)
                    for i in range(90):#tourne le disque
                        fenetre.blit(fond, (0, 0))
                        blitRotate(fenetre, disk, (0,393), (590,593),i*9)
                        pygame.display.flip()
                    upImg2(fenetre, menu2, fond, disk)
                    musique_selection=4
                    
                if event.key == K_SPACE and select_mode == 3:
                    upImg(fenetre, menu1, fond, disk)
                    for i in range(90):#tourne le disque
                        fenetre.blit(fond, (0, 0))
                        blitRotate(fenetre, disk, (0,393), (590,593),i*9)
                        pygame.display.flip()
                    upImg2(fenetre, menu2, fond, disk)
                    musique_selection=2
                    
                if event.key == K_UP:
                    select_mode-=1 
                    if select_mode < 0:
                        select_mode=3               
                    
                if event.key == K_DOWN:
                    select_mode+=1
                    if select_mode >= 4:
                        select_mode=0
                    
            if musique_selection==1:
                if event.key == K_RETURN:#Retour 
                    downImg2(fenetre, menu2, fond, disk)
                    for i in range(90):#tourne le disque
                        fenetre.blit(fond, (0, 0))
                        #blitRotate(fenetre, disk, (0,393), (590,593),i*-9)#rotation du disqe
                        pygame.display.flip()

                    downImg(fenetre, menu1, fond, disk)                    
                    musique_selection=0
                if event.key == K_DOWN:
                    #Haut
                    choix += 1
                    if choix==valeur_a+1:
                        choix -=1
                if event.key == K_UP:#Base
                    choix -= 1
                    if choix<0:
                        choix +=1
                if event.key == K_KP_ENTER:
                    print(str(list_song[choix]))
                    main3(str(list_song[choix]))
            
                    
            if musique_selection==3:####Menu de Selection
                                
                if event.key == K_RETURN:#Retour 
                    downImg2(fenetre, menu2, fond, disk)
                    for i in range(90):#tourne le disque
                        fenetre.blit(fond, (0, 0))
                        #blitRotate(fenetre, disk, (0,393), (590,593),i*-9)#rotation du disqe
                        pygame.display.flip()

                    downImg(fenetre, menu1, fond, disk)                    
                    musique_selection=0
                if event.key == K_DOWN: #Haut
                    choix += 1
                    if choix==valeur_a+1:
                        choix -=1
                if event.key == K_UP:#Base
                    choix -= 1
                    if choix<0:
                        choix +=1
                if event.key == K_KP_ENTER:#Jouer
                    print("yolo")
                    fichier = open("prefs.txt", "w")
                    fichier.write(str(list_song[choix]))
                    fichier.write(" ")
                    if couleur_choisie_g == 0:
                        fichier.write("0 ")
                        fichier.write("91 21 142 ")
                        fichier.write("33 83 188 ")
                    elif couleur_choisie_g == 1:
                        fichier.write("1 ")
                        fichier.write("255 150 0 ")
                        fichier.write("237 0 0 ")
                    elif couleur_choisie_g == 2:
                        fichier.write("2 ")
                        fichier.write("255 255 0 ")
                        fichier.write("91 21 142 ")
                    elif couleur_choisie_g == 3:
                        fichier.write("3 ")
                        fichier.write("68 170 0 ")
                        fichier.write("205 135 222 ")
                    elif couleur_choisie_g == 4:
                        fichier.write("4 ")
                        fichier.write("21 250 211 ")
                        fichier.write("0 152 193 ")
                        
                    if couleur_choisie_d == 0:
                        fichier.write("0 ")
                        fichier.write("91 21 142 ")
                        fichier.write("33 83 188 ")
                    elif couleur_choisie_d == 1:
                        fichier.write("1 ")
                        fichier.write("255 150 0 ")
                        fichier.write("237 0 0 ")
                    elif couleur_choisie_d == 2:
                        fichier.write("2 ")
                        fichier.write("255 255 0 ")
                        fichier.write("91 21 1²2 ")
                    elif couleur_choisie_d == 3:
                        fichier.write("3 ")
                        fichier.write("68 170 0 ")
                        fichier.write("205 135 222 ")
                    elif couleur_choisie_d == 4:
                        fichier.write("4 ")
                        fichier.write("21 250 211 ")
                        fichier.write("0 152 193 ")
                    fichier.close()
                    #subprocess.call("C:/Python32/python.exe","main.py", shell = True)
                    main("M")

            
            if musique_selection==2:####Menu Couleurs
                if event.key == K_RETURN:#Retour 
                    for i in range(90):#tourne le disque
                        fenetre.blit(fond, (0, 0))
                        pygame.display.flip()                  
                    musique_selection=0
                if event.key == K_RIGHT:
                    if color_selec_mode==0:
                        color_selec_mode = 1
                    elif color_selec_mode == 1:
                        color_selec_mode = 0
                
                if color_selec_mode == 0:
                    if event.key == K_d:
                        cpt_droite +=1
                        cpt_droite = cpt_droite%5
                    if event.key == K_g:
                        cpt_gauche +=1
                        cpt_gauche = cpt_gauche%5
                        
    

    pygame.display.flip()    
 
       
pygame.display.quit()


    
