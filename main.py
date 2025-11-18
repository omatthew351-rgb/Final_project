import sys

import pygame
import pygame.locals
import random
import math
import time




WIDTH, HEIGHT = 800, 500
#  r=20, health=3, speed=3, damage=1, cooldown=1000, color=(255, 0, 0), special_tags=None
ENEMY_TYPES = {
    1: [1, 15, 3, 3, 1, 1000, (255, 0, 0)],
    2: [2, 20, 10, 1.5, 1, 1000, (0, 255, 0)],
    3: [3, 15, 5, 1, 1, 3000, (0, 0, 255), ["ranged"]],
}

difficulty = [1, 2, 3, 4]
Player_reload = pygame.USEREVENT + 0
enemy_bullets = []

pygame.font.init()
room_number_font = pygame.font.SysFont("Comic Sans MS", 200)
difficulty_font = pygame.font.SysFont("Comic Sans MS", 20)

# player_img = pygame.transform.scale(pygame.image.load('player.png'), (64, 64))
floor_img = pygame.image.load('floor.png')
left_wall_img = pygame.image.load('left_wall.png')
top_wall_img = pygame.image.load('top_wall.png')
bottom_wall_img = pygame.image.load('bottom_wall.png')
left_top_corner_img = pygame.image.load('left_top_corner.png')
left_bottom_corner_img = pygame.image.load('left_bottom_corner.png')
heart_img = pygame.image.load('2025_11_17_0j9_Kleki.png')
dead_heart_img = heart = pygame.image.load('dead_heart.png')
bullet = pygame.image.load('2025_11_18_0i8_Kleki.png')
player_sprite = pygame.image.load('pixilart-drawing (1).png')
enemy_sprite = pygame.image.load('pixil-frame-0.png')


class Player:
    def __init__(self, screen: pygame.Surface):
        self.x = screen.get_width() / 2
        self.y = screen.get_height() / 2
        self.vx = 0
        self.vy = 0
        self.health = 3
        self.max_health = self.health
        self.screen = screen
        self.tile_length = self.screen.get_height() / 10
        self.speed = self.tile_length/200
        self.r = self.tile_length/3
        self.weapon = Weapon(3, 1000, 3000, 5)
        self.last_upgrade = -3000
        self.upgrade_text = difficulty_font.render("No Upgrade", True, (255, 255, 255))

    def update(self, keys_held: set[int] | None = None, door_open=False) -> None:
        ax, ay = 0, 0
        if keys_held is not None:
            if keys_held[pygame.K_UP] or keys_held[pygame.K_w]:
                ay -= self.speed
            if keys_held[pygame.K_DOWN] or keys_held[pygame.K_s]:
                ay += self.speed
            if keys_held[pygame.K_LEFT] or keys_held[pygame.K_a]:
                ax -= self.speed
            if keys_held[pygame.K_RIGHT] or keys_held[pygame.K_d]:
                ax += self.speed
            if ax != 0 and ay != 0:
                acceleration = pygame.Vector2(ax, ay).clamp_magnitude(self.speed)
                print(acceleration)
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

            self.vx *= 0.9
            self.vy *= 0.9

        # pygame.draw.rect(self.screen, "#1f74f5", (self.x-self.r, self.y-self.r, 2*self.r, 2*self.r))
        
        self.screen.blit(player_sprite, (self.x-self.r, self.y-self.r))

        # pygame.draw.rect(self.screen, "#00ff00", (5, 5, 20, 20))
        # pygame.draw.rect(self.screen, "#00ff00", (55, 5, 20, 20))
        # pygame.draw.rect(self.screen, "#00ff00", (105, 5, 20, 20))
        # if self.health == 2:
        #     pygame.draw.rect(self.screen, "#ff0000", (105, 5, 20, 20))
        # if self.health == 1:
        #     pygame.draw.rect(self.screen, "#ff0000", (55, 5, 20, 20))
        #     pygame.draw.rect(self.screen, "#ff0000", (105, 5, 20, 20))                      
        
        for i in range(self.max_health):
            self.screen.blit(dead_heart_img, (5+self.tile_length*i, self.tile_length/10))
        for i in range(self.health):
            self.screen.blit(heart_img, (5+self.tile_length*i, self.tile_length/10))

        scaled_bullet = pygame.transform.scale(bullet, (self.tile_length, self.tile_length))
        for i in range(self.weapon.bullet_count):
            self.screen.blit(scaled_bullet, (self.screen.get_width()-(i+1.5)*self.tile_length/2, 5))

        if pygame.time.get_ticks() - self.last_upgrade < 3000:
            textpos = self.upgrade_text.get_rect(
            centerx=self.x, centery=self.y - 2*self.r
            )
            self.screen.blit(self.upgrade_text, textpos)

    def upgrade(self, upgrade):
        self.last_upgrade = pygame.time.get_ticks()
        print(upgrade)
        if upgrade == 1:
            self.weapon.damage *= 1.1
            self.upgrade_text = difficulty_font.render("Bullet damage increased", True, (255, 255, 255))
        elif upgrade == 2:
            self.weapon.reload_time *= 0.9
            self.upgrade_text = difficulty_font.render("Reload time decreased", True, (255, 255, 255))
        elif upgrade == 3:
            self.weapon.cooldown *= 0.9
            self.upgrade_text = difficulty_font.render("Shooting cooldown decreased", True, (255, 255, 255))
        elif upgrade == 4:
            self.weapon.max_bullet += 2
            self.upgrade_text = difficulty_font.render("Bullet count increased", True, (255, 255, 255))
        elif upgrade == 5:
            self.speed += 0.1
            self.upgrade_text = difficulty_font.render("Speed increased", True, (255, 255, 255))
        
class Projectile:
    def __init__(self, screen, start_pos, direction, damage) -> None:
        self.pos = pygame.Vector2(start_pos)
        self.direction = pygame.Vector2(direction).normalize()
        self.tile_length = screen.get_width()/16
        self.speed = self.tile_length/6
        self.r = self.tile_length/12
        self.screen = screen
        self.damage = damage

    def update(self, color="#1f74f5"):
        self.pos += self.direction * self.speed
        pygame.draw.circle(self.screen, color, (self.pos), self.r)

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


class Enemy:
    def __init__(
        self,
        screen,
        enemy_type,
        r=20,
        health=3,
        speed=3,
        damage=1,
        cooldown=1000,
        color=(255, 0, 0),
        special_tags=None,
    ):
        self.x = random.uniform(50, screen.get_width() - 50)
        self.y = random.uniform(50, screen.get_height() - 50)
        self.type = enemy_type
        self.r = r
        self.health = health
        self.max_health = health
        self.screen = screen
        self.tile_length = self.screen.get_height() / 10
        self.damage = damage
        self.cooldown = cooldown
        self.speed = speed*self.tile_length/60
        self.last_attack_time = pygame.time.get_ticks()
        self.color = color
        self.special_tags = [] if special_tags is None else special_tags
        self.r = self.r/60*self.tile_length

    def update(self, player_x, player_y) -> None:
        global enemy_bullets
        dist_x = player_x - self.x
        dist_y = player_y - self.y
        length = math.sqrt(dist_x**2 + dist_y**2)
        self.x += dist_x / length * self.speed
        self.y += dist_y / length * self.speed
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        health_bar_length = self.tile_length*3/4
        health_bar_height = health_bar_length/8
        health_bar_x = self.x - health_bar_length/2
        health_bar_y = self.y - self.r - health_bar_height*3/2
        pygame.draw.rect(
            self.screen,
            "#ff0000",
            (health_bar_x, health_bar_y, health_bar_length, health_bar_height)
        )
        pygame.draw.rect(
            self.screen,
            "#00ff00",
            (
                health_bar_x,
                health_bar_y,
                health_bar_length * (self.health / self.max_health),
                health_bar_height,
            )
        )
        if "ranged" in self.special_tags:

            if pygame.time.get_ticks() - self.last_attack_time > self.cooldown:
                self.last_attack_time = pygame.time.get_ticks()
                enemy_bullets.append(
                    Projectile(
                        self.screen,
                        (self.x, self.y),
                        (player_x - self.x, player_y - self.y),
                        self.damage,
                    )
                )


class Weapon:
    def __init__(self, damage=3, cooldown=1000, reload_time=0, max_bullet=1) -> None:
        self.damage = damage
        self.cooldown = cooldown
        self.reload_time = reload_time
        self.bullet_count = max_bullet
        self.max_bullet = max_bullet
        self.last_attack_time = -self.cooldown
        self.reloading = False


def generate_enemies(screen, player_pos, room_num=1, difficulty=1) -> list[Enemy]:
    enemies = []
    level = room_num//10+1
    room_num %= 10
    for _ in range(int(room_num**1.1 + difficulty*(room_num/5)**(1.25))):
        enemy_stats = ENEMY_TYPES[random.choice(list(ENEMY_TYPES.keys()))]
        enemy = Enemy(screen, *enemy_stats)
        while math.dist((player_pos), (enemy.x, enemy.y)) < 300:
            enemy = Enemy(screen, *enemy_stats)
        enemy.health *= 2**(level-1)
        enemy.max_health *= 2**(level-1)
        enemies.append(enemy)
    return enemies


def change_room(screen, player, old_grid, new_grid, room_number, direction):
    old_room = pygame.Surface((screen.get_width(), screen.get_height()))
    new_room = pygame.Surface((screen.get_width(), screen.get_height()))
    draw_background(old_room, old_grid, room_number)
    draw_background(new_room, new_grid, room_number + 1)
    draw_bottom_wall(old_room, old_grid, True)
    draw_bottom_wall(new_room, new_grid, True)
    player.weapon.bullet_count = player.weapon.max_bullet
    speed = screen.get_width()//700
    for offset in range(
        0,
        max(
            screen.get_height() * abs(direction[1]),
            screen.get_width() * abs(direction[0]),
        ),
        speed,
    ):
        screen.blits(
            [
                (old_room, (direction[0] * offset, direction[1] * offset)),
                (
                    new_room,
                    (
                        direction[0] * (offset - screen.get_width()),
                        direction[1] * (offset - screen.get_height()),
                    ),
                ),
            ]
        )
        player.x += speed * direction[0]
        player.y += speed * direction[1]
        player.update()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    screen.blit(new_room)
    player.upgrade(random.randint(1, 5))
    
def draw_background(screen, grid, room_number, door_open=True):
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
                screen.blit(floor_img, (x * square_length, y * square_length, square_length, square_length))
                if x == 0:
                    screen.blit(left_wall_img, (x * square_length, y * square_length, square_length, square_length))
                elif x == 15:
                    screen.blit(right_wall_img, (x * square_length, y * square_length, square_length, square_length))

                if y == 0:
                    screen.blit(top_wall_img, (x * square_length, y * square_length, square_length, square_length))

                if x == 0 and y == 0:
                    screen.blit(left_top_corner_img, (x * square_length, y * square_length, square_length, square_length))
                elif x == 15 and y == 0:
                    screen.blit(right_top_corner_img, (x * square_length, y * square_length, square_length, square_length))

            elif value == 1:
                pygame.draw.rect(
                    screen,
                    (100, 100, 100), (x*square_length, y*square_length, square_length, square_length))
            elif value == 2:
                pygame.draw.rect(screen, (255, 0, 0),
                    (
                        x * square_length,
                        y * square_length,
                        square_length,
                        square_length,
                    ),
                )
    
    if door_open:
        screen.blit(floor_img, (7 * square_length, 0, square_length, square_length))
        screen.blit(floor_img, (8 * square_length, 0, square_length, square_length))
        screen.blit(floor_img, (0 * square_length, 4*square_length, square_length, square_length))
        screen.blit(floor_img, (0 * square_length, 5*square_length, square_length, square_length))
        screen.blit(floor_img, (15 * square_length, 4*square_length, square_length, square_length))
        screen.blit(floor_img, (15 * square_length, 5*square_length, square_length, square_length))

    text = room_number_font.render(str(room_number), True, (30, 30, 30))
    textpos = text.get_rect(
        centerx=screen.get_width() / 2, centery=screen.get_height() / 2
    )
    screen.blit(text, textpos)

    difficulty_font = pygame.font.SysFont("Comic Sans MS", 20)
    text = difficulty_font.render(str(difficulty[0]), True, (255, 255, 255))
    textpos = text.get_rect(centerx=screen.get_width() / 2, centery=square_length / 2)
    screen.blit(text, textpos)
    text = difficulty_font.render(str(difficulty[3]), True, (255, 255, 255))
    textpos = text.get_rect(
        centerx=screen.get_width() - square_length / 2, centery=screen.get_height() / 2
    )
    screen.blit(text, textpos)
    text = difficulty_font.render(str(difficulty[1]), True, (255, 255, 255))
    textpos = text.get_rect(
        centerx=screen.get_width() / 2, centery=screen.get_height() - square_length / 2
    )
    screen.blit(text, textpos)
    text = difficulty_font.render(str(difficulty[2]), True, (255, 255, 255))
    textpos = text.get_rect(centerx=square_length / 2, centery=screen.get_height() / 2)
    screen.blit(text, textpos)


def draw_bottom_wall(screen, grid, door_open):
    square_length = screen.get_width() / 16
    for i in range(len(grid[-1])):
        if i == 0:
            screen.blit(left_bottom_corner_img, (i * square_length, (9+11/30) * square_length, square_length, square_length))
        elif i == 15:
            screen.blit(right_bottom_corner_img, (i * square_length, (9+11/30) * square_length, square_length, square_length))
        else:
            if not door_open or not (i == 7 or i == 8):
                screen.blit(bottom_wall_img, (i * square_length, (9+11/30) * square_length, square_length, square_length))
    text = difficulty_font.render(str(difficulty[1]), True, (255, 255, 255))
    textpos = text.get_rect(
        centerx=screen.get_width() / 2, centery=screen.get_height() - square_length / 2
    )
    screen.blit(text, textpos)


def main():
    global floor_img, left_wall_img, right_wall_img, top_wall_img, bottom_wall_img, left_door_img, player_sprite
    global left_top_corner_img, right_top_corner_img, left_bottom_corner_img, right_bottom_corner_img, right_door_img, heart_img, dead_heart_img
    global enemy_bullets
    fps = 60
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    room_number = 0
    print(screen.get_width(), screen.get_height())
    player = Player(screen)
    grid = [[0 for _ in range(16)] for _ in range(10)]
    bullets = []
    enemies: list[Enemy] = []
    square_length = screen.get_width() / 16  + 1

    floor_img = pygame.transform.scale(floor_img, (square_length, square_length))
    left_wall_img = pygame.transform.scale(left_wall_img, (square_length, square_length))
    right_wall_img = pygame.transform.flip(left_wall_img, True, False)
    top_wall_img = pygame.transform.scale(top_wall_img, (square_length, square_length))
    bottom_wall_img = pygame.transform.scale(bottom_wall_img, (square_length, square_length*19/30))
    left_top_corner_img = pygame.transform.scale(left_top_corner_img, (square_length, square_length))
    right_top_corner_img = pygame.transform.flip(left_top_corner_img, True, False)
    left_bottom_corner_img = pygame.transform.scale(left_bottom_corner_img, (square_length, square_length*19/30))
    right_bottom_corner_img = pygame.transform.flip(left_bottom_corner_img, True, False)
    heart_img = pygame.transform.scale(heart_img, (square_length, square_length))
    dead_heart_img = pygame.transform.scale(dead_heart_img, (square_length, square_length))
    player_sprite = pygame.transform.scale(player_sprite, ((square_length*2)/3, (square_length*2)/3))


    while player.health > 0:
        draw_background(screen, grid, room_number, len(enemies) == 0)

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == Player_reload:
                player.weapon.bullet_count = player.weapon.max_bullet
                player.weapon.reloading = False
                pygame.time.set_timer(Player_reload, 0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    player.weapon.reloading = True
                    pygame.time.set_timer(Player_reload, int(player.weapon.reload_time))        
        if pygame.mouse.get_pressed()[0]:
            if (
                pygame.time.get_ticks() - player.weapon.last_attack_time
                > player.weapon.cooldown
            ):
                if player.weapon.bullet_count > 0 and not player.weapon.reloading:
                    pos = pygame.mouse.get_pos()
                    bullets.append(
                        Projectile(
                            screen,
                            (player.x, player.y),
                            (pos[0] - player.x, pos[1] - player.y),
                            player.weapon.damage,
                        )
                    )
                    player.weapon.last_attack_time = pygame.time.get_ticks()
                    player.weapon.bullet_count -= 1
                elif not player.weapon.reloading:
                    player.weapon.reloading = True
                    pygame.time.set_timer(Player_reload, int(player.weapon.reload_time))

        keys_held = pygame.key.get_pressed()
        player.update(keys_held, len(enemies) == 0)
        for r, row in enumerate(grid):
            for c, x in enumerate(row):
                if x != 2:
                    continue
                if pygame.Rect((player.x-player.r, player.y-player.r, 2*player.r, 2*player.r)).colliderect(pygame.Rect(c*square_length, r*square_length, square_length, square_length)):
                    player.health -= 1
                    grid[r][c] = 1
                    print(player.health)
        if len(enemies) == 0:
            if player.y + player.r < 0:
                direction = (0, 1)
                new_grid = [[0 for _ in range(16)] for _ in range(10)]
                trap_positions = random.sample([(y, x) for y in range(2, 8) for x in range(2, 14)], room_number//2)
                for y, x in trap_positions:
                    new_grid[y][x] = 2
                change_room(screen, player, grid, new_grid, room_number, direction)
                grid = new_grid
                room_number += 1
                enemies = generate_enemies(screen, (player.x, player.y), room_number, difficulty[0])
                random.shuffle(difficulty)
            elif player.y - player.r > screen.get_height():
                direction = (0, -1)
                new_grid = [[0 for _ in range(16)] for _ in range(10)]
                trap_positions = random.sample([(y, x) for y in range(2, 8) for x in range(2, 14)], room_number//2)
                for y, x in trap_positions:
                    new_grid[y][x] = 2
                change_room(screen, player, grid, new_grid, room_number, direction)
                grid = new_grid
                room_number += 1
                enemies = generate_enemies(screen, (player.x, player.y), room_number, difficulty[1])
                random.shuffle(difficulty)
            if player.x + player.r < 0:
                direction = (1, 0)
                new_grid = [[0 for _ in range(16)] for _ in range(10)]
                trap_positions = random.sample([(y, x) for y in range(2, 8) for x in range(2, 14)], room_number//2)
                for y, x in trap_positions:
                    new_grid[y][x] = 2
                change_room(screen, player, grid, new_grid, room_number, direction)
                grid = new_grid
                room_number += 1
                enemies = generate_enemies(screen, (player.x, player.y), room_number, difficulty[2])
                random.shuffle(difficulty)
            elif player.x - player.r > screen.get_width():
                direction = (-1, 0)
                new_grid = [[0 for _ in range(16)] for _ in range(10)]
                trap_positions = random.sample([(y, x) for y in range(2, 8) for x in range(2, 14)], room_number//2)
                for y, x in trap_positions:
                    new_grid[y][x] = 2
                change_room(screen, player, grid, new_grid, room_number, direction)
                grid = new_grid
                room_number += 1
                enemies = generate_enemies(screen, (player.x, player.y), room_number, difficulty[3])
                random.shuffle(difficulty)

        for enemy in enemies:
            enemy.update(player.x, player.y)
            if math.dist((player.x, player.y), (enemy.x, enemy.y)) < player.r + enemy.r:
                if pygame.time.get_ticks() - enemy.last_attack_time > enemy.cooldown:
                    player.health -= enemy.damage
                    enemy.last_attack_time = pygame.time.get_ticks()
                overlap = (
                    -math.dist((player.x, player.y), (enemy.x, enemy.y))
                    + player.r
                    + enemy.r
                )
                to_player_vector = pygame.Vector2(
                    player.x - enemy.x, player.y - enemy.y
                ).normalize()
                enemy.x -= to_player_vector.x * overlap / 2
                enemy.y -= to_player_vector.y * overlap / 2
                player.x += to_player_vector.x * overlap / 2
                player.y += to_player_vector.y * overlap / 2
            for other in enemies:
                if enemy is other:
                    continue
                if (
                    math.dist((other.x, other.y), (enemy.x, enemy.y))
                    < other.r + enemy.r
                ):
                    overlap = (
                        -math.dist((other.x, other.y), (enemy.x, enemy.y))
                        + other.r
                        + enemy.r
                    )
                    to_other_vector = pygame.Vector2(
                        other.x - enemy.x, other.y - enemy.y
                    ).normalize()
                    enemy.x -= to_other_vector.x * overlap / 2
                    enemy.y -= to_other_vector.y * overlap / 2
                    other.x += to_other_vector.x * overlap / 2
                    other.y += to_other_vector.y * overlap / 2

        for bullet in bullets.copy():
            bullet.update()
            for enemy in enemies.copy():
                if math.dist((bullet.pos), (enemy.x, enemy.y)) < bullet.r + enemy.r:
                    enemies[enemies.index(enemy)].health -= bullet.damage
                    if enemies[enemies.index(enemy)].health <= 0:
                        enemies.remove(enemy)
                        if random.randint(1, 5) == 1:
                            player.upgrade(random.randint(1, 5))
                    bullets.remove(bullet)
                    break
        bullets = [bullet for bullet in bullets if not bullet.in_border()]

        for bullet in enemy_bullets.copy():
            bullet.update((255, 0, 0))
            if math.dist((bullet.pos), (player.x, player.y)) < bullet.r + player.r:
                player.health -= bullet.damage
                enemy_bullets.remove(bullet)
        enemy_bullets = [bullet for bullet in enemy_bullets if not bullet.in_border()]

        draw_bottom_wall(screen, grid, len(enemies) == 0)
        pygame.display.flip()
        fps_clock.tick(fps)

        if player.weapon.bullet_count == 0 and not player.weapon.reloading:
            player.weapon.reloading = True
            pygame.time.set_timer(Player_reload, int(player.weapon.reload_time))  


if __name__ == "__main__":
    main()
