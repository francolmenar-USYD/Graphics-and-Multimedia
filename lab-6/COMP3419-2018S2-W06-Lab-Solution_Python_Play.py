import pygame, Pyglet
import time

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((400, 300))
done = False

pygame.mixer.music.load("/Users/fran/Documents/UC3M/Graph/lab6/drum.wav")

#######################################play, pause and unpause###########################################

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:  # Three buttons
            if event.button == 2:  # middle to play music
                print('play')
                pygame.mixer.music.play(0)
                time.sleep(1)
            elif event.button == 1:  # Left to pause
                print('pause')
                pygame.mixer.music.pause()
            else:  # Right to play again
                print('play again')
                pygame.mixer.music.unpause()
    pygame.display.flip()

##########################################################################################################
