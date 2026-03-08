import pygame
import sys
import subprocess

# initializing pygame
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont("Tahoma", 45)
pygame.mixer.init()

# Set up sound for click
click = pygame.mixer.Sound("assets/sounds/setting.mp3")
# load the mute setting from the text file
with open("controls.txt", "r") as f:
    lines = f.readlines()
    mute_setting = lines[5].strip()
click.set_volume(int(mute_setting) ^ 1)

# window settings
WIDTH = 1280
HEIGHT = 800
fenetre = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("treeboom")

# load and resize the background image
image1 = pygame.image.load("/assets/images/options-menu-tryout.png")
image1 = pygame.transform.scale(image1, (WIDTH, HEIGHT))

# toggle button settings
toggle_x = 265
toggle_y = 160
toggle_state = True
radius = 40
green = (0,255,0)
red = (255,0,0)
color = 0

# mute/unmute button settings
(mx, my) = pygame.mouse.get_pos()
button_1 = pygame.Rect(500, 100, 300, 120)  # Toggle button
mute_text = font.render("Mute / Unmute", True, (0, 0, 0))
mute_rect = mute_text.get_rect(midtop=(button_1.centerx, button_1.top))

# return menu button settings
button_rect = pygame.Rect(900, 100, 150, 20)
return_text = font.render("Return Menu", True, (0, 0, 0))
button_text_rect = return_text.get_rect(center=button_rect.center)

filename = "controls.txt"

# Main loop
running = True
while running:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            subprocess.Popen([sys.executable, "treeboom-menu.py"])
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mx, my) = pygame.mouse.get_pos()

            # check if the toggle button was clicked
            if (mx - toggle_x)**2 + (my - toggle_y)**2 <= radius**2:
                toggle_state = not toggle_state

                # rewrite the text file with the new value of the toggle state
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

            # check if the return menu button was clicked
            elif button_rect.collidepoint(event.pos):
                click.play()
                subprocess.Popen([sys.executable, "treeboom-menu.py"])
                running = False

            # check if the mute/unmute button was clicked
            elif button_1.collidepoint(event.pos):

                # rewrite the text file with the new value of the mute setting
                with open(filename, "r+") as f:
                    lines = f.readlines()

                    #invert the value of the mute setting
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



        # quit the game if the user clicks the close button
        if event.type == pygame.QUIT:
            running = False
    # fill the background with the image
    fenetre.blit(image1, (0, 0))


    # draw the toggle button with the appropriate color

    pygame.draw.circle(fenetre, (toggle_state*255, abs(1-toggle_state)*255, 0), (toggle_x, toggle_y), radius)

    # draw the mute/unmute button with the appropriate color
    mute_setting = int(mute_setting)
    pygame.draw.circle(fenetre, (mute_setting*255, abs(1-mute_setting)*255, 0), (640, 180), 20)

    # display the button texts
    fenetre.blit(mute_text, mute_rect)
    fenetre.blit(return_text, button_text_rect)

    # update the display
    pygame.display.flip()
    clock.tick(60)


pygame.quit()



