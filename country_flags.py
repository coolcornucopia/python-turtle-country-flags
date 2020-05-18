# Liens internet vers la description des drapeaux du monde
# https://fr.wikipedia.org/wiki/Galerie_des_drapeaux_des_pays_du_monde
# https://fr.wikipedia.org/wiki/Liste_des_drapeaux_nationaux_par_proportions

from turtle import *

# Pour trier les chaines de caractères sans les accents
# cf strip_accents()
import unicodedata


### LES FONCTIONS POUR DESSINER DES FORMES SIMPLES ###

# Cette fonction sert à se déplacer et à mettre
# l'orientation par défaut
def prepare_dessin(x, y):
    penup()
    goto(x, y)
    # On met l'orientation par défaut vers la droite
    # En mode standard, 0=est 90=nord 180=ouest 270=sud
    # En mode logo, 0=nord 90=est 180=sud 270=ouest
    # ici nous considérons que nous sommes en mode standard
    setheading(0)
    pendown()

def rectangle(x, y, longueur, hauteur):
    prepare_dessin(x, y)
    forward(longueur)
    right(90)
    forward(hauteur)
    right(90)
    forward(longueur)
    right(90)
    forward(hauteur)

def rectangle_plein(x, y, longueur, hauteur):
    begin_fill()
    rectangle(x, y, longueur, hauteur)
    end_fill()

def carre(x, y, longueur):
    rectangle(x, y, longueur, longueur)

def carre_plein(x, y, longueur):
    rectangle_plein(x, y, longueur, longueur)

# On utilise le diamètre plutot que le rayon
# car on sait plus facilement comment faire
# se toucher deux objets (on évite le x2)
def cercle(centre_x, centre_y, diametre):
    # on recentre le cercle
    prepare_dessin(centre_x, centre_y - diametre / 2)
    circle(diametre / 2)

def cercle_plein(centre_x, centre_y, diametre):
    begin_fill()
    cercle(centre_x, centre_y, diametre)
    end_fill()


# La croix est inscrite à l'intérieur d'un cercle de
# diamètre "longueur"
def croix(centre_x, centre_y, longueur):
    # On bouge à gauche de la croix et on trace
    prepare_dessin(centre_x - (longueur / 2), centre_y)
    forward(longueur)
    # On bouge en haut de la croix et on trace
    prepare_dessin(centre_x, centre_y + (longueur / 2))
    right(90)
    forward(longueur)

# L'étoile est "débout" avec les "bras" ouverts à
# l'horizontal et une envergure de "longueur"
# La fonction renvoie le rectangle contenant
# exactement l'étoile, pratique pour les aligner :-)
# L'algo ci-dessous est une version adaptée de
# https://stackoverflow.com/questions/26356543/turtle-graphics-draw-a-star
def etoile_5_branches(centre_x, centre_y, longueur):
    # https://rechneronline.de/pi/pentagon.php
    # d = longueur
    # a = côté du pentagone = 0,618 * d
    # h = hauteur = 0,951 * d
    # ri = rayon cercle inscrit = 0,425 * d
    # rc = rayon cercle circonscrit = 0,526 * d
    d = longueur
    h = 0.951 * d
    rc = 0.526 * d

    # par défaut 144 pour une étoile "droite", si on met une
    # autre valeur, l'étoile sera + ou - "pointue"
    angle = 144
    branche = d / 2.6
    prepare_dessin(centre_x + d / 2 - branche, centre_y + d / 6)

    for i in range(5):
        forward(branche)
        right(angle)
        forward(branche)
        right(72 - angle)

    # rectangle autour
    # rectangle(centre_x - d / 2, centre_y + rc, d, h)
    # cercle circonscrit
    # cercle(centre_x, centre_y, rc * 2)

    # Retourne les coordonnées et tailles du rectangle autour
    # cela peut être utile pour coller parfaitement des étoiles
    # les unes aux autres
    return centre_x - d / 2, centre_y + rc, d, h

# (lire la description dans etoile_5_branches au dessus)
def etoile_pleine_5_branches(centre_x, centre_y, longueur):
    begin_fill()
    x, y, l, h = etoile_5_branches(centre_x, centre_y, longueur)
    end_fill()
    return x, y, l, h

# ANCIENNE version, non utilisée car pb de remplissage
def etoile_5_branches2(centre_x, centre_y, longueur):
    # https://rechneronline.de/pi/pentagon.php
    # d = longueur
    # a = côté du pentagone = 0,618 * d
    # h = hauteur = 0,951 * d
    # ri = rayon cercle inscrit = 0,425 * d
    # rc = rayon cercle circonscrit = 0,526 * d
    d = longueur
    h = 0.951 * d
    rc = 0.526 * d

    prepare_dessin(centre_x - d / 2, centre_y + d / 6)
    for i in range(5):
        forward(d)
        right(144)

    # rectangle autour
    # rectangle(centre_x - d / 2, centre_y + rc, d, h)
    # cercle circonscrit
    # cercle(centre_x, centre_y, rc * 2)

    # Retourne les coordonnées et tailles du rectangle autour
    # cela peut être utile pour coller parfaitement des étoiles
    # les unes aux autres
    return centre_x - d / 2, centre_y + rc, d, h



### LES FONCTIONS POUR AIDER A DESSINER LES DRAPEAUX ###
def rectangle_3_bandes_verticales(x, y, longueur, hauteur,
                                  couleur1, couleur2, couleur3):
    l = longueur / 3
    color(couleur1, couleur1)
    rectangle_plein(x, y, l, hauteur)
    color(couleur2, couleur2)
    rectangle_plein(x + l, y, l, hauteur)
    color(couleur3, couleur3)
    rectangle_plein(x + 2 * l, y, l, hauteur)
    # On trace maintenant le contour
    color(contour_drapeau)
    rectangle(x, y, longueur, hauteur)

def rectangle_3_bandes_horizontales(x, y, longueur, hauteur,
                                    couleur1, couleur2, couleur3):
    h = hauteur / 3
    color(couleur1, couleur1)
    rectangle_plein(x, y, longueur, h)
    color(couleur2, couleur2)
    rectangle_plein(x, y - h, longueur, h)
    color(couleur3, couleur3)
    rectangle_plein(x, y - 2 * h, longueur, h)
    # On trace maintenant le contour
    color(contour_drapeau)
    rectangle(x, y, longueur, hauteur)

def rectangle_cercle(rect_x, rect_y, longueur, hauteur,
                     cerc_x, cerc_y, diametre,
                     rect_couleur, cerc_couleur):
    color(rect_couleur, rect_couleur)
    rectangle_plein(rect_x, rect_y, longueur, hauteur)
    color(cerc_couleur, cerc_couleur)
    cercle_plein(cerc_x, cerc_y, diametre)
    # On trace maintenant le contour
    color(contour_drapeau)
    rectangle(rect_x, rect_y, longueur, hauteur)

### LES FONCTIONS POUR DESSINER LES DRAPEAUX ###
# Avec ces fonctions, on n'est pas obligé de respecter
# les proportions (ça peut être pratique parfois)
def drapeau_allemagne(x, y, longueur, hauteur):
    rectangle_3_bandes_horizontales(x, y, longueur, hauteur,
                                    '#000', '#D00', '#FFCE00')

def drapeau_armenie(x, y, longueur, hauteur):
    rectangle_3_bandes_horizontales(x, y, longueur, hauteur,
                                    '#D90012', '#0033A0', '#F2A800')

def drapeau_autriche(x, y, longueur, hauteur):
    rectangle_3_bandes_horizontales(x, y, longueur, hauteur,
                                    '#ED2939', 'white', '#ED2939')

def drapeau_bangladesh(x, y, longueur, hauteur):
    rectangle_cercle(x, y, longueur, hauteur,
                     x + longueur * 450/1000, y - hauteur / 2, 2 * longueur / 5,
                     '#006a4e', '#f42a41')

def drapeau_belgique(x, y, longueur, hauteur):
    rectangle_3_bandes_verticales(x, y, longueur, hauteur,
                                  'black', '#FAE042', '#ED2939')

def drapeau_benin(x, y, longueur, hauteur):
    h = hauteur / 2
    color('#FCD116')
    rectangle_plein(x, y, longueur, h)
    color('#E8112D')
    rectangle_plein(x, y - h, longueur, h)
    color('#008751')
    rectangle_plein(x, y, longueur / 2.5, hauteur)

def drapeau_birmanie(x, y, longueur, hauteur):
    rectangle_3_bandes_horizontales(x, y, longueur, hauteur,
                                    '#FECB00', '#34B233', '#EA2839')
    color('white')
    h = 2 * hauteur / 3
    d = h / 0.951  # voir calcul dans etoile_pleine_5_branches()
    etoile_pleine_5_branches(x + longueur / 2, y - hauteur / 1.92, d)

def drapeau_bolivie(x, y, longueur, hauteur):
    rectangle_3_bandes_verticales(x, y, longueur, hauteur,
                                  'black', '#FAE042', '#ED2939')

def drapeau_bulgarie(x, y, longueur, hauteur):
    rectangle_3_bandes_horizontales(x, y, longueur, hauteur,
                                    'white', '#00966E', '#D62612')

def drapeau_cote_d_ivoire(x, y, longueur, hauteur):
    rectangle_3_bandes_verticales(x, y, longueur, hauteur,
                                  '#f77f00', 'white', '#009e60')

def drapeau_estonie(x, y, longueur, hauteur):
    rectangle_3_bandes_horizontales(x, y, longueur, hauteur,
                                    '#0072ce', 'black', 'white')

def drapeau_france(x, y, longueur, hauteur):
    rectangle_3_bandes_verticales(x, y, longueur, hauteur,
                                  '#002395', 'white', '#ED2939')

def drapeau_gabon(x, y, longueur, hauteur):
    rectangle_3_bandes_horizontales(x, y, longueur, hauteur,
                                    '#3a75c4', '#fcd116', '#009e60')

def drapeau_etats_unis(x, y, longueur, hauteur):
    # Le fond blanc
    color('white')
    rectangle_plein(x, y, longueur, hauteur)
    # Les 7 bandes rouges
    color('#B22234')
    h = hauteur / 13  # 13 bandes
    yy = y
    for i in range(7):
        rectangle_plein(x, yy , longueur, h)
        yy -= 2 * h
    # Le rectangle bleu
    color('#3C3B6E')
    rectangle_plein(x, y, longueur / 2.5, hauteur * 7 / 13)
    # Les étoiles
    color('white')
    # color('#717095', 'white') # false antialiasing if big flag
    elx = longueur / 30
    ely = longueur / 28
    ey = y - ely
    for yy in range(5):
        ex = x + elx
        for xx in range(6):
            etoile_pleine_5_branches(ex, ey, elx)
            ex += 2 * elx
        ey -= 2 * ely

    ey = y - (2 * ely)
    for yy in range(4):
        ex = x + (2 * elx)
        for xx in range(5):
            etoile_pleine_5_branches(ex, ey, elx)
            ex += 2 * elx
        ey -= 2 * ely

def drapeau_japon(x, y, longueur, hauteur):
    rectangle_cercle(x, y, longueur, hauteur,
                     x + longueur / 2, y - hauteur / 2, 2 * longueur / 5,
                     'white', '#bc002d')


### LA SUPER FONCTION POUR AFFICHER TOUS LES DRAPEAUX ###

# Une petite classe pour pouvoir manipuler tous les drapeaux
class Drapeau:
    proportion_variable = False
    proportion_defaut = 2/3
    def __init__(self, pays, proportion, fonction_de_dessin):
        self.pays = pays
        if self.proportion_variable:
            self.proportion = proportion
        else:
            self.proportion = self.proportion_defaut
        self.fonction_de_dessin = fonction_de_dessin

    def dessine(self, x, y, longueur):
        self.fonction_de_dessin(x, y, longueur,
                                longueur * self.proportion)


# La liste de tous les drapeaux
drapeaux_list = list()
drapeaux_list.append(Drapeau("Allemagne", 3/5, drapeau_allemagne))
drapeaux_list.append(Drapeau("Arménie", 1/2, drapeau_armenie))
drapeaux_list.append(Drapeau("Autriche", 2/3, drapeau_autriche))
drapeaux_list.append(Drapeau("Bangladesh", 3/5, drapeau_bangladesh))
drapeaux_list.append(Drapeau("Belgique", 13/15, drapeau_belgique))
drapeaux_list.append(Drapeau("Bénin", 2/3, drapeau_benin))
drapeaux_list.append(Drapeau("Birmanie (Myanmar)", 3/3, drapeau_birmanie))

drapeaux_list.append(Drapeau("Bolivie", 15/22, drapeau_bolivie))
drapeaux_list.append(Drapeau("Bulgarie", 3/5, drapeau_bulgarie))
drapeaux_list.append(Drapeau("Côte d'Ivoire", 2/3, drapeau_cote_d_ivoire))
drapeaux_list.append(Drapeau("Estonie", 7/11, drapeau_estonie))
drapeaux_list.append(Drapeau("France", 2/3, drapeau_france))
drapeaux_list.append(Drapeau("Gabon", 3/4, drapeau_gabon))

drapeaux_list.append(Drapeau("États-Unis", 10/19, drapeau_etats_unis))
drapeau_test = drapeau_birmanie

drapeaux_list.append(Drapeau("Japon", 2/3, drapeau_japon))


# Fonction pour retirer les accents, notamment pour les tris
# sinon États-Unis est le dernier de la liste
# https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string/518232#518232
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

# On trie la liste en utilisant une fonction lambda
drapeaux_list.sort(key=lambda x: strip_accents(x.pays))


def affiche_tous_les_drapeaux(longueur, bord, affiche_texte = False):
    # on récupère la taille de la fenètre
    fenetre_longueur = window_width()
    fenetre_largeur = window_height()
    #setup(fenetre_longueur * 1.0, fenetre_largeur * 1.0)
    #print(screensize(), window_width(), window_height())
    nb_drapeaux = len(drapeaux_list)
    x_depart = -(fenetre_longueur / 2) + bord
    y_depart = (fenetre_largeur / 2) - bord
    max_drapeaux_horiz = int((fenetre_longueur - 2 * bord) / longueur)
    print(max_drapeaux_horiz)
    bord_int = (fenetre_longueur - (2 * bord)) - (max_drapeaux_horiz * longueur)
    bord_int /= (max_drapeaux_horiz - 1)
    if bord_int < 5:
        max_drapeaux_horiz -= 1
        bord_int = (fenetre_longueur - (2 * bord)) - (max_drapeaux_horiz * longueur)
        bord_int /= (max_drapeaux_horiz - 1)
    x = x_depart
    y = y_depart
    print(x,y, bord_int)
    for i in range(nb_drapeaux):
        d = drapeaux_list[i]
        d.dessine(x, y, longueur)
        x += longueur + bord_int
        if x > (fenetre_longueur / 2) - bord - longueur:
            x = x_depart
            y -= longueur * 2/3 + bord_int




### LE PROGRAMME COMMENCE ICI ###

debug = False
#debug = True

rapide = True
#rapide = False
if rapide:
    # On met la vitesse au maximum
    speed(0)
    # On cache la tortue
    hideturtle()
    # On va gérer la mise à jour nous même donc on fait
    # tracer(0). Quand on voudra une mise à jour de l'écran
    # on fera update()
    tracer(0)

# Bord bleu, intérieur rouge
color('black', 'red')

# Epaisseur du trait, 10 gros
pensize(1)

# Test de nos primitives, mettre debug = True pour essayer
if debug:
    color('black', 'red')
    pensize(1)
    croix(0, 0, 40)
    cercle(0, 0, 40)
    cercle_plein(40, 0, 40)
    carre(60, 20, 40)
    carre_plein(100, 20, 40)
    rectangle(-20, -20, 80, 40)
    rectangle_plein(60, -20, 80, 40)
    #color("black")
    x, y, l, h = etoile_5_branches(0, -80, 40)
    rectangle(x, y, l, h) # dessin du rectangle autour de l'étoile
    etoile_pleine_5_branches(40, -80, 40)
    if rapide:
        update()
    k = input("Appuyez sur ENTREE pour continuer")
    clear()

# TODO prévoir aussi de gérer l'épaisseur du contour
# avec peut être un déplacement relatif si le contour
# fait plus de 1 pixel
# avec reset de l'épaisseur des tracers à l'intérieur
contour_drapeau = 'black'

#drapeau_armenie(0, 0, 100, 100)
drapeau_test(-300, 200, 400, 400*2/3)
update()
k = input("Appuyez sur ENTREE pour continuer")


if debug:
    print("Liste des pays en ordre alphabétique:")
    for d in drapeaux_list:
        print(d.pays)

print("Il y a déjà " + str(len(drapeaux_list)) +
      " drapeaux!")

affiche_tous_les_drapeaux(100, 20)

if rapide:
    update()
