import sys

import pygame
import pygame.locals
import random


WIDTH, HEIGHT = 640, 480


class Player:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)

    def update(self, surface: pygame.Surface) -> None:
        self.x += self.vx
        self.y += self.vy
        pygame.draw.circle(surface, "#ff0000", (self.x, self.y), 30)

class Enemy:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)

    def update(self, surface: pygame.Surface) -> None:
        self.x += self.vx
        self.y += self.vy
        pygame.draw.circle(surface, "#ff0000", (self.x, self.y), 30)


def main():
    fps = 60
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    while True:
        screen.fill("#000000")
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()