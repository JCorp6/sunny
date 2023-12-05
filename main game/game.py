import pygame
import sys

pygame.init()
clock = pygame.time.Clock()

WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.transform.scale(
    pygame.image.load("./main game/assets/back.png"), (WIDTH, HEIGHT)
)
grass = pygame.image.load("./main game/assets/platform.png")
dirt = pygame.image.load("./main game/assets/dirt0000.png")

tree = pygame.transform.scale(
    pygame.image.load("./main game/assets/tree.png"), (119 * 2, 111 * 2)
)
pine = pygame.transform.scale(
    pygame.image.load("./main game/assets/pine.png"), (82 * 1.5, 130 * 1.5)
)
bush = pygame.transform.scale(
    pygame.image.load("./main game/assets/bush.png"), (46 * 2, 28 * 2)
)
sign = pygame.transform.scale(
    pygame.image.load("./main game/assets/sign.png"), (18 * 2, 20 * 2)
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.move_right = False
        self.move_left = False
        self.jump = False
        self.speed = 10
        self.gravity = 0.5
        self.y_velo = 0
        self.move = False

        self.right = [
            pygame.transform.scale(
                pygame.image.load(
                    f"./main game/assets/player/idle/player-idle-{index}.png"
                ),
                (50, 50),
            )
            for index in range(1, 5)
        ]
        self.left = [pygame.transform.flip(image, True, False) for image in self.right]

        self.walk_right = [
            pygame.transform.scale(
                pygame.image.load(
                    f"./main game/assets/player/run/player-run-{index}.png"
                ),
                (50, 50),
            )
            for index in range(1, 6)
        ]
        self.walk_left = [
            pygame.transform.flip(image, True, False) for image in self.walk_right
        ]

        self.frame = 0
        self.idle = self.right[self.frame]
        self.walk_idle = self.walk_right[self.frame]
        self.rect = self.idle.get_rect(
            topleft=(platform.tile_size * 2, HEIGHT - 2 * platform.tile_size - 64)
        )
        self.width = self.idle.get_width()
        self.height = self.idle.get_width()
        self.direction = 1

    def update(self):
        self.dx = 0
        self.dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and not self.jump:
            self.y_velo = -15
            self.jump = True
            self.move = True
        if not keys[pygame.K_w]:
            self.jump = False
            self.move = True
        if keys[pygame.K_d] and self.rect.right <= WIDTH:
            self.dx += 5
            self.direction = 1
            self.move = True
        if keys[pygame.K_a] and self.rect.left >= 0:
            self.dx -= 5
            self.direction = -1
            self.move = True
        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            self.move = False
            if self.direction == 1:
                self.walk_idle = self.walk_right[int(self.frame)]
            if self.direction == -1:
                self.walk_idle = self.walk_left[int(self.frame)]

        if self.move is False:
            self.frame += 0.2
            if self.frame >= len(self.right):
                self.frame = 0
            if self.direction == 1:
                self.idle = self.right[int(self.frame)]
            if self.direction == -1:
                self.idle = self.left[int(self.frame)]

        if self.move is True:
            self.frame += 0.2
            if self.frame >= len(self.walk_right):
                self.frame = 0
            if self.direction == 1:
                self.idle = self.walk_right[int(self.frame)]
            if self.direction == -1:
                self.idle = self.walk_left[int(self.frame)]

        self.y_velo += 1
        if self.y_velo > 10:
            self.y_velo = 10
        self.dy += self.y_velo

        for tile in platform.tile_list:
            if tile[1].colliderect(
                self.rect.x + self.dx, self.rect.y, self.width, self.height
            ):
                self.dx = 0

            if tile[1].colliderect(
                self.rect.x, self.rect.y + self.dy, self.width, self.height
            ):
                if self.y_velo < 0:
                    self.dy = tile[1].bottom - self.rect.top
                    self.y_velo = 0
                elif self.y_velo >= 0:
                    self.dy = tile[1].top - self.rect.bottom
                    self.y_velo = 0

        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.dy = 0


class Enemy:
    def __init__(self):
        self.right = []
        self.left = []
        for index in range(1, 6):
            self.img = pygame.image.load(
                f"./main game/assets/enemy/opossum-{index}.png"
            )
            enemy_right = pygame.transform.scale(self.img, (50, 50))
            enemy_left = pygame.transform.flip(self.img, True, False)
            self.right.append(enemy_right)
            self.left.append(enemy_left)
        self.frame = 0
        self.image = self.right[self.frame]
        self.enemy_rect = self.image.get_rect(topleft=(650, 350))

    def update(self):
        self.frame += 0.1
        if self.frame >= len(self.right):
            self.frame = 0
        self.image = self.right[int(self.frame)]



class Platform:
    def __init__(self):
        self.tile_list = []
        self.tile_size = 50
        self.map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2],
            [2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
            [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 2, 2, 2, 2, 2],
            [2, 2, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
            [2, 2, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        ]

        self.draw_platforms()

    def draw_platforms(self):
        for row_index, row in enumerate(self.map):
            for col_index, tile in enumerate(row):
                if tile == 1:
                    img = pygame.transform.scale(
                        grass, (self.tile_size, self.tile_size)
                    )
                    img_rect = img.get_rect(
                        topleft=(col_index * self.tile_size, row_index * self.tile_size)
                    )
                    self.tile_list.append((img, img_rect))
                if tile == 2:
                    img = pygame.transform.scale(dirt, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect(
                        topleft=(col_index * self.tile_size, row_index * self.tile_size)
                    )
                    self.tile_list.append((img, img_rect))

    def draw(self):
        screen.blit(tree, (700, 78))
        screen.blit(bush, (600, 344))
        screen.blit(pine, (120, 305))
        screen.blit(sign, (525, 360))

        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


platform = Platform()
player = Player()
enemy = Enemy()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((234, 56, 70))
    screen.blit(bg, (0, 0))
    player.update()
    platform.draw()
    enemy.update()
    screen.blit(player.idle, player.rect)
    screen.blit(enemy.image, enemy.enemy_rect)

    pygame.display.flip()
    clock.tick(60)
