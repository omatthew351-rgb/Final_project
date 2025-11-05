import sys

import pygame
import pygame.locals
import random
import math


WIDTH, HEIGHT = 800, 600


class Player:

    def __init__(self, screen: pygame.Surface):
        self.x = screen.get_width() / 2
        self.y = screen.get_height() / 2
        self.vx = 0
        self.vy = 0
        self.health = 3
        self.screen = screen
        self.r = 20

    def update(self, keys_held: set[int]) -> None:
        ax, ay = 0, 0
        if keys_held[pygame.K_UP]:
            ay -= 0.5
        if keys_held[pygame.K_DOWN]:
            ay += 0.5
        if keys_held[pygame.K_LEFT]:
            ax -= 0.5
        if keys_held[pygame.K_RIGHT]:
            ax += 0.5
        if ax != 0 and ay != 0:
            acceleration = pygame.Vector2(ax, ay).clamp_magnitude(0.5)
            ax = acceleration.x
            ay = acceleration.y
        self.vx += ax
        self.vy += ay
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.9
        self.vy *= 0.9
        if self.x < self.screen.get_width()/32+self.r:
            self.x = self.screen.get_width()/32+self.r
        if self.x > self.screen.get_width()*31/32-self.r:
            self.x = self.screen.get_width()*31/32-self.r
        if self.y < self.screen.get_height()/32+self.r:
            self.y = self.screen.get_height()/32+self.r
        if self.y > self.screen.get_height()*31/32-self.r:
            self.y = self.screen.get_height()*31/32-self.r
        pygame.draw.circle(self.screen, "#ff0000", (self.x, self.y), self.r)


class Enemy:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.vx = 1
        self.vy = 1

    def update(self, surface: pygame.Surface) -> None:
        self.x += self.vx
        self.y += self.vy
        pygame.draw.circle(surface, "#00ff00", (self.x, self.y), 15)



def main():
    fps = 60
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    square_length = screen.get_width()/16
    player = Player(screen)
    grid = [[0 for _ in range(16)] for _ in range(10)]
    while True:
        screen.fill("#000000")
        for y, row in enumerate(grid):
            for x, idx in enumerate(row):
                pygame.draw.rect(screen, (100, 100, 100), (x*square_length, y*square_length, square_length, square_length), 3)

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        keys_held = pygame.key.get_pressed()
        player.update(keys_held)
    
        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()