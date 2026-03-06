import pygame, sys, math, subprocess, time
from random import *


# Initialize the mixer before loading sounds
pygame.mixer.init()

# loads the sound files
game_over = pygame.mixer.Sound('game-over.mp3')
hit_enemy = pygame.mixer.Sound('hit-enemy.mp3')

# read the mute setting and score from controls.txt
with open("controls.txt", "r") as f:
    lines = f.readlines()
    mute_setting = lines[5].strip()
    score_test = int(lines[7].strip())

# set the volume of the sounds according to the mute setting
game_over.set_volume(int(mute_setting) ^ 1)
hit_enemy.set_volume((int(mute_setting) ^ 1)*0.7)

# initialize pygame
pygame.init()
score = 0

# window settings
LARGEUR, HAUTEUR = 1280, 800
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Déplacements et tir")

# load and resize images
miku_img = pygame.image.load("miku1-no-w.png")
smol_tree = pygame.image.load("smol-tree.png")
big_tree = pygame.image.load("big-tree.png")
mid_tree = pygame.image.load("mid-tree.png")
damazon_down = pygame.image.load("damazon-down.png")
damazon_up = pygame.image.load("damazon-up.png")
damazon_right = pygame.image.load("damazon-right.png")
damazon_left = pygame.image.load("damazon-left.png")
damazon = damazon_down
dead = pygame.image.load("dead-antimilo.png")

# font settings
font = pygame.font.Font("04b_25__.ttf", 30)

def afficher_texte(texte, x, y, couleur):
    """
    This function displays text in a Pygame window starting from a given position (x, y). If a line of text exceeds the window width, it is automatically truncated and continued on the next line.

    Parameters:

    ------------
    text(str): The text to display.

    x(int): The position in pixels on the x-axis (horizontal) where the text begins to be displayed.

    y(int): The position in pixels on the y-axis (vertical) where the text begins to be displayed.

    color(tuple): A color defined as a tuple (R, G, B) for the text color.
    """


    assert type(texte) == str, "Le paramètre 'texte' doit être une chaîne de caractères."
    assert type(x) == int and type(y) == int, "Les paramètres 'x' et 'y' doivent être des entiers."
    assert type(couleur) == tuple and len(couleur) == 3, "Le paramètre 'couleur' doit être un tuple de trois entiers (R, G, B)."
    mots = texte.split(' ')
    ligne_actuelle = ''
    y_offset = 0

    for mot in mots:
        # check if the current line plus the next word exceeds the window width
        if font.size(ligne_actuelle + mot)[0] <= LARGEUR - x:
            ligne_actuelle += mot + ' '
        else:
            # Draw the current line and reset for the new line
            ecran.blit(font.render(ligne_actuelle.strip(), True, couleur), (x, y + y_offset))
            ligne_actuelle = mot + ' '
            y_offset += font.get_height()  # Increase the offset for the next line

    # Draw the last line if it is not empty
    if ligne_actuelle:
        ecran.blit(font.render(ligne_actuelle.strip(), True, couleur), (x, y + y_offset))




# game variables
co2 = 1
ran = True # for enemy respawn

# initial background
background1 = pygame.image.load("background-grey0.png")
current_back = background1



def enemy(j_x,j_y, c_x, c_y):
    """
    This function manages the behavior of the enemy in the game. It calculates the movement of the enemy towards the player, checks for collisions with the player's bullets, and handles the respawn of the enemy when it is defeated.
    Parameters:
    j_x (int or float): The x-coordinate of the player.
    j_y (int or float): The y-coordinate of the player.
    c_x (int or float): The x-coordinate of the center of the player (used for aiming).
    c_y (int or float): The y-coordinate of the center of the player (used for aiming).

    outputs:
    The function does not return any value but updates the global variables related to the enemy's state
    and the player's score. It also handles the drawing of the enemy on the screen and the game over condition when the enemy collides with the player.

    function logic:
    - If the enemy is alive, it calculates the direction vector from the enemy to the player and normalizes it to determine the movement of the enemy towards the player.
    - It checks for collisions between the enemy and the player's bullets. If a bullet is close enough to the enemy, it plays a hit sound, increases the player's score, and sets the enemy to not alive, triggering its respawn.
    - If the enemy gets too close to the player, it plays a game over sound, displays a game over screen, and quits the game.

    respawn logic:
    - When the enemy is defeated, it is set to not alive and a random respawn
    - position is chosen for the enemy among four predefined positions. The respawn is managed by a timer to prevent immediate respawn and potential freezing of the game.


    """
    assert (type(j_x) == int or type(j_x) == float) and (type(j_y) == int or type(j_y) == float), "Les paramètres de position du joueur doivent être des entiers ou des flottants."
    assert (type(c_x) == int or type(c_x) == float) and (type(c_y) == int or type(c_y) == float), "Les paramètres de position de la balle doivent être des entiers ou des flottants."
    

    # we use global variables to manage the state of the enemy and the player's score, as well as the respawn logic for both the enemy and the tree.
    global alive, e_x, e_y, score, current_back, ran

    assert (type(e_x) == int or type(e_x) == float) and (type(e_y) == int or type(e_y) == float), "Les variables de position de l'enemy doivent être des entiers ou des flottants."
    assert type(score) == int, "Le score doit être un entier."
    assert type(alive) == bool, "La variable 'alive' doit être un booléen."
    assert type(ran) == bool, "La variable 'ran' doit être un booléen."


    # enemy behavior and collision detection
    if alive == True:
        # speed calculated based on the score (to increase difficulty as the player progresses)
        speed = score +1
        # calculate the direction vector from the enemy to the player
        dx, dy = j_x - e_x, j_y - e_y
        dist = math.hypot(dx, dy)
        # calculate the hitbox of the enemy
        e_w, e_h = anti.get_width(), anti.get_height()
        e_c_x = e_x + e_w / 2
        e_c_y = e_y + e_h / 2
        # collision detection with a bullet
        for bx, by, _, _ in nouvelles_balles:
            # calculate the distance between the bullet and the center of the enemy
            dist2 = math.hypot(bx - e_c_x, by - e_c_y)
            # if the distance is less than 30 pixels, it is considered a hit on the enemy
            if dist2 < 30:
                # play the hit sound, increase the score, and set the enemy to not alive to trigger its respawn
                hit_enemy.play()
                score += 1
                alive = False
                # prepare the respawn of the enemy by choosing a random position among four predefined positions and setting the respawn timer to prevent immediate respawn and potential freezing of the game.
                temp = randint(0,3)
                if temp==0:
                    e_x, e_y = 550, 800
                elif temp==1:
                    e_x, e_y = 0, 500
                elif temp==2:
                    e_x, e_y =1280, 270
                else:
                    e_x, e_y = 780, 0

                ran = False # variable to manage the respawn timing of the enemy, and not freeze the game
        # if the enemy gets too close to the player, it is considered a collision that results in a game over. The game over sound is played, a game over screen is displayed, and the game is quit.
        if dist < 30:
            # death sequence: play game over sound, display game over screen, and quit the game
            game_over.play()
            pygame.time.delay(1000)
            for i in range(50):
                ecran.blit(dead, (0,0))
            quit_game(score, score_test)


        dx, dy = dx / dist, dy / dist  # Normalising  the vector
        # speed of the enemy in function of this vector
        e_x += dx * speed
        e_y += dy * speed
        # draw the enemy on the screen
        ecran.blit(anti, (int(e_x), int(e_y)))



# player variables
j_w, j_h = 40, 60
miku_img = pygame.transform.scale(miku_img, (j_w, j_h))# rezise the player image to fit the hitbox
j_x, j_y = LARGEUR//2, HAUTEUR//2
v_joueur = 5
bord_arrondi = 100

# pointer variables
dist_max_point = 40
rayon_point = 8
coul_point = (255, 0, 0)

# enemy variables
anti = pygame.image.load("anti-milo.png")
anti = pygame.transform.scale(anti, (80, 60))
global e_y,e_x
e_x =550
e_y =800

# ball variables
balles = []
v_balle = 12
c_x = 0
c_y = 0


horloge = pygame.time.Clock()

# properly quit the game and return to the menu, while saving the score if it is higher than the previous score stored in controls.txt
def quit_game(sc, sc_test):
    assert type(sc) == int and type(sc_test) == int , "Les scores doivent être des entiers."
    if sc > sc_test:
        # updates the score in controls.txt if the current score is higher than the previous score
        with open('controls.txt', "r+")as f:
            lines = f.readlines()
            lines[7] = str(sc) + "\n"
            f.seek(0)
            f.writelines(lines)
            f.truncate()
    subprocess.Popen([sys.executable, "treeboom-menu.py"])
    alive = False
    sys.exit()







def creer_arbre(): # creation of the tree and random choice of its position among 6 predefined positions
    """
    this function creates a tree in the game and randomly chooses its position among six predefined positions.
    The background of the game is also updated based on the current CO2 level, which is a global variable that increases when the player successfully hits the tree with a bullet.
    The function returns the coordinates of the tree's position for use in collision detection and drawing the tree on the screen.
      
    inputs:
        - none, but it uses the global variable 'co2' to determine the background and the state of the game.

    outputs:
        - pose (tuple): A tuple containing the x and y coordinates of the tree's position on the screen.

    """
    global current_back, co2
    assert type(co2) == int , "Le niveau de CO2 doit être un entier."
    # we change the background according to the co2 level
    if co2 >=32:
        current_back = pygame.image.load("background-grey3.png")
    elif co2 >= 22:
        current_back = pygame.image.load("background-grey2.png")
    elif co2 >= 12:
        current_back = pygame.image.load("background-grey1.png")
    # otherwise we keep the base background (without gray)

    # random choice of the tree's position among 6 positions
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

    return pose  # we return the randomly chosen position of the tree for use in collision detection and drawing the tree on the screen

# initialisation of the first tree's position
t_x, t_y = creer_arbre()



# choice of the control mode (ZQSD or WASD) based on the settings stored in controls.txt, and management of the player's movement according to the chosen control mode.
touches = pygame.key.get_pressed()
with open("controls.txt", "r") as f:
    lines = f.readlines()
    control_mode = int(lines[1].strip())

# respawn variables
global alive, alive_t, enemy_respawn_time, tree_respawn_time, ran_t
alive = True
alive_t = True
running = True
enemy_respawn_time = 0
tree_respawn_time = 0
ran_t = False



# button variables for returning to the menu
button_rect = pygame.Rect(900, 0, 150, 20)
return_text = font.render("Return Menu", True, (255, 255, 255))
button_text_rect = return_text.get_rect(center=button_rect.center)



while running:
    # MAIN LOOP -----------------------------------------------------------------------------------------------------------------

    for ev in pygame.event.get():
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(ev.pos):
                quit_game(score, score_test)
        # creation of a vector from the center of the player to the mouse position to determine the direction of the shot
        s_x, s_y = pygame.mouse.get_pos()
        c_x = j_x + j_w / 2
        c_y = j_y + j_h / 2
        dir_x = s_x - c_x
        dir_y = s_y - c_y
        dist = math.hypot(dir_x, dir_y)
        angle = math.atan2(s_y - j_y, s_x - j_x) * 180 / math.pi

        # the orientation of the aiming reticle (damazon)
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
            enemy_respawn_time = time.time() + randint(1, 7)  #  arbitrary respawn time for the enemy
        if alive_t == False and not ran_t:
            ran_t = True
            tree_respawn_time = time.time() + randint(0, 3)  #  arbitrary respawn time for the tree

        # we check if the respawn timers for the enemy and the tree have elapsed, and if so, we set them to alive again and call the enemy function to respawn the enemy at a new position, and we call the creer_arbre function to respawn the tree at a new position.
        if ran and not alive and time.time() >= enemy_respawn_time:
            alive = True

            enemy(j_x , j_y, c_x, c_y)

        if ran and not alive_t and time.time() >= tree_respawn_time:
            alive_t = True
            t_x, t_y = creer_arbre()

        # kill the player if they touch the borders/water
        if j_x < 68 or j_x > LARGEUR - 68 or j_y > HAUTEUR - 115 or j_y < 68:
            quit_game(score, score_test)

        if ev.type == pygame.QUIT:
            quit_game(score, score_test)
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and dist !=0 and len(balles) < 3:
            dir_x /= dist
            dir_y /= dist
            balles.append([c_x, c_y, dir_x, dir_y])


    # player movement management according to the chosen control mode (ZQSD or WASD)
    touches = pygame.key.get_pressed()
    if control_mode == 0:
        dx = touches[pygame.K_d] - touches[pygame.K_q]
        dy = touches[pygame.K_s] - touches[pygame.K_z]
    else:
        dx = touches[pygame.K_d] - touches[pygame.K_a]
        dy = touches[pygame.K_s] - touches[pygame.K_w]


    # normalization of the movement vector to ensure consistent speed in all directions, and movement of the player according to this vector, while ensuring that the player does not go out of the screen boundaries.
    if dx != 0 or dy != 0:
        longueur = math.hypot(dx, dy)
        dx /= longueur
        dy /= longueur

    j_x += dx * v_joueur
    j_y += dy * v_joueur
    j_x = max(0, min(LARGEUR - j_w, j_x))
    j_y = max(0, min(HAUTEUR - j_h, j_y))



    # update the positions of the bullets and remove those that go out of the screen boundaries, while ensuring that the player can only have a maximum of 3 bullets on the screen at a time.
    nouvelles_balles = []
    for bx, by, dx, dy in balles:
        bx += dx * v_balle
        by += dy * v_balle
        if 0 < bx < LARGEUR and 0 < by < HAUTEUR:
            nouvelles_balles.append([bx, by, dx, dy])

    balles = nouvelles_balles

    ecran.blit(current_back, (0, 0)) # draw the current background based on the CO2 level
    # tree redimension and hitbox calculation
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
