import pygame, sys, math, subprocess, time
from random import *


# Initialize the mixer before loading sounds
pygame.mixer.init()

# charger les sons
game_over = pygame.mixer.Sound('game-over.mp3')
hit_enemy = pygame.mixer.Sound('hit-enemy.mp3')

# lire les parametres
with open("controls.txt", "r") as f:
    lines = f.readlines()
    mute_setting = lines[5].strip()
    score_test = int(lines[7].strip())

# appliquer le volume
game_over.set_volume(int(mute_setting) ^ 1)
hit_enemy.set_volume((int(mute_setting) ^ 1)*0.7)

# Initialisation de Pygame
pygame.init()
score = 0

# Paramètres de la fenêtre
LARGEUR, HAUTEUR = 1280, 800
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Déplacements et tir")

# Charger les images
miku_img = pygame.image.load("miku1-no-w.png")
smol_tree = pygame.image.load("smol-tree.png")
big_tree = pygame.image.load("big-tree.png")
mid_tree = pygame.image.load("mid-tree.png")
damazon = pygame.image.load("damazon-down.png")
damazon_down = pygame.image.load("damazon-down.png")
damazon_up = pygame.image.load("damazon-up.png")
damazon_right = pygame.image.load("damazon-right.png")
damazon_left = pygame.image.load("damazon-left.png")
dead = pygame.image.load("dead-antimilo.png")

# Police de texte
font = pygame.font.Font("04b_25__.ttf", 30)

def afficher_texte(texte, x, y, couleur):
    """
    Cette fonction permet d'afficher du texte dans une fenêtre Pygame à partir d'une position donnée (x, y). Si une ligne de texte dépasse
    la largeur de la fenêtre, elle est automatiquement coupée et continuée à la ligne suivante.

    Paramètres :
    -----------
        texte(str) : Le texte à afficher.

        x(int) : La position en pixels sur l'axe des abscisses (horizontal) où le texte commence à être affiché.

        y(int) : La position en pixels sur l'axe des ordonnées (vertical) où le texte commence à être affiché.

        couleur(tuple): Une couleur définie sous forme de tuple (R, G, B) pour la couleur du texte.
    """


    assert type(texte) == str, "Le paramètre 'texte' doit être une chaîne de caractères."
    assert type(x) == int and type(y) == int, "Les paramètres 'x' et 'y' doivent être des entiers."
    assert type(couleur) == tuple and len(couleur) == 3, "Le paramètre 'couleur' doit être un tuple de trois entiers (R, G, B)."
    mots = texte.split(' ')
    ligne_actuelle = ''
    y_offset = 0

    for mot in mots:
        # Vérifie si on peut ajouter le mot à la ligne actuelle
        if font.size(ligne_actuelle + mot)[0] <= LARGEUR - x:
            ligne_actuelle += mot + ' '
        else:
            # Dessine la ligne actuelle et réinitialise pour la nouvelle ligne
            ecran.blit(font.render(ligne_actuelle.strip(), True, couleur), (x, y + y_offset))
            ligne_actuelle = mot + ' '
            y_offset += font.get_height()  # Augmente l'offset pour la prochaine ligne

    # Dessine la dernière ligne si elle n'est pas vide
    if ligne_actuelle:
        ecran.blit(font.render(ligne_actuelle.strip(), True, couleur), (x, y + y_offset))




# Variables de jeu
co2 = 1
ran = True # pour le respawn enemy

# initial background
background1 = pygame.image.load("background-grey0.png")
current_back = background1



def enemy(j_x,j_y, c_x, c_y):
    """
     on call la fonction avec les coordonées de joueur
        j-x, j_y
    et les coordonées de la balle
        c_y , c_x

    on global score car on ajoute + si on tue anti milo
    on global alive pour le respawn
    on global ran pour tourner le respawn une seule fois
    current back sert a change the background (niveau co2)
    on calcule grace au coo de joueur, le vecteur ideal puis on y va
        la vittese de deplacement est defini pour le gametesting

    si joueur est dans un radius de 30px, c fini pour nous 
        on reouvre menu apres


    """
    assert (type(j_x) == int or type(j_x) == float) and (type(j_y) == int or type(j_y) == float), "Les paramètres de position du joueur doivent être des entiers ou des flottants."
    assert (type(c_x) == int or type(c_x) == float) and (type(c_y) == int or type(c_y) == float), "Les paramètres de position de la balle doivent être des entiers ou des flottants."
    

    #on utilise les variables globales
    global alive, e_x, e_y, score, current_back, ran

    assert (type(e_x) == int or type(e_x) == float) and (type(e_y) == int or type(e_y) == float), "Les variables de position de l'enemy doivent être des entiers ou des flottants."
    assert type(score) == int, "Le score doit être un entier."
    assert type(alive) == bool, "La variable 'alive' doit être un booléen."
    assert type(ran) == bool, "La variable 'ran' doit être un booléen."


    # logique enemy
    if alive == True:
        # calcule de la vitesse selon le score
        speed = score +1
        # calcul du vecteur entre enemy et joueur
        dx, dy = j_x - e_x, j_y - e_y
        dist = math.hypot(dx, dy)
         # calcule de la hitbox de l'enemy
        e_w, e_h = anti.get_width(), anti.get_height()
        e_c_x = e_x + e_w / 2
        e_c_y = e_y + e_h / 2
        # detection de collision avec une balle
        for bx, by, _, _ in nouvelles_balles:
            # calcul de la distance entre la balle et l'enemy
            dist2 = math.hypot(bx - e_c_x, by - e_c_y)
            # si la distance est inferieure a 30px, on le tue
            if dist2 < 30:
                #sequence de mort de l'enemy
                hit_enemy.play()
                score += 1
                alive = False
                # repositionnement aleatoire au prochain spawn selon 4 position
                # "temp" est une variable temporaire pour stocker le resultat du randint
                temp = randint(0,3)
                if temp==0:
                    e_x, e_y = 550, 800
                elif temp==1:
                    e_x, e_y = 0, 500
                elif temp==2:
                    e_x, e_y =1280, 270
                else:
                    e_x, e_y = 780, 0

                ran = False # variable pour ne pas repeter le respawn et freeze le pc
        # si la distance est inferieure a 30px, on perd
        if dist < 30:
            #sequence de mort du joueur
            game_over.play()
            pygame.time.delay(1000)
            for i in range(50):
                ecran.blit(dead, (0,0))
            quit_game(score, score_test)


        dx, dy = dx / dist, dy / dist  # Normalise le vecteur
        # vitesse par rapport au vecteur
        e_x += dx * speed
        e_y += dy * speed
        # Affichage de l'enemy
        ecran.blit(anti, (int(e_x), int(e_y)))



# Variables joueur
j_w, j_h = 40, 60
miku_img = pygame.transform.scale(miku_img, (j_w, j_h))# rezise de miku au rectangle defini
j_x, j_y = LARGEUR//2, HAUTEUR//2
v_joueur = 5
bord_arrondi = 100

# Variables viseur
dist_max_point = 40
rayon_point = 8
coul_point = (255, 0, 0)

# Variables enemy
anti = pygame.image.load("anti-milo.png")
anti = pygame.transform.scale(anti, (80, 60))
global e_y,e_x
e_x =550
e_y =800

# Variables balles
balles = []
v_balle = 12
rayon_balle = 5
coul_balle = (255, 255, 0)


horloge = pygame.time.Clock()# pour horloge.tick pour fps (mit a 60)

# fonction quitter le jeu proprement
def quit_game(sc, sc_test):
    assert type(sc) == int and type(sc_test) == int , "Les scores doivent être des entiers."
    if sc > sc_test:
        # mise a jour du score dans le fichier txt
        with open('controls.txt', "r+")as f:
            lines = f.readlines()
            lines[7] = str(sc) + "\n"
            f.seek(0)
            f.writelines(lines)
            f.truncate()
    subprocess.Popen([sys.executable, "treeboom-menu.py"])
    alive = False
    sys.exit()







def creer_arbre(): # CREATION D'ARBRE ET CHOIX ENTRE POSITIONS
    """
      on call la fonction



      la fonction return "pose", coordonée de l'arbre
    """
    global current_back, co2
    assert type(co2) == int , "Le niveau de CO2 doit être un entier."
    #on change le background selon le niveau de co2
    if co2 >=32:
        current_back = pygame.image.load("background-grey3.png")
    elif co2 >= 22:
        current_back = pygame.image.load("background-grey2.png")
    elif co2 >= 12:
        current_back = pygame.image.load("background-grey1.png")
    #sinon on garde le background de base (sans gris)

    # choix aleatoire de la position de l'arbre parmi 6 positions
    rd_tree = randint(1,6)

    if rd_tree == 1:
        pose = (900, 500)

    elif rd_tree == 2:
        pose = (50, 200)

    elif rd_tree == 3:
        pose = (400, 90)

    elif rd_tree == 4:
        pose = (1000, 15)

    elif rd_tree == 5:
        pose = (1100, 350)

    elif rd_tree == 6:
        pose = (90, 400)

    #print(pose) pour debugger les positions
    return pose  # on return la position choisie au hasard

# initialisation de l'arbre et recup des coordonnees
t_x, t_y = creer_arbre()

# Variables viseur
c_x = 0
c_y = 0

#choix du mode de controle (azerty/qwerty)
touches = pygame.key.get_pressed()
with open("controls.txt", "r") as f:
    lines = f.readlines()
    control_mode = int(lines[1].strip())

# Variables de respawn
global alive, alive_t, enemy_respawn_time, tree_respawn_time, ran_t
alive = True
alive_t = True
running = True
enemy_respawn_time = 0
tree_respawn_time = 0
ran_t = False



#mise en place du bouton retour menu
button_rect = pygame.Rect(900, 0, 150, 20)
return_text = font.render("Return Menu", True, (255, 255, 255))
button_text_rect = return_text.get_rect(center=button_rect.center)



while running:
    # BOUCLE PRINCIPALE  -----------------------------------------------------------------------------------------------------------------

    for ev in pygame.event.get():
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(ev.pos):
                quit_game(score, score_test)
        # Création d'une balle (imagee par le carton), calcul de la direction, normalisation, et ajout à la liste des balles
        s_x, s_y = pygame.mouse.get_pos()
        c_x = j_x + j_w / 2
        c_y = j_y + j_h / 2
        dir_x = s_x - c_x
        dir_y = s_y - c_y
        dist = math.hypot(dir_x, dir_y)
        angle = math.atan2(s_y - j_y, s_x - j_x) * 180 / math.pi

        if angle >= 45 and angle < 135:
            dir = "Down"
            damazon = damazon_down
        elif angle >= 135 or angle < -135:
            dir = "Left"
            damazon = damazon_left
        elif angle >= -135 and angle < -45:
            dir = "Up"
            damazon = damazon_up
        elif angle >= -45 and angle < 45:
            dir = "Right"
            damazon = damazon_right


        if alive == False and not ran:
            ran = True
            enemy_respawn_time = time.time() + randint(1, 7)  # temps d'attente pour qui respawn j'ai mis 1-7 pour l'instant
        if alive_t == False and not ran_t:
            ran_t = True
            tree_respawn_time = time.time() + randint(0, 3)  # temps d'attente pour qui respawn j'ai mis 0-3 pour l'instant

        # on verifie si c bon pour le respawn
        if ran and not alive and time.time() >= enemy_respawn_time:
            alive = True

            enemy(j_x , j_y, c_x, c_y)

        if ran and not alive_t and time.time() >= tree_respawn_time:
            alive_t = True
            t_x, t_y = creer_arbre()

        # tue le joueur si il est dans l'eau
        if j_x < 68 or j_x > LARGEUR - 68 or j_y > HAUTEUR - 115 or j_y < 68:
            quit_game(score, score_test)

        if ev.type == pygame.QUIT:
            quit_game(score, score_test)
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and dist !=0 and len(balles) < 3:
            dir_x /= dist
            dir_y /= dist
            balles.append([c_x, c_y, dir_x, dir_y])


    # Déplacements joueur
    touches = pygame.key.get_pressed()
    if control_mode == 0:
        dx = touches[pygame.K_d] - touches[pygame.K_q]
        dy = touches[pygame.K_s] - touches[pygame.K_z]
    else:
        dx = touches[pygame.K_d] - touches[pygame.K_a]
        dy = touches[pygame.K_s] - touches[pygame.K_w]


    # Normalisation du vecteur de déplacement
    if dx != 0 or dy != 0:
        longueur = math.hypot(dx, dy)
        dx /= longueur
        dy /= longueur

    j_x += dx * v_joueur
    j_y += dy * v_joueur
    j_x = max(0, min(LARGEUR - j_w, j_x))
    j_y = max(0, min(HAUTEUR - j_h, j_y))



    # mise a jour des positions des balles
    nouvelles_balles = []
    for bx, by, dx, dy in balles:
        bx += dx * v_balle
        by += dy * v_balle
        if 0 < bx < LARGEUR and 0 < by < HAUTEUR:
            nouvelles_balles.append([bx, by, dx, dy])

    balles = nouvelles_balles

    ecran.blit(current_back, (0, 0)) # on blit le fond d'ecran selon niveau co2
    # redimention des arbres
    t_w, t_h = smol_tree.get_width(), smol_tree.get_height()
    t_c_x = t_x + t_w / 2
    t_c_y = t_y + t_h / 2


    # detection de collision avec un arbre par les balles
    for bx, by, _, _ in nouvelles_balles:
        dist_tree = math.hypot(bx - t_c_x, by - t_c_y)
        if dist_tree < 80:
            if alive_t:
                co2 += 1


            # on prepare le respawn de l'arbre pour pas freeze le pc
            alive_t = False
            ran_t= False 
            break

    # Affichage de l'arbre s'il est vivant
    if alive_t:
        ecran.blit(smol_tree, (t_x, t_y))



    # on call enemy pour la premiere fois
    enemy(j_x , j_y, c_x, c_y)


    # Joueur
    ecran.blit(miku_img, (int(j_x), int(j_y)))

    # Point rouge (viseur attaché au joueur, qui a ete remplacé par l'image damazon)
    s_x, s_y = pygame.mouse.get_pos()
    c_x = j_x + j_w / 2
    c_y = j_y + j_h / 2
    vec_x = s_x - c_x
    vec_y = s_y - c_y
    distance = math.hypot(vec_x, vec_y)
    if distance != 0:
        dist_reelle = min(distance, dist_max_point)
        vec_x = vec_x / distance * dist_reelle
        vec_y = vec_y / distance * dist_reelle
    point_x = c_x + vec_x
    point_y = c_y + vec_y
    ecran.blit(damazon, (int(point_x-11), int(point_y-6)))



    # Dessiner les balles
    for bx, by, _, _ in balles:
        ecran.blit(damazon, (int(bx), int(by)))

    # afficher les textes

    afficher_texte( "score :", 150, 0, (255, 255, 255))
    afficher_texte( "cartons :", 550, 0, (255, 255, 255))
    afficher_texte( "co2 level:", 910, 750, (255, 255, 255))


    afficher_texte(str(co2), 1090, 750, (255, 255, 255))
    afficher_texte( str(score), 260, 0, (255, 255, 255))
    afficher_texte( str(3-len(nouvelles_balles))+ " /3", 660, 0, (255, 255, 255))

    # bouton retour menu
    ecran.blit(return_text, button_text_rect)

    # Actualisation de l'écran
    pygame.display.flip()

    horloge.tick(60)# FIN DE WHILE----------------------------------------------------------------------------------


pygame.quit()