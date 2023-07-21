import pygame

pygame.init()

in_play = True
win_width = 600
win_height = 480
border = 50
margin = 100
ground_height = 90
num_smashers = 3
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Timing Game")
bg = pygame.image.load("sky3.jpg")
obstacle = pygame.image.load("smasher.png")
ground = pygame.Rect(0, win_height - ground_height, win_width, ground_height)
game_over_screen = pygame.image.load("game_over_screen.png")
walkRight = [pygame.image.load("run_right1.png"), pygame.image.load("run_right0.png"),
             pygame.image.load("run_right2.png")]
love_font = pygame.font.Font('Love.ttf', 32)
smashers = []


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
        self.y = y - height
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

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        window.blit(self.image, (self.x, self.y))


class Obstacle:

    def __init__(self, x, width, height, max_y, min_y, vel, acc):
        self.x = x
        self.width = width
        self.height = height
        self.y = min_y
        self.max_y = max_y
        self.min_y = min_y
        self.vel = vel
        self.acc = acc
        self.image = obstacle
        self.rise = True
        self.fall = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_char(self, w_width, char):

        if self.x > -w_width:
            self.x -= char.vel
            char.right = True
        else:
            self.x = win_width
            self.vel += self.acc

    def crush(self, surface_rect):
        if self.rect.colliderect(surface_rect):
            self.fall = False
            self.rise = True
        elif self.y <= self.min_y:
            self.rise = False
            self.fall = True

        if self.rise:
            rise_inc = self.vel
            if self.y - self.vel < self.min_y:
                rise_inc = self.y - self.min_y
            self.y -= rise_inc
        else:
            fall_inc = self.vel
            if self.y + self.vel > self.max_y:
                fall_inc = self.max_y - self.y
            self.y += fall_inc

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


bunny = Player(win_width/4 - 47/2, win_height - ground_height, 47, 116, 40)
title = GameText(love_font, (0, 0, 0), 'Bunny Game', border)

for n in range(num_smashers):
    new_smasher = Obstacle(-win_width + (win_width * 2 / num_smashers) * n, 148, 431, -25, -240, 15, 10)
    smashers.append(new_smasher)

count = num_smashers - 1
curr_obstacle = smashers[count]


def redraw_game_window():
    win.blit(bg, (0, 0))
    bunny.draw(win)
    for obj in smashers:
        obj.draw(win)
    title.draw(win)
    pygame.draw.rect(win, (0, 0, 0), ground)
    pygame.display.update()


run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    game_over = False

    for smasher in smashers:
        if bunny.rect.colliderect(smasher.rect):
            game_over = True

    if game_over:
        in_play = False
        win.blit(bg, (0, 0))
        pygame.draw.rect(win, (0, 0, 0), ground)
        win.blit(bunny.image, (bunny.x, bunny.y))
        for smasher in smashers:
            win.blit(smasher.image, (smasher.x, smasher.y))
        win.blit(game_over_screen, (0, 0))
        title.color = (255, 255, 255)
        title.draw(win)
        pygame.display.update()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and in_play:

        for smasher in smashers:
            smasher.move_char(win_width, bunny)

        if curr_obstacle.x == bunny.vel:
            title.score += 1
            count += 1
            curr_obstacle = smashers[count % num_smashers]

    else:
        bunny.right = False
        bunny.walkCount = 0

    if in_play:

        for smasher in smashers:
            smasher.crush(ground)

    if in_play:
        redraw_game_window()

pygame.quit()
