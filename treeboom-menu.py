import pygame, sys, subprocess


# pygame initialisation
pygame.font.init()
font = pygame.font.SysFont("Tahoma", 45)

# window settings
LARGEUR = 1280
HAUTEUR = 800
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("treeboom")
clock = pygame.time.Clock()

# load the background image
image1 = pygame.image.load("menu-img-2.png")
image1 = pygame.transform.scale(image1, (LARGEUR, HAUTEUR))

# clickable rectangle zones
button1_rect = pygame.Rect(190, 310, 300, 80)  # "Play"
button2_rect = pygame.Rect(262, 470, 260, 80)  # "Options"
button3_rect = pygame.Rect(350, 700, 200, 70)  # "Exit"
button4_rect = pygame.Rect(1000, 625, 100, 80)  # name
button5_rect = pygame.Rect(1000, 700 ,100, 80)  # score

# text for each button
play_text = font.render("Play", True, (0, 0, 0))
options_text = font.render("Options", True, (0, 0, 0))
exit_text = font.render("Exit", True, (0, 0, 0))
# load name and score from save file
with open("controls.txt", "r+") as f:
    lines = f.readlines()
    name = lines[3]
    # two variables for the score : with and without "high score : "
    points = lines[7].strip()
    points_tx = "high score : " + lines[7]
# create the text for the name and score
name_text = font.render(name.strip(), True, (0,0 ,0))
points_text = font.render(points_tx.strip(), True, (0,0,0))


# Center texts in respective button
play_rect = play_text.get_rect(center=button1_rect.center)
options_rect = options_text.get_rect(center=button2_rect.center)
exit_rect = exit_text.get_rect(center=button3_rect.center)
name_rect = name_text.get_rect(center=button4_rect.center)
points_rect = points_text.get_rect(center=button5_rect.center )

# Main loop
fin = False
while not fin:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fin = True
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # check if a button has been clicked
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

    # Display background image
    fenetre.blit(image1, (0, 0))

    # Display text in each button
    fenetre.blit(play_text, play_rect)
    fenetre.blit(options_text, options_rect)
    fenetre.blit(exit_text, exit_rect)
    fenetre.blit(name_text, name_rect)
    fenetre.blit(points_text, points_rect)

    # display update for each tick
    pygame.display.flip()
    clock.tick(60)  # 60 FPS cap


pygame.quit()

