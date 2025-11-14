import sys

import pygame
import pygame.locals
import random
import math


WIDTH, HEIGHT = 800, 600


class Player:

    def __init__(self, screen: pygame.Surface):
        self.x = screen.get_width() / 2
        self.y = screen.get_height() / 2 + 200
        self.vx = 0
        self.vy = 0
        self.health = 6
        self.screen = screen
        self.r = 20
        self.tile_length = self.screen.get_height() / 10
        self.weapon = Weapon(5, 1, 5, 5)


    def update(self, keys_held: set[int], door_open=False) -> None:
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

        if door_open:
            if not (
                self.tile_length * 4 + self.r < self.y < self.tile_length * 6 - self.r
            ):  # check in door

                if self.x < self.tile_length / 2 + self.r:
                    if not (
                        self.tile_length * 4 + self.r
                        < self.y - self.vy / 4 * 5
                        < self.tile_length * 6 - self.r
                    ):  # if was not in door before, normal else push back in the door
                        self.x = self.tile_length / 2 + self.r
                        self.vx = 0
                    else:
                        self.y = max(
                            self.tile_length * 4 + self.r,
                            min(self.tile_length * 6 - self.r, self.y),
                        )

                if self.x > self.screen.get_width() - self.tile_length / 2 - self.r:
                    if not (
                        self.tile_length * 4 + self.r
                        < self.y - self.vy / 2 * 5
                        < self.tile_length * 6 - self.r
                    ):
                        self.x = self.screen.get_width() - self.tile_length / 2 - self.r
                        self.vx = 0
                    else:
                        self.y = max(
                            self.tile_length * 4 + self.r,
                            min(self.tile_length * 6 - self.r, self.y),
                        )

            if not (
                self.tile_length * 7 + self.r < self.x < self.tile_length * 9 - self.r
            ):

                if self.y < self.tile_length / 2 + self.r:
                    if not (
                        self.tile_length * 7 + self.r
                        < self.x - self.vx / 4 * 5
                        < self.tile_length * 9 - self.r
                    ):
                        self.y = self.tile_length / 2 + self.r
                        self.vy = 0
                    else:
                        self.x = max(
                            self.tile_length * 7 + self.r,
                            min(self.tile_length * 9 - self.r, self.x),
                        )
                if self.y > self.screen.get_height() - self.tile_length / 2 - self.r:
                    if not (
                        self.tile_length * 7 + self.r
                        < self.x - self.vx / 4 * 5
                        < self.tile_length * 9 - self.r
                    ):
                        self.y = (
                            self.screen.get_height() - self.tile_length / 2 - self.r
                        )
                        self.vy = 0
                    else:
                        self.x = max(
                            self.tile_length * 7 + self.r,
                            min(self.tile_length * 9 - self.r, self.x),
                        )

        else:

            if self.x < self.tile_length / 2 + self.r:
                self.x = self.tile_length / 2 + self.r
                self.vx = 0
            elif self.x > self.screen.get_width() - self.tile_length / 2 - self.r:
                self.x = self.screen.get_width() - self.tile_length / 2 - self.r
                self.vx = 0

            if self.y < self.tile_length / 2 + self.r:
                self.y = self.tile_length / 2 + self.r
                self.vy = 0
            if self.y > self.screen.get_height() - self.tile_length / 2 - self.r:
                self.y = self.screen.get_height() - self.tile_length / 2 - self.r
                self.vy = 0

        self.vx *= 0.8
        self.vy *= 0.8

        pygame.draw.circle(self.screen, "#1f74f5", (self.x, self.y), self.r)
        


class Enemy:

    def __init__(self, screen, r=20, health=3, speed=3, damage=1, cooldown=1):
        self.x = random.uniform(50, screen.get_width() - 50)
        self.y = random.uniform(50, screen.get_height() / 2)
        self.r = r
        self.health = health
        self.screen = screen
        self.damage = 1 
        self.cooldown = cooldown
        self.speed = random.choice([1, 3])
        self.last_attack_time = -1000
        # if self.speed == 0:
        #     self.color = (128, 128, 128)
        #     self.damage = 5
        #     self.cooldown = 1000
        if self.speed == 1:
            self.color = (255, 0, 0)
            self.health = 5
            self.damage = 1
            self.cooldown = 1000
        # elif self.speed == 2:
        #     self.color = (255, 255, 0)
        #     self.damage = 2
        #     self.cooldown = 1500
        elif self.speed == 3:
            self.color = (0, 255, 0)
            self.damage = 1
            self.health = 3
            self.cooldown = 1000

    def update(self, player_x, player_y) -> None:
        dist_x = player_x - self.x
        dist_y = player_y - self.y
        length = math.sqrt(dist_x**2 + dist_y**2)
        self.x += dist_x / length * self.speed
        self.y += dist_y / length * self.speed
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        health_bar_length = 30
        health_bar_height = 5
        health_bar_x = self.x - health_bar_length / 2
        health_bar_y = self.y - self.r - 10
        pygame.draw.rect(
            self.screen,
            "#ff0000",
            (health_bar_x, health_bar_y, health_bar_length, health_bar_height),
        )
        pygame.draw.rect(
            self.screen,
            "#00ff00",
            (
                health_bar_x,
                health_bar_y,
                health_bar_length * (self.health / 3),
                health_bar_height,
            ),
        )

class Projectile:
    def __init__(self, screen, start_pos, direction, damage) -> None:
        self.pos = pygame.Vector2(start_pos)
        self.direction = pygame.Vector2(direction).normalize()
        self.speed = 8
        self.r = 5
        self.screen = screen
        self.damage = damage

    def update(self):
        self.pos += self.direction * self.speed
        pygame.draw.circle(self.screen, "#1f74f5", (self.pos), self.r)

    def in_border(self) -> bool:
        if self.pos.x < self.screen.get_width() / 32 + self.r:
            return True
        if self.pos.x > self.screen.get_width() * 31 / 32 - self.r:
            return True
        if self.pos.y < self.screen.get_height() / 32 + self.r:
            return True
        if self.pos.y > self.screen.get_height() * 31 / 32 - self.r:
            return True
        return False


class Weapon:
    def __init__(self, damage=3, cooldown=0, reload_time=0, max_bullet=1) -> None:
        self.damage = damage
        self.cooldown = cooldown
        self.reload_time = reload_time
        self.bullet_count = max_bullet
        self.max_bullet = max_bullet


def generate_enemies(screen, room_num=1, difficulty=1) -> list[Enemy]:
    enemies = []
    for _ in range(room_num + difficulty):
        enemies.append(Enemy(screen))

    return enemies

def change_room(screen, player, old_grid, new_grid, room_number, direction):
    old_room = pygame.Surface((screen.get_width(), screen.get_height()))
    new_room = pygame.Surface((screen.get_width(), screen.get_height()))
    draw_background(old_room, old_grid, room_number)
    draw_background(new_room, new_grid, room_number+1)
    
    for offset in range(0, max(screen.get_height()*abs(direction[1]), screen.get_width()*abs(direction[0])), 2):
        screen.blits(
            [(old_room, (direction[0]*offset, direction[1]*offset)), (new_room, (direction[0]*(offset-screen.get_width()), direction[1]*(offset - screen.get_height())))]
        )
        pygame.draw.circle(screen, "#1f74f5", (player.x + offset*direction[0], player.y + offset*direction[1]), player.r)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    
    player.x += screen.get_width()*direction[0]
    player.y += screen.get_height()*direction[1]

def draw_background(screen, grid, room_number):
    screen.fill((100, 100, 100))
    square_length = screen.get_width() / 16
    pygame.draw.rect(
        screen,
        ("#000000"),
        (square_length / 2, square_length / 2, square_length * 15, square_length * 9),
    )

    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value == 0:
                pygame.draw.rect(
                    screen,
                    (100, 100, 100),
                    (
                        x * square_length,
                        y * square_length,
                        square_length,
                        square_length,
                    ),
                    3,
                )
            elif value == 1:
                pygame.draw.rect(screen, (200, 200, 200), (x*square_length, y*square_length, square_length, square_length))
    my_font = pygame.font.SysFont('Comic Sans MS', 250)
    text = my_font.render(str(room_number), True, (255, 255, 255))
    textpos = text.get_rect(centerx=screen.get_width() / 2, centery=screen.get_height() / 2)
    screen.blit(text, textpos)

def main():
    fps = 60
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    room_number = 1
    player = Player(screen)
    grid = [[0 for _ in range(16)] for _ in range(10)]
    grid[3][5] = 1
    bullets = []
    enemies: list[Enemy] = []#generate_enemies(screen, 5)

    while player.health > 0:
        draw_background(screen, grid, room_number)

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                bullets.append(Projectile(screen, (player.x, player.y), (event.pos[0]-player.x, event.pos[1]-player.y), player.weapon.damage))

        keys_held = pygame.key.get_pressed()
        player.update(keys_held, len(enemies) == 0)
        if len(enemies) == 0:
            if player.y+player.r < 0:
                direction = (0, 1)
                change_room(screen, player, grid, grid, room_number, direction)
                room_number += 1
                enemies = generate_enemies(screen, room_number)
            elif player.y-player.r > screen.get_height():
                direction = (0, -1)
                change_room(screen, player, grid, grid, room_number, direction)
                room_number += 1
                enemies = generate_enemies(screen, room_number)
            if player.x+player.r < 0:
                direction = (1, 0)
                change_room(screen, player, grid, grid, room_number, direction)
                room_number += 1
                enemies = generate_enemies(screen, room_number)
            elif player.x-player.r > screen.get_width():
                direction = (-1, 0)
                change_room(screen, player, grid, grid, room_number, direction)
                room_number += 1
                enemies = generate_enemies(screen, room_number)

        for enemy in enemies:
            enemy.update(player.x, player.y)
            if (
                math.dist((player.x, player.y), (enemy.x, enemy.y)) < player.r + enemy.r
                and pygame.time.get_ticks() - enemy.last_attack_time > enemy.cooldown
            ):
                player.health -= enemy.damage
                enemy.last_attack_time = pygame.time.get_ticks()

        for bullet in bullets.copy():
            bullet.update()
            for enemy in enemies.copy():
                if math.dist((bullet.pos), (enemy.x, enemy.y)) < bullet.r + enemy.r:
                    enemies[enemies.index(enemy)].health -= bullet.damage
                    if enemies[enemies.index(enemy)].health <= 0:
                        enemies.remove(enemy)
                    bullets.remove(bullet)
                    break
        bullets = [bullet for bullet in bullets if not bullet.in_border()]
    
        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()