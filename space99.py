import pygame
import random

# ----- fps
clock = pygame.time.Clock()

# ----- screen
screen_w = 400
screen_h = 600
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("space 99")
icon = pygame.image.load("data/imgs/icon.png")
pygame.display.set_icon(icon)

# ----- properties
alien_cooldown = 300
last_alien_shot = pygame.time.get_ticks()


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/imgs/spaceship.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()

    def update(self):

        # ----- movement
        speed = 6

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 10:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_w - 10:
            self.rect.x += speed
        if key[pygame.K_UP] and self.rect.y > screen_h - 100:
            self.rect.y -= speed / 5
        if key[pygame.K_DOWN] and self.rect.y < screen_h - 60:
            self.rect.y += speed

        # ----- bullets & cooldown
        cooldown = 500
        time_now = pygame.time.get_ticks()

        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            bullet = Spaceship_Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

        self.mask = pygame.mask.from_surface(self.image)

        # ----- health
        pygame.draw.rect(screen, (99, 99, 99), (self.rect.x, (self.rect.y + 40),
                         int(self.rect.width * (self.health_remaining / self.health_start)), 8))


class Spaceship_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/imgs/bullet.png")
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()


class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            f"data/imgs/aliens/alien-{random.randint(1, 3)}.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1

        if abs(self.move_counter) > 54:
            self.move_direction *= -1
            self.move_counter *= self.move_direction


class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/imgs/enemy_bullet.png")
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 3
        if self.rect.bottom > screen_h:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            spaceship.health_remaining -= 1


spaceship = Spaceship(int(screen_w / 2), screen_h - 100, 3)

# ----- groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()

spaceship_group.add(spaceship)


def create_aliens():
    for row in range(6):
        for entity in range(5):
            alien = Aliens(80 + 48 * row, 24 + 40 * entity)
            alien_group.add(alien)


create_aliens()


while True:

    time_now = pygame.time.get_ticks()

    if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
        attacking_alien = random.choice(alien_group.sprites())
        alien_bullet = Alien_Bullets(
            attacking_alien.rect.centerx, attacking_alien.rect.bottom)
        alien_bullet_group.add(alien_bullet)
        last_alien_shot = time_now

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill((255, 255, 255))

    # ----- update
    spaceship.update()

    bullet_group.update()
    alien_group.update()
    alien_bullet_group.update()

    # ----- draw
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)

    pygame.display.update()
    clock.tick(60)
