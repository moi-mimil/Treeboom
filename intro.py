import pygame, sys, subprocess

#mise en place du son pour l'entree du nom
pygame.mixer.init()
sound = pygame.mixer.Sound("setting.mp3")
with open("controls.txt", "r") as f:
    lines = f.readlines()
    mute_setting = lines[5].strip()
sound.set_volume(int(mute_setting) ^ 1)


#secure txt file
filename = "controls.txt"

#on reecr le fichier avec les valeurs par defaut
with open(filename, "w") as f:
    f.write("wasd or zqsd (0 is wasd 1 is zqsd):\n1\nname:\nplaceholder\nMute/Unmute (0 is unmute 1 is mute):\n0\npoints:\n0\n")

if not pygame.mixer.get_init():
    pygame.mixer.init()









# Initialisation de pygame
pygame.init()

# Paramètres de la fenêtre
LARGEUR= 1280
HAUTEUR = 800
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("L'aventure interactive")

clock = pygame.time.Clock()
# Police de texte
font = pygame.font.Font("04b_25__.ttf", 30)

# Définition des variables des couleurs à utiliser dans le programme
BLEU = (116, 208, 241)
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)

# Charger une image et la redimensionner
image1 = pygame.image.load("menu-img-2.png")
image1 = pygame.transform.scale(image1, (LARGEUR, HAUTEUR))

# Variables de jeu
input_active = False
prenom_joueur = ""

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
            fenetre.blit(font.render(ligne_actuelle.strip(), True, couleur), (x, y + y_offset))
            ligne_actuelle = mot + ' '
            y_offset += font.get_height()  # Augmente l'offset pour la prochaine ligne

    # Dessine la dernière ligne si elle n'est pas vide
    if ligne_actuelle:
        fenetre.blit(font.render(ligne_actuelle.strip(), True, couleur), (x, y + y_offset))


def input_text(x, y, largeur, hauteur, couleur_fond, couleur_texte):
    """
    Cette fonction gère la saisie de texte par l'utilisateur dans une zone de texte définie dans une fenêtre Pygame.
    L'utilisateur peut entrer du texte jusqu'à appuyer sur la touche "Entrée", moment auquel la saisie est terminée
    et le texte saisi est retourné.

    Paramètres :
    -----------
        x (int) : La position en pixels sur l'axe des abscisses (horizontal) où la zone de texte commence à être affichée.

        y (int) : La position en pixels sur l'axe des ordonnées (vertical) où la zone de texte commence à être affichée.

        largeur (int) : La largeur de la zone de texte en pixels.

        hauteur (int) : La hauteur de la zone de texte en pixels.

        couleur_fond (tuple) : La couleur de fond de la zone de texte, définie sous forme de tuple (R, G, B).

        couleur_texte (tuple) : La couleur du texte dans la zone de texte, définie sous forme de tuple (R, G, B).

    Returns :
    -------
        texte (str) : Le texte saisi par l'utilisateur.
    """
    assert type(x) == int and type(y) == int, "Les paramètres 'x' et 'y' doivent être des entiers."
    assert type(largeur) == int and type(hauteur) == int, "Les paramètres 'largeur' et 'hauteur' doivent être des entiers."
    assert type(couleur_fond) == tuple and len(couleur_fond) == 3, "Le paramètre 'couleur_fond' doit être un tuple de trois entiers (R, G, B)."
    assert type(couleur_texte) == tuple and len(couleur_texte) == 3, "Le paramètre 'couleur_texte' doit être un tuple de trois entiers (R, G, B)."

    global input_active
    input_active = True
    texte = ""

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False  # Désactive l'input
                    return texte  # Retourne le texte saisi
                elif event.key == pygame.K_BACKSPACE:
                    texte = texte[:-1]  # Supprime le dernier caractère
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    if len(texte) < 48 and event.unicode.isprintable():  # Limite la longueur du texte à 49 caractères
                        texte += event.unicode  # Ajoute le caractère à la chaîne
                        sound.play()

        # Afficher la zone de texte
        pygame.draw.rect(fenetre, couleur_fond, (x, y, largeur, hauteur))

        # Afficher le texte
        texte_surface = font.render(texte + "_", True, couleur_texte)
        fenetre.blit(texte_surface, (x + 10, y + 10))

        pygame.display.flip()  # Met à jour l'affichage

fin = False

#pygame.key.set_repeat(300, 50)


# Boucle principale du jeu, tant que le jeu n'est pas fini on continue
while not fin:

    # Boucle de gestion des évènements dans la fenêtre
    for event in pygame.event.get():

        # Si l'utilisateur appuie sur la croix en haut à droite, cela met fin au jeu et ferme pygame
        if event.type == pygame.QUIT:
            fin = True
            pygame.quit()
            sys.exit()

    # Remplir l'écran de bleu
    fenetre.fill(BLEU)

    # Afficher l'image à l'écran, le coin en haut à gauche à la coordonnée 0,0
    fenetre.blit(image1, (0, 0))

    # Si le prénom du joueur n'a pas encore été saisi
    if prenom_joueur == "":
        # On demande et on recupère le prénom saisi par l'utilisateur
        afficher_texte("Quel est", 300, 300, NOIR)
        afficher_texte("ton nom ?", 300, 330, NOIR)
        prenom_joueur = input_text(200, 500, 800, 50, BLANC, BLEU)
        #verification du nom jade pour le troll
        if "jade" in prenom_joueur:
            print(""" \033[31mTraceback (most recent call last):
File "D:/treeboomPEAK WITH SAVE ONE/intro.py", line 165, in <name>
    jade
pygame.error: user name is too short\033[0m""")
            fin = True
            pygame.quit()
            sys.exit()

        elif prenom_joueur.strip() == "placeholder":
            print("name reserved error, please choose another name")
            prenom_joueur = ""

        #si le nom est valide (pas jade) on l'enregistre dans le fichier txt
        else:
            if prenom_joueur != "":
                filename = "controls.txt"
                with open(filename, "r+") as f:
                    lines = f.readlines()
                    lines[3] = prenom_joueur
                    lines[3] += "\n"

                    f.seek(0)
                    f.writelines(lines)
                    f.truncate()
                    subprocess.Popen([sys.executable, "treeboom-menu.py"])
                    fin = True

    # Mise à jour de l'affichage
    pygame.display.flip()
    clock.tick(60)  # 60 FPS cap
pygame.quit()
sys.exit()
