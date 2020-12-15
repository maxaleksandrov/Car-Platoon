import pygame

pygame.init()
(width, height) = (1500, 1000)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()
running = True
FPS = pygame.time.Clock()
period = 1 / 60
mu = 0.2
g = 9.8


class LEADCAR(pygame.sprite.Sprite):
    def __init__(self, v, f, x, y, m):
        pygame.sprite.Sprite.__init__(self)
        self.v = v
        self.f = f
        self.m = m
        self.a = (self.f - self.m * mu * g) / self.m
        self.image = pygame.Surface((25, 25))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.v += self.a
            self.rect.x -= self.v
        elif keys[pygame.K_DOWN]:
            self.v -= self.a
            self.rect.x -= self.v
        else:
            self.rect.x -= self.v

    def distance(self):
        x, y = self.rect.midright
        return x


leadcar = LEADCAR(0.5, 2010, 1250, 600, 1000)


class FOLLOWERCAR(pygame.sprite.Sprite):
    def __init__(self, v, x, y, D):
        pygame.sprite.Sprite.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.v = v
        self.vel = v
        self.D = D
        self.image = pygame.Surface((25, 25))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.wrong_distance = False
        self.time = 0

    def distance_check(self):
        x = leadcar.distance()
        return x

    def update(self):
        x, y = self.rect.midleft
        d = abs(x - self.distance_check() + 25)
        if d == self.D:
            self.rect.x -= self.v
        elif d > self.D:
            self.v = self.v + (d - self.D)
            self.rect.x -= self.v
        elif d < self.D:
            self.v = self.v + (d - self.D)
            self.rect.x -= self.v


follower = FOLLOWERCAR(0.5, 1450, 600, 200)
Sprites = pygame.sprite.Group()
Sprites.add(leadcar)
Sprites.add(follower)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    FPS.tick(60)
    Sprites.update()
    pygame.Surface.fill(screen, (0, 0, 0))
    Sprites.draw(screen)
    pygame.display.update()
