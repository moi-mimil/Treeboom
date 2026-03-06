import pygame, sys, subprocess

# Initialisation de pygame
pygame.font.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont("Tahoma", 45)
pygame.mixer.init()

#mise en place du son pour le click
click = pygame.mixer.Sound("setting.mp3")
#charger le mute setting
with open("controls.txt", "r") as f:
    lines = f.readlines()
    mute_setting = lines[5].strip()
click.set_volume(int(mute_setting) ^ 1)

# Paramètres de la fenêtre
LARGEUR = 1280
HAUTEUR = 800
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("treeboom")

# Charger une image et la redimensionner
image1 = pygame.image.load("options-menu-tryout.png")
image1 = pygame.transform.scale(image1, (LARGEUR, HAUTEUR))

# Définir les positions et l'état du toggle button
toggle_x = 265
toggle_y = 160
toggle_state = True
radius = 40
green = (0,255,0)
red = (255,0,0)
color = 0

#bouton mute unmute
(mx, my) = pygame.mouse.get_pos()
button_1 = pygame.Rect(500, 100, 300, 120)  # Toggle button
mute_text = font.render("Mute / Unmute", True, (0, 0, 0))
mute_rect = mute_text.get_rect(midtop=(button_1.centerx, button_1.top))

#bouton return menu
button_rect = pygame.Rect(900, 100, 150, 20)
return_text = font.render("Return Menu", True, (0, 0, 0))
button_text_rect = return_text.get_rect(center=button_rect.center)

global filename
filename = "controls.txt"

#boucle principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            subprocess.Popen([sys.executable, "treeboom-menu.py"])
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mx, my) = pygame.mouse.get_pos()

            # Vérifier si le toggle button a été cliqué en cliquant dans le cercle
            if (mx - toggle_x)**2 + (my - toggle_y)**2 <= radius**2:
                toggle_state = not toggle_state

                # Reécrire le fichier texte avec la nouvelle valeur du toggle
                with open(filename, "r+") as f:
                    lines = f.readlines()
                    if lines[1].strip() == "0":
                        lines[1] = "1\n"
                    else:
                        lines[1] = "0\n"

                    f.seek(0)
                    f.writelines(lines)
                    f.truncate()
                click.play()

            # Vérifier si le bouton return menu a été cliqué
            elif button_rect.collidepoint(event.pos):
                click.play()
                subprocess.Popen([sys.executable, "treeboom-menu.py"])
                running = False

            # Vérifier si le bouton mute/unmute a été cliqué
            elif button_1.collidepoint(event.pos):
                #print(mute_setting, type(mute_setting))    pour debugger

                # Reécrire le fichier texte avec la nouvelle valeur du mute setting
                with open(filename, "r+") as f:
                    lines = f.readlines()

                    #inverser la valeur du mute setting
                    if lines[5].strip() == "0":
                        lines[5] = "1\n"
                        mute_setting = "1"
                    else:
                        lines[5] = "0\n"
                        mute_setting = "0"

                    f.seek(0)
                    f.writelines(lines)
                    f.truncate()

                click.play()



        # Quitter la boucle si la fenêtre est fermée
        if event.type == pygame.QUIT:
            running = False
    # Remplir l'écran avec l'image de fond
    fenetre.blit(image1, (0, 0))


    # Dessiner le toggle button avec la couleur appropriée, vert pour activé, rouge pour désactivé

    pygame.draw.circle(fenetre, (toggle_state*255, abs(1-toggle_state)*255, 0), (toggle_x, toggle_y), radius)

    # Dessiner le bouton mute/unmute avec la couleur appropriée
    mute_setting = int(mute_setting)
    pygame.draw.circle(fenetre, (mute_setting*255, abs(1-mute_setting)*255, 0), (640, 180), 20)

    # Afficher les textes des boutons
    fenetre.blit(mute_text, mute_rect)
    fenetre.blit(return_text, button_text_rect)

    # Mettre à jour l'affichage
    pygame.display.flip()
    clock.tick(60)


pygame.quit()