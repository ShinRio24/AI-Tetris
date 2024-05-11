import pygame
screen=pygame.display.set_mode([1300, 750])
screen.fill([255, 255, 255])
red=255
blue=0
green=0
left=50
top=50
width=15
height=5
filled=0
pygame.draw.rect(screen, [red, blue, green], [left, top, width, height], filled)
pygame.display.flip()
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
pygame.quit()