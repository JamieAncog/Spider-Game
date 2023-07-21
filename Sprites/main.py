import pygame

pygame.init()

in_play = True
win_width = 852
win_height = 480
border = 50
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Timing Game")
bg = pygame.image.load("sky3.jpg")
obstacle = pygame.image.load("smasher.png")
game_over_screen = pygame.image.load("game_over_screen.png")
portal = pygame.image.load("portal.png")
walkRight = [pygame.image.load("run_right1.png"), pygame.image.load("run_right0.png"),
             pygame.image.load("run_right2.png")]
love_font = pygame.font.Font('Love.ttf', 32)


class GameText:
    def __init__(self, font, color, header, text_border):
        self.font = font
        self.color = color
        self.header = header
        self.text_border = text_border
        self.score = 0

    def draw(self, window):
        text = self.font.render(self.header, True, self.color)
        text_rect = text.get_rect()
        text_rect.center = (text_rect.width / 2 + self.text_border, self.text_border)
        score_text = self.font.render('Score: ' + str(self.score), True, self.color)
        score_text_rect = text.get_rect()
        score_text_rect.center = (text_rect.width / 2 + self.text_border, self.text_border + text_rect.height)
        window.blit(text, text_rect)
        window.blit(score_text, score_text_rect)


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


class Portal:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = portal

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))


left_portal = Portal(win_width-border-59, 300, 59, 117)
right_portal = Portal(border, 300, 59, 117)
bunny = Player(border + left_portal.width/2, 305, 47, 116, 20)
smasher = Obstacle(450, -240, 148, 431, -10, -240, 15)
title = GameText(love_font, (0, 0, 0), 'Bunny Game', border)


def redraw_game_window():
    win.blit(bg, (0, 0))
    bunny.draw(win)
    smasher.draw(win)
    left_portal.draw(win)
    right_portal.draw(win)
    title.draw(win)
    pygame.display.update()


run = True
while run:
    pygame.time.delay(100)

    if bunny.rect.colliderect(smasher.rect):
        in_play = False
        win.blit(bg, (0, 0))
        win.blit(bunny.image, (bunny.x, bunny.y))
        win.blit(left_portal.image, (left_portal.x, left_portal.y))
        win.blit(right_portal.image, (right_portal.x, right_portal.y))
        win.blit(smasher.image, (smasher.x, smasher.y))
        win.blit(game_over_screen, (0, 0))
        title.color = (255, 255, 255)
        title.draw(win)
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and in_play:
        if bunny.x < win_width - 50 - right_portal.width/2 - bunny.width - bunny.vel:
            bunny.x += bunny.vel
            bunny.right = True
        else:
            bunny.x = border + left_portal.width/2
            title.score += 1
            smasher.vel += 5
    else:
        bunny.right = False
        bunny.walkCount = 0

    if smasher.y >= smasher.max_y:
        smasher.fall = False
        smasher.rise = True
    elif smasher.y <= smasher.min_y:
        smasher.rise = False
        smasher.fall = True

    if in_play:
        if smasher.rise:
            smasher.y -= smasher.vel
        else:
            smasher.y += smasher.vel

    if in_play:
        redraw_game_window()

pygame.quit()
