#/usr/bin/python

import pygame
import sys
#import math
import random
import AnimatedRainbow

pygame.init()
clock = pygame.time.Clock()

CongratFlag = False
Score = 0
WINDOWSIZE = (1024, 250)
SwitchColorON = (153, 153, 0)
SwitchColorOFF = (20,20,20)
RainbowColorEffect = (0,0,0)
r = g = b = 0
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
        global RainbowColorEffect
        if self.state == 0:
            self.color = SwitchColorOFF
        else:
            self.color = RainbowColorEffect
        pygame.draw.rect(screen, self.color, self.rect)
        xfont = pygame.font.Font(None, 18)
        label = xfont.render(str(self.BitNumber), 1, RainbowColorEffect)
        screen.blit(label, self.rect.bottomleft)

    def click(self):
        if self.state == 1:
            self.state = 0
        else:
            self.state = 1

def RenderScreen():
    global CongratFlag, MyRandomNumber, Score, MAXRANDOM
    global RainbowColorEffect
    screen.blit(background, (0, 0))
    CurrentBinarySum = str(GetBits(SwitchPlates))
    TextBinarySum = font.render(CurrentBinarySum, 1, RainbowColorEffect)
    if CongratFlag != True:
        # Render Text
        RainbowColorEffect = GetRainbowEffect()
        if int(CurrentBinarySum) > MyRandomNumber:
            TextHint = font.render("Too High.", 1, RainbowColorEffect)
        elif int(CurrentBinarySum) < MyRandomNumber:
            TextHint = font.render("Too Low.", 1, RainbowColorEffect)
        elif int(CurrentBinarySum) == MyRandomNumber:
            TextHint = font.render("You Win!", 1, RainbowColorEffect)
            #MyRandomNumber = random.randrange(1, MAXRANDOM+1)
            #TurnAllSwitchPlatesOff(SwitchPlates)
            #Score += 1
            #CongratFlag = True

        #Render Switchplates
        SwitchPlates.update()
        TextScore = font.render("Score: " + str(Score), 1, RainbowColorEffect)
        #Image transfer
        screen.blit(TextBinarySum, (WINDOWSIZE[0]/2, WINDOWSIZE[1]-21))
        screen.blit(TextHint, (25, WINDOWSIZE[1]-21))
        screen.blit(TextScore, (WINDOWSIZE[0]-100, WINDOWSIZE[1]-21))

        #render dividor
        pygame.draw.line(screen, RainbowColorEffect, (0, WINDOWSIZE[1] - 25), (WINDOWSIZE[0], WINDOWSIZE[1]-25))
        #apply
        pygame.display.flip()

def GetRainbowEffect():
    global c_color, n_color, frames
    c_color = AnimatedRainbow.FadingRainbow(c_color, n_color, frames) # get next color
    return map(int, c_color)

def TurnAllSwitchPlatesOff(plates):
    for p in plates:
        p.state = 0

def GetBits(plates):
    sum = 0
    for p in plates:
        if p.state > 0:
            sum += (p.BitNumber * p.state)
    return sum

SwitchPlate.groups = SwitchPlates

#build switches
rows = 3
cSpacing = 7
dLeft = 7
dTop = 10
dWidth = (WINDOWSIZE[0] - 75) / 10
dHeight = (WINDOWSIZE[1] - 25) / rows
vLeft = dLeft
vTop = dTop

bNum = 1
for col in xrange(1, rows):
    for row in xrange(1, 11):
        NewRect = SwitchPlate(SwitchColorOFF, vLeft, vTop, dWidth, dHeight, bNum)
        SwitchPlates.add(NewRect)
        bNum *= 2
        vLeft = vLeft + dWidth + cSpacing
    vLeft = dLeft
    vTop = vTop + dHeight + (cSpacing * 3)


# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))


#get the max random number dynamically
MAXRANDOM = 0
for p in SwitchPlates:
    MAXRANDOM += p.BitNumber
MyRandomNumber = random.randrange(1, MAXRANDOM+1)
MyRandomNumber = 0


#precode for rainbow effects
c_color = AnimatedRainbow.cycle.next() # RED    current_color
n_color = AnimatedRainbow.cycle.next() # BLACK  next_color
frames = AnimatedRainbow.FADE_SPEED
## --------------

MyBinary = '{0:020b}'.format(MyRandomNumber)[::-1]
#print MyBinary
i = 0
iNum = 1
while i < 20:
    for p in SwitchPlates:
        if p.BitNumber == iNum:
            p.state = int(MyBinary[i])
            i += 1
            iNum *= 2

#print MyBinary



while True:
    MyRandomNumber += 1

    #Event Handleing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            MyRandomNumber += 1
            for sp in SwitchPlates:
                myMouse = pygame.mouse.get_pos()
                if sp.rect.collidepoint(myMouse[0], myMouse[1]):
                    CongratFlag = False
                    sp.click()

        if event.type == pygame.KEYDOWN:
            pressedkeys = pygame.key.get_pressed()
            if pressedkeys:
                if pressedkeys[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit(0)

    MyBinary = '{0:020b}'.format(MyRandomNumber)[::-1]
    #print MyBinary
    i = 0
    iNum = 1
    while i < 20:
        for p in SwitchPlates:
            if p.BitNumber == iNum:
                p.state = int(MyBinary[i])
                i += 1
                iNum *= 2



    #Rendering
    frames -= 1
    if frames == 0: # translation complete
        frames = AnimatedRainbow.FADE_SPEED
        n_color = AnimatedRainbow.cycle.next() # get next color
    RenderScreen()