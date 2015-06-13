#/usr/bin/python

import pygame
import sys
import math

pygame.init()
clock = pygame.time.Clock()

WINDOWSIZE = (576, 125)
screen = pygame.display.set_mode(WINDOWSIZE)
pygame.display.set_caption("Binary Counting")

SwitchPlates = pygame.sprite.Group()

font = pygame.font.Font(None, 24)

class SwitchPlate(pygame.sprite.Sprite):
    def __init__(self, color, left, top, width, height, BitNumber):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.color = color
        self.rect = (left, top, width, height)
        self.state = 0
        self.BitNumber = BitNumber
        self.image = pygame.Surface((width, height))
        self.rect = pygame.Rect((left, top, width, height))

    def update(self):
        if self.state == 0:
            self.color = (123,123,123)
        else:
            self.color = (0, 250, 125)
        pygame.draw.rect(screen, self.color, self.rect)
        xfont = pygame.font.Font(None, 18)
        label = xfont.render(str(self.BitNumber), 1, (255,255,0))
        screen.blit(label, self.rect.bottomleft)

    def click(self):
        if self.state == 1:
            self.state = 0
        else:
            self.state = 1

def GetBits(plates):
    sum = 0
    for p in plates:
        if p.state > 0:
            sum += (p.BitNumber * p.state)
    return str(sum)

SwitchPlate.groups = SwitchPlates

cSpacing = 7
dLeft = 7
dTop = 10
dWidth = 50
dHeight = 75
vLeft = dLeft

bNum = 1
for row in xrange(1, 11):
    NewRect = SwitchPlate((123,123,123), vLeft, dTop, dWidth, dHeight, bNum)
    SwitchPlates.add(NewRect)
    bNum *= 2
    vLeft = vLeft + dWidth + cSpacing


# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for sp in SwitchPlates:
                myMouse = pygame.mouse.get_pos()
                if sp.rect.collidepoint(myMouse[0], myMouse[1]):
                    sp.click()

        if event.type == pygame.KEYDOWN:
            pressedkeys = pygame.key.get_pressed()
            if pressedkeys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit(0)

    screen.blit(background, (0, 0))

    # Render Text
    label = font.render(GetBits(SwitchPlates), 1, (255,255,0))

    #Switchplates
    SwitchPlates.update()

    #Image transfer
    screen.blit(label, (WINDOWSIZE[0]/2, WINDOWSIZE[1]-21))
    pygame.display.flip()

