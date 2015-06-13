## http://stackoverflow.com/questions/16381020/basic-pygame-graphics
## 5/5/2013
## Pradyun

import pygame, itertools

R = (255, 0, 0)
O = (255, 127, 0)
Y = (255, 255, 0)
G = (0, 255, 0)
B = (0, 0, 255)
I = (75, 0, 130)
V = (143, 0, 255)

FADE_SPEED = 320 # no of frames for shifting
colors = (R, O, Y, G, B, I, V) # to allow you to iterate over the colors
cycle = itertools.cycle(colors)

def FadingRainbow(c1, c2, n=FADE_SPEED):
    """ Give the next color to draw \n"""
    "Args: c1,c2 => colors, n => int"
    dif = [(c1[i]-c2[i])/float(n) for i in range(3)] # calculate the per-frame difference
    return [c1[i]-dif[i] for i in range(3)] # subtract that difference


if __name__ == '__main__':  # Begin demo code
    ## needed for fading
    c_color = cycle.next() # RED    current_color
    n_color = cycle.next() # BLACK  next_color
    frames = FADE_SPEED
    ## --------------

    SIZE = (1000,1000)
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock() # regulate fps

    while True:
        # handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # close window event
                pygame.quit()

        c_color = FadingRainbow(c_color, n_color, frames) # get next color

        pygame.draw.circle(screen, map(int, c_color), (500, 500), 200)
        pygame.display.flip()

        frames -= 1
        if frames == 0: # translation complete
            frames = FADE_SPEED
            n_color = cycle.next() # get next color

        clock.tick(40) # run at maximum of 40 frames per second