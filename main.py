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
        if keys_held[pygame.K_UP] or keys_held[pygame.K_w]:
            ay -= 1
        if keys_held[pygame.K_DOWN] or keys_held[pygame.K_s]:
            ay += 1
        if keys_held[pygame.K_LEFT] or keys_held[pygame.K_a]:
            ax -= 1
        if keys_held[pygame.K_RIGHT] or keys_held[pygame.K_d]:
            ax += 1
        if ax != 0 and ay != 0:
            acceleration = pygame.Vector2(ax, ay).clamp_magnitude(1)
            ax = acceleration.x
            ay = acceleration.y
        self.vx += ax
        self.vy += ay
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.8
        self.vy *= 0.8
        if self.x < self.screen.get_width()/32+self.r:
            self.x = self.screen.get_width()/32+self.r
        if self.x > self.screen.get_width()*31/32-self.r:
            self.x = self.screen.get_width()*31/32-self.r
        if self.y < self.screen.get_height()/32+self.r:
            self.y = self.screen.get_height()/32+self.r
        if self.y > self.screen.get_height()*31/32-self.r:
            self.y = self.screen.get_height()*31/32-self.r
        pygame.draw.circle(self.screen, "#1f74f5", (self.x, self.y), self.r)


class Enemy:

    def __init__(self, screen):
        self.r = 20
        self.x = 0
        self.y = 0
        self.vx = 1
        self.vy = 1
        self.r = 15
        self.health = 3
        self.screen = screen

    def update(self) -> None:
        self.x += self.vx
        self.vx *= 0.5
        self.vy *= 0.5
        pygame.draw.circle(self.screen, "#7b0a0a", (self.x, self.y), self.r)


class Projectile:
    def __init__(self, screen, start_pos, direction, damage) -> None:
        self.pos = pygame.Vector2(start_pos)
        self.direction = pygame.Vector2(direction).normalize()
        self.speed = 8
        self.r = 5
        self.screen = screen
        self.damage = damage
    
    def update(self):
        self.pos += self.direction*self.speed
        pygame.draw.circle(self.screen, "#1f74f5", (self.pos), self.r)

    def in_border(self) -> bool:
        if self.pos.x < self.screen.get_width()/32+self.r:
           return True
        if self.pos.x > self.screen.get_width()*31/32-self.r:
            return True
        if self.pos.y < self.screen.get_height()/32+self.r:
            return True
        if self.pos.y > self.screen.get_height()*31/32-self.r:
            return True
        return False


def main():
    fps = 60
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    square_length = screen.get_width()/16
    player = Player(screen)
    grid = [[0 for _ in range(16)] for _ in range(10)]
    bullets = []
    enemies = [Enemy(screen)]
    while True:
        screen.fill("#000000")
        for y, row in enumerate(grid):
            for x, value in enumerate(row):
                pygame.draw.rect(screen, (100, 100, 100), (x*square_length, y*square_length, square_length, square_length), 3)

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                bullets.append(Projectile(screen, (player.x, player.y), (event.pos[0]-player.x, event.pos[1]-player.y), 3))

        keys_held = pygame.key.get_pressed()
        player.update(keys_held)
        for enemy in enemies:
            enemy.update()
        for bullet in bullets.copy():
            bullet.update()
            for enemy in enemies.copy():
                if math.dist((bullet.pos), (enemy.x, enemy.y)) < bullet.r + enemy.r:
                    enemies[enemies.index(enemy)].health -= bullet.damage
                    if enemies[enemies.index(enemy)].health <= 0:
                        enemies.remove(enemy)
                    bullets.remove(bullet)
        bullets = [bullet for bullet in bullets if not bullet.in_border()]
    
        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()