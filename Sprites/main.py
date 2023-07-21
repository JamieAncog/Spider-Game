import pygame

pygame.init()

init_x = 40
in_play = True
win_width = 852
win_height = 480
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Timing Game")
bg = pygame.image.load("sky3.jpg")
obstacle = pygame.image.load("smasher.png")
walkRight = [pygame.image.load("run_right1.png"), pygame.image.load("run_right0.png"),
             pygame.image.load("run_right2.png")]


class Player:
    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.right = False
        self.walkCount = 0
        self.image = walkRight[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.right:
            self.image = walkRight[self.walkCount % 3]
            self.walkCount += 1
        else:
            self.image = walkRight[1]

        window.blit(self.image, (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Obstacle:

    def __init__(self, x, y, width, height, max_y, min_y, vel):
        self.x = x
        self.y = y
        self.max_y = max_y
        self.min_y = min_y
        self.vel = vel
        self.width = width
        self.height = height
        self.image = obstacle
        self.rise = True
        self.fall = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Entrance:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = obstacle
        self.rise = True
        self.fall = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


bunny = Player(init_x, 305, 47, 116, 20)
smasher = Obstacle(500, -10, 148, 431, -10, -220, 15)


def redraw_game_window():
    win.blit(bg, (0, 0))
    bunny.draw(win)
    smasher.draw(win)
    pygame.display.update()


run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        if bunny.x < win_width - bunny.width - bunny.vel:
            bunny.x += bunny.vel
            bunny.right = True
        else:
            bunny.x = 0
    else:
        bunny.right = False
        bunny.walkCount = 0

    if smasher.y >= smasher.max_y:
        smasher.fall = False
        smasher.rise = True
    elif smasher.y <= smasher.min_y:
        smasher.rise = False
        smasher.fall = True

    if smasher.rise:
        smasher.y -= smasher.vel
    else:
        smasher.y += smasher.vel

    if bunny.rect.colliderect(smasher.rect):
        in_play = False

    if in_play:
        redraw_game_window()

pygame.quit()
