import pygame
import sys
import math
import subprocess
import time
import random







# initialize pygame
pygame.init()
score = 0

#constants:
# Constants
CONTROL_FILE = "controls.txt"
SOUND_GAME_OVER = "game-over.mp3"
SOUND_HIT_ENEMY = "hit-enemy.mp3"
FONT_FILE = "04b_25__.ttf"

WIDTH, HEIGHT = 1280, 800
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
PLAYER_SPEED = 5
ball_speed = 12
MAX_BALLS = 3
MAX_AIM_DISTANCE = 40
AIM_POINT_RADIUS = 8
ENEMY_HIT_RADIUS = 30
TREE_HIT_RADIUS = 80
 
 # Initialize the mixer before loading sounds
pygame.mixer.init()
 
 # loads the sound files
game_over = pygame.mixer.Sound(SOUND_GAME_OVER)
hit_enemy = pygame.mixer.Sound(SOUND_HIT_ENEMY)

# read the mute setting and score from controls.txt
with open(CONTROL_FILE, "r") as f:
    lines = f.readlines()
    mute_setting = lines[5].strip()
    score_test = int(lines[7].strip())

# set the volume of the sounds according to the mute setting
game_over.set_volume(int(mute_setting) ^ 1)
hit_enemy.set_volume((int(mute_setting) ^ 1)*0.7)


# window settings
WIDTH, HEIGHT = 1280, 800
ecran = pygame.display.set_mode((WIDTH, HEIGHT))
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

def display_text(text, x, y, color):
    """
    This function displays text in a Pygame window starting from a given position (x, y). If a line of text exceeds the window width, it is automatically truncated and continued on the next line.

    Parameters:

    ------------
    text(str): The text to display.

    x(int): The position in pixels on the x-axis (horizontal) where the text begins to be displayed.

    y(int): The position in pixels on the y-axis (vertical) where the text begins to be displayed.

    color(tuple): A color defined as a tuple (R, G, B) for the text color.
    """


    assert type(text) == str, "this function only accepts string as input for the 'text' parameter."
    assert type(x) == int and type(y) == int, "this function only accepts integers for the 'x' and 'y' parameters."
    assert type(color) == tuple and len(color) == 3, "this function only accepts a tuple of three integers for the 'color' parameter."
    mots = text.split(' ')
    ligne_actuelle = ''
    y_offset = 0

    for mot in mots:
        # check if the current line plus the next word exceeds the window width
        if font.size(ligne_actuelle + mot)[0] <= WIDTH - x:
            ligne_actuelle += mot + ' '
        else:
            # Draw the current line and reset for the new line
            ecran.blit(font.render(ligne_actuelle.strip(), True, color), (x, y + y_offset))
            ligne_actuelle = mot + ' '
            y_offset += font.get_height()  # Increase the offset for the next line

    # Draw the last line if it is not empty
    if ligne_actuelle:
        ecran.blit(font.render(ligne_actuelle.strip(), True, color), (x, y + y_offset))




# game variables
co2 = 1
ran = True # for enemy respawn

# initial background
background0 = pygame.image.load("background-grey0.png")
background1 = pygame.image.load("background-grey1.png")
background2 = pygame.image.load("background-grey2.png")
background3 = pygame.image.load("background-grey3.png")
current_back = background0



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
    assert (type(j_x) == int or type(j_x) == float) and (type(j_y) == int or type(j_y) == float), "the parameters of the player's position must be integers or floats."
    assert (type(c_x) == int or type(c_x) == float) and (type(c_y) == int or type(c_y) == float), "the parameters of the bullet's position must be integers or floats."

    # we use global variables to manage the state of the enemy and the player's score, as well as the respawn logic for both the enemy and the tree.
    global alive, e_x, e_y, score, current_back, ran

    assert (type(e_x) == int or type(e_x) == float) and (type(e_y) == int or type(e_y) == float), "the parameters of the enemy's position must be integers or floats."
    assert type(score) == int, "the score must be an integer."
    assert type(alive) == bool, "the 'alive' variable must be a boolean."
    assert type(ran) == bool, "the 'ran' variable must be a boolean."


    # enemy behavior and collision detection
    if alive:
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
                temp = random.randint(0,3)
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

        if dist:
            dx, dy = dx / dist, dy / dist  # Normalising  the vector
        # speed of the enemy in function of this vector
        e_x += dx * speed
        e_y += dy * speed
        # draw the enemy on the screen
        ecran.blit(anti, (int(e_x), int(e_y)))



# player variables
j_w, j_h = PLAYER_WIDTH, PLAYER_HEIGHT
miku_img = pygame.transform.scale(miku_img, (j_w, j_h))# rezise the player image to fit the hitbox
j_x, j_y = WIDTH//2, HEIGHT//2
v_joueur = PLAYER_SPEED

# pointer variables
dist_max_point = 40
rayon_point = 8

# enemy variables
anti = pygame.image.load("anti-milo.png")
anti = pygame.transform.scale(anti, (80, 60))
e_x =550
e_y =800

# ball variables
balls = []
c_x = 0
c_y = 0


clock = pygame.time.Clock()

# properly quit the game and return to the menu, while saving the score if it is higher than the previous score stored in controls.txt
def quit_game(score, previous_score):
    assert type(score) == int and type(previous_score) == int , "The scores must be integers."
    if score > previous_score:
        # updates the score in controls.txt if the current score is higher than the previous score
        with open(CONTROL_FILE, "r+")as f:
            lines = f.readlines()
            lines[7] = str(score) + "\n"
            f.seek(0)
            f.writelines(lines)
            f.truncate()
    subprocess.Popen([sys.executable, "treeboom-menu.py"])
    alive = False
    sys.exit()







def create_tree(): # creation of the tree and random choice of its position among 6 predefined positions
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
        current_back = background3
    elif co2 >= 22:
        current_back = background2
    elif co2 >= 12:
        current_back = background1
    # otherwise we keep the base background (without gray)

    # random choice of the tree's position among 6 positions
    rd_tree = random.randint(1,6)

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
t_x, t_y = create_tree()



# choice of the control mode (ZQSD or WASD) based on the settings stored in controls.txt, and management of the player's movement according to the chosen control mode.
with open("controls.txt", "r") as f:
    lines = f.readlines()
    control_mode = int(lines[1].strip())

# respawn variables
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

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
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
            # the reticle points downwards
            damazon = damazon_down
        elif angle >= 135 or angle < -135:
            # the reticle points to the left
            damazon = damazon_left
        elif angle >= -135 and angle < -45:
            # the reticle points upwards
            damazon = damazon_up
        elif angle >= -45 and angle < 45:
            # the reticle points to the right
            damazon = damazon_right


        if not alive and not ran:
            ran = True
            enemy_respawn_time = time.time() + random.randint(1, 7)  #  arbitrary respawn time for the enemy
        if not alive_t and not ran_t:
            ran_t = True
            tree_respawn_time = time.time() + random.randint(0, 3)  #  arbitrary respawn time for the tree

        # we check if the respawn timers for the enemy and the tree have elapsed, and if so, we set them to alive again and call the enemy function to respawn the enemy at a new position, and we call the creer_arbre function to respawn the tree at a new position.
        if ran and not alive and time.time() >= enemy_respawn_time:
            alive = True

            enemy(j_x , j_y, c_x, c_y)

        if ran_t and not alive_t and time.time() >= tree_respawn_time:
            alive_t = True
            t_x, t_y = create_tree()

        # kill the player if they touch the borders/water
        if j_x < 68 or j_x > WIDTH - 68 or j_y > HEIGHT - 115 or j_y < 68:
            quit_game(score, score_test)

        if event.type == pygame.QUIT:
            quit_game(score, score_test)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and dist !=0 and len(balls) < 3:
            dir_x /= dist
            dir_y /= dist
            balls.append([c_x, c_y, dir_x, dir_y])


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
    j_x = max(0, min(WIDTH - j_w, j_x))
    j_y = max(0, min(HEIGHT - j_h, j_y))



    # update the positions of the bullets and remove those that go out of the screen boundaries, while ensuring that the player can only have a maximum of 3 bullets on the screen at a time.
    nouvelles_balles = []
    for bx, by, dx, dy in balls:
        bx += dx * ball_speed
        by += dy * ball_speed
        if 0 < bx < WIDTH and 0 < by < HEIGHT:
            nouvelles_balles.append([bx, by, dx, dy])

    balls = nouvelles_balles

    ecran.blit(current_back, (0, 0)) # draw the current background based on the CO2 level
    # tree redimension and hitbox calculation
    t_w, t_h = smol_tree.get_width(), smol_tree.get_height()
    t_c_x = t_x + t_w / 2
    t_c_y = t_y + t_h / 2


    # tree collision detection with bullets
    for bx, by, _, _ in nouvelles_balles:
        dist_tree = math.hypot(bx - t_c_x, by - t_c_y)
        if dist_tree < 80:
            if alive_t:
                co2 += 1


            # we prepare the respawn of the tree
            alive_t = False
            ran_t= False 
            break

    # display the tree on the screen if it is alive
    if alive_t:
        ecran.blit(smol_tree, (t_x, t_y))



    # we call the enemy once at the beginning of the game to initialize its position and behavior
    enemy(j_x , j_y, c_x, c_y)


    # player display
    ecran.blit(miku_img, (int(j_x), int(j_y)))

    # aiming reticle (damazon) display, which follows the mouse position while maintaining a maximum distance from the center of the player
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



    # show the bullets on the screen
    for bx, by, _, _ in balls:
        ecran.blit(damazon, (int(bx), int(by)))

    # text display for score, number of bullets, and CO2 level

    display_text( "score :", 150, 0, (255, 255, 255))
    display_text( "cartons :", 550, 0, (255, 255, 255))
    display_text( "co2 level:", 910, 750, (255, 255, 255))


    display_text(str(co2), 1090, 750, (255, 255, 255))
    display_text( str(score), 260, 0, (255, 255, 255))
    display_text( str(3-len(nouvelles_balles))+ " /3", 660, 0, (255, 255, 255))

    # button to return to the menu
    ecran.blit(return_text, button_text_rect)

    # screen update
    pygame.display.flip()

    clock.tick(60)# END OF MAIN LOOP----------------------------------------------------------------------------------


pygame.quit()
