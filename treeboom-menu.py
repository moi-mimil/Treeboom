import pygame, sys, subprocess


# Initialisation de pygame
pygame.font.init()
font = pygame.font.SysFont("Tahoma", 45)

# Paramètres de la fenêtre
LARGEUR = 1280
HAUTEUR = 800
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("treeboom")
clock = pygame.time.Clock()

# Charger une image et la redimensionner
image1 = pygame.image.load("menu-img-2.png")
image1 = pygame.transform.scale(image1, (LARGEUR, HAUTEUR))

# Définir les rectangles des zones cliquables (invisibles)
button1_rect = pygame.Rect(190, 310, 300, 80)  # "Play"
button2_rect = pygame.Rect(262, 470, 260, 80)  # "Options"
button3_rect = pygame.Rect(350, 700, 200, 70)  # "Exit"
button4_rect = pygame.Rect(1000, 625, 100, 80)  #montrer le nom
button5_rect = pygame.Rect(1000, 700 ,100, 80)  #montrer le score

# Créer les textes des boutons
play_text = font.render("Play", True, (0, 0, 0))
options_text = font.render("Options", True, (0, 0, 0))
exit_text = font.render("Exit", True, (0, 0, 0))
# Récupérer le nom et le score du joueur depuis le fichier texte
with open("controls.txt", "r+") as f:
    lines = f.readlines()
    name = lines[3]
    # deux variables pour le score avec et sans le texte "high score : "
    points = lines[7].strip()
    points_tx = "high score : " + lines[7]
# Créer les textes pour le nom et le score
name_text = font.render(name.strip(), True, (0,0 ,0))
points_text = font.render(points_tx.strip(), True, (0,0,0))


# Centrer les textes dans les boutons
play_rect = play_text.get_rect(center=button1_rect.center)
options_rect = options_text.get_rect(center=button2_rect.center)
exit_rect = exit_text.get_rect(center=button3_rect.center)
name_rect = name_text.get_rect(center=button4_rect.center)
points_rect = points_text.get_rect(center=button5_rect.center )

# Boucle principale
fin = False
while not fin:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fin = True
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Vérifier si un bouton a été cliqué
            if button1_rect.collidepoint(event.pos):
                print("Play clicked")
                subprocess.Popen([sys.executable, "treeboom.py"])
                pygame.quit()
            elif button2_rect.collidepoint(event.pos):
                print("Options clicked")
                subprocess.Popen([sys.executable, "treeboom-settings.py"])
                pygame.quit()

            elif button3_rect.collidepoint(event.pos):
                print("Exit has been clicked")
                pygame.quit()
                sys.exit()
            elif button4_rect.collidepoint(event.pos):
                subprocess.Popen([sys.executable, "intro.py"])
                pygame.quit()
            elif button5_rect.collidepoint(event.pos):
                print("you have", points, "points")

    # Afficher l'image de fond
    fenetre.blit(image1, (0, 0))

    # Afficher les textes des boutons (optionnel)
    fenetre.blit(play_text, play_rect)
    fenetre.blit(options_text, options_rect)
    fenetre.blit(exit_text, exit_rect)
    fenetre.blit(name_text, name_rect)
    fenetre.blit(points_text, points_rect)

    # Mise à jour de l'affichage
    pygame.display.flip()
    clock.tick(60)  # 60 FPS cap


pygame.quit()
