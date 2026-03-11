import pygame
import sys
import subprocess

# Set up sound for name input
pygame.mixer.init()
sound = pygame.mixer.Sound("assets/sounds/setting.mp3")
with open("controls.txt", "r") as f:
    lines = f.readlines()
    mute_setting = lines[5].strip()
sound.set_volume(int(mute_setting) ^ 1)  # invert mute setting

# Secure text file
filename = "controls.txt"

# Rewrite the file with default values
with open(filename, "w") as f:
    f.write("wasd or zqsd (0 is wasd 1 is zqsd):\n1\nname:\nplaceholder\nMute/Unmute (0 is unmute 1 is mute):\n0\npoints:\n0\n")

if not pygame.mixer.get_init():
    pygame.mixer.init()

# Pygame initialization
pygame.init()

# Window settings
WIDTH = 1280
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Adventure")

clock = pygame.time.Clock()

# Text font
font = pygame.font.Font("04b_25__.ttf", 30)

# Color variables used in the program
BLUE = (116, 208, 241)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load and resize an image
image1 = pygame.image.load("/assets/imagesmenu-img-2.png")
image1 = pygame.transform.scale(image1, (WIDTH, HEIGHT))

# Game variables
input_active = False
player_name = ""

def display_text(text, x, y, color):
    """
    Displays text in a Pygame window starting at a given
    position (x, y). If a line of text exceeds the window width, 
    it is automatically wrapped to the next line.
    """
    assert type(text) == str, "Parameter 'text' must be a string."
    assert type(x) == int and type(y) == int, "Parameters 'x' and 'y' must be integers."
    assert type(color) == tuple and len(color) == 3, "Parameter 'color' must be an RGB tuple."

    words = text.split(' ')
    current_line = ''
    y_offset = 0

    for word in words:
        # check if the word fits on the current line
        if font.size(current_line + word)[0] <= WIDTH - x:
            current_line += word + ' '
        else:
            # draw the current line and start a new one
            window.blit(font.render(current_line.strip(), True, color), (x, y + y_offset))
            current_line = word + ' '
            y_offset += font.get_height()

    # draw the last line if it is not empty
    if current_line:
        window.blit(font.render(current_line.strip(), True, color), (x, y + y_offset))

def input_text(x, y, width, height, bg_color, text_color):
    """
    Handles user text input inside a defined text box.
    The user types until pressing "Enter", which ends the input.
    """
    assert type(x) == int and type(y) == int, "Parameters 'x' and 'y' must be integers."
    assert type(width) == int and type(height) == int, "Parameters 'width' and 'height' must be integers."
    assert type(bg_color) == tuple and len(bg_color) == 3, "Parameter 'bg_color' must be an RGB tuple."
    assert type(text_color) == tuple and len(text_color) == 3, "Parameter 'text_color' must be an RGB tuple."

    global input_active
    input_active = True
    text = ""

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    # limit text length to 48 characters
                    if len(text) < 48 and event.unicode.isprintable():
                        text += event.unicode
                        sound.play()

        # Draw the text box
        pygame.draw.rect(window, bg_color, (x, y, width, height))

        # Display typed text
        text_surface = font.render(text + "_", True, text_color)
        window.blit(text_surface, (x + 10, y + 10))

        pygame.display.flip()

finished = False

# Main game loop
while not finished:

    # Event handling
    for event in pygame.event.get():

        # If user clicks close button, exit game
        if event.type == pygame.QUIT:
            finished = True
            pygame.quit()
            sys.exit()

    # Fill the screen with blue
    window.fill(BLUE)

    # Display the image at (0,0)
    window.blit(image1, (0, 0))

    # If the player name has not been entered
    if player_name == "":
        # Ask and get the player's name
        display_text("What is", 275, 300, BLACK)
        display_text("your name?", 275, 330, BLACK)
        player_name = input_text(200, 500, 800, 50, WHITE, BLUE)

        # Check for troll name "jade"
        if "jade" in player_name:
            print(""" \033[31mTraceback (most recent call last):
File "D:/treeboomPEAK WITH SAVE ONE/intro.py", line 165, in <name>
    jade
pygame.error: user name is too short\033[0m""")
            finished = True
            pygame.quit()
            sys.exit()

        elif player_name.strip() == "placeholder":
            print("Name reserved error, please choose another name")
            player_name = ""

        # If name is valid, save it to the txt file
        else:
            if player_name != "":
                filename = "controls.txt"
                with open(filename, "r+") as f:
                    lines = f.readlines()
                    lines[3] = player_name + "\n"

                    f.seek(0)
                    f.writelines(lines)
                    f.truncate()

                    subprocess.Popen([sys.executable, "treeboom-menu.py"])
                    finished = True

    pygame.display.flip()
    clock.tick(60)  # 60 FPS cap

pygame.quit()
sys.exit()
