import pygame

pygame.init()

init_x = 40
win = pygame.display.set_mode((852, 480))
pygame.display.set_caption("Timing Game")
bg = pygame.image.load("sky3.jpg")
walkRight = [pygame.image.load("run_right1.png"), pygame.image.load("run_right0.png"),
             pygame.image.load("run_right2.png")]


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.right = False
        self.walkCount = 0

    def draw(self, window):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.right:
            window.blit(walkRight[self.walkCount % 3], (self.x, self.y))
            self.walkCount += 1
        else:
            window.blit(walkRight[1], (self.x, self.y))


bunny = Player(init_x, 305, 42, 105)


def redraw_game_window():
    win.blit(bg, (0, 0))
    bunny.draw(win)
    pygame.display.update()


run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        if bunny.x < 852 - bunny.width - bunny.vel:
            bunny.x += bunny.vel
            bunny.right = True
        else:
            bunny.x = 0
    else:
        bunny.right = False
        bunny.walkCount = 0

    redraw_game_window()

pygame.quit()
