
import pygame
import time


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((400, 300))
done = False

pygame.mixer.music.load("drum.wav")




######################################################change volum####################################

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button ==2:                                    # middle button to play music
                print('play')
                pygame.mixer.music.play(0)
                time.sleep(1)
            elif event.button ==1:                               # left button to change the position and the volume.(y direction)
                print('change volum')
                pygame.mixer.music.pause()
                mx, my = pygame.mouse.get_pos()
                print('position (x, y): ', mx, my)
                rate = my/300.0
                pygame.mixer.music.set_volume(rate)
                pygame.mixer.music.unpause()

    pygame.display.flip()

#######################################################################################################

