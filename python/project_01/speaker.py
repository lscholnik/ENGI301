'''
speaker driver



#from playsound import playsound
if __name__ == '__main__':
    try:
        mplayer('Dustin.mp3')
    
    except KeyboardInterrupt:
        pass
'''

import pygame
pygame.mixer.init()
pygame.mixer.music.load("Dustin.mp3")
pygame.mixer.music.play()
#**Loop while playing**
pygame.mixer.stop()
pygame.mixer.quit()