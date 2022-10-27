# Flying Squirrel presents two face
import pygame
import sys
from math import floor, ceil
from pygame.locals import *
from layouts import level_1_layout

pygame.mixer.pre_init()
pygame.init()
flags = FULLSCREEN | DOUBLEBUF | SCALED  # fullscreen, double buffering, scaled resolution
clock = pygame.time.Clock()
FPS = 120  # limit frame rate to 120 fps
pygame.mouse.set_visible(False)  # invisible mouse cursor
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

tile = 80  # tile size in pixels (higher # = higher quality, slower)
width, height = (1280, 800)
center_w = width / 2
center_h = height / 2
window = pygame.display.set_mode((width, height), flags)

two_face_img = pygame.image.load("imgs/twoface.png")
two_face_img = pygame.tranform.scale(two_face_img, (tile, tile))
menu_bg = pygame.image.load("imgs/twofacemenuBG.png").convert()
menu_bg = pygame.transform.scale(menu_bg, (width, height))
menu_bg_width = menu_bg.get_width()
menu_tiles = ceil(width / menu_bg_width) + 1  # creates tiles for menu screen scroll

#level_1_bg = pygame.image.load...

title_font = pygame.font.Font("fonts/VCR_OSD_MONO.ttf", 125)
pygame.display.set_caption('two-face.')  # caption of window

pygame.mixer.music.load('audio/dark_tundra.wav')
pygame.mixer.music.play(-1)  # play song on infinite loop


def moveCheck(level, row, col):  # checks if space can be moved to
    if col == -1 or col == len(level[0]) or row == -1 or row == len(level):  # allows movement past level bounds
        return 1
    if level[int(row)][int(col)] != 0:  # if move spot is not a boundary
        return 1
    return False


class Game:
    def __init__(self):
        self.two_face = [1, 1]
        self.moves, self.move_delay = 0, 2
        self.speed = 1 / 32
        self.dir = self.new_dir = 0
        self.two_face_angle = 0
        self.two_face_rect = Rect(tile, tile, tile, tile)
        self.stopped = False
        self.state = "main_menu"
        self.game_scroll = [0, 0]
        self.wiggle = [0, 0]
        self.menu_scroll = 0
        # self.level_bg = level_1_bg
        self.i = 0
        self.keyScore = 0

    def twoFaceMovement(self, board):
        if self.moves == self.move_delay:
            self.moves = 0
            if self.new_dir == 0:
                if moveCheck(board, floor(self.two_face[0] - self.speed), self.two_face[1]) \
                        and self.two_face[1] % 1.0 == 0:
                    self.two_face[0] -= self.speed
                    self.dir = self.new_dir
                    self.two_face_angle = 0
                    return
            elif self.new_dir == 1:
                if moveCheck(board, self.two_face[0], ceil(self.two_face[1] + self.speed)) \
                        and self.two_face[0] % 1.0 == 0:
                    self.two_face[1] += self.speed
                    self.dir = self.new_dir
                    self.two_face_angle = 270
                    return
            elif self.new_dir == 2:
                if moveCheck(board, ceil(self.two_face[0] + self.speed), self.two_face[1]) \
                        and self.two_face[1] % 1.0 == 0:
                    self.two_face[0] += self.speed
                    self.dir = self.new_dir
                    self.two_face_angle = 180
                    return
            elif self.new_dir == 3:
                if moveCheck(board, self.two_face[0], floor(self.two_face[1] - self.speed)) \
                        and self.two_face[0] % 1.0 == 0:
                    self.two_face[1] -= self.speed
                    self.dir = self.new_dir
                    self.two_face_angle = 90
                    return

            if self.dir == 0:  # dir handler
                if moveCheck(board, floor(self.two_face[0] - self.speed), self.two_face[1]) \
                        and self.two_face[1] % 1.0 == 0:
                    self.two_face[0] -= self.speed
            elif self.dir == 1:
                if moveCheck(board, self.two_face[0], ceil(self.two_face[1] + self.speed)) \
                        and self.two_face[0] % 1.0 == 0:
                    self.two_face[1] += self.speed
            elif self.dir == 2:
                if moveCheck(board, ceil(self.two_face[0] + self.speed), self.two_face[1]) \
                        and self.two_face[1] % 1.0 == 0:
                    self.two_face[0] += self.speed
            elif self.dir == 3:
                if moveCheck(board, self.two_face[0], floor(self.two_face[1] - self.speed)) \
                        and self.two_face[0] % 1.0 == 0:
                    self.two_face[1] -= self.speed

    def keyGetter(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # key mapping
                if event.key == pygame.K_w:
                    self.new_dir = 0  # north
                    self.stopped = False
                if event.key == pygame.K_d:
                    self.new_dir = 1  # east
                    self.stopped = False
                if event.key == pygame.K_s:
                    self.new_dir = 2  # south
                    self.stopped = False
                if event.key == pygame.K_a:
                    self.new_dir = 3  # west
                    self.stopped = False
                if event.key == pygame.K_SPACE:
                    self.stopped = not self.stopped  # pauses and unpauses movement on spacebar
                if event.key == pygame.K_q:
                    pygame.quit()  # quit on keystroke q
                    sys.exit()

    def boardCreate(self):
        # wiggle room: the size of the background level image - the size of the screen
        self.wiggle[0] = self.level_bg.get_size()[0] - width
        self.wiggle[1] = self.level_bg.get_size()[1] - height

        # game screen scroll: screen move effect centered around player but stops at screen edges
        self.game_scroll[0] += (self.two_face_rect.x - self.game_scroll[0] - center_w) / 40
        self.game_scroll[1] += (self.two_face_rect.y - self.game_scroll[1] - center_h) / 40

        # game will always stop scrolling at the borders of the game map
        if self.game_scroll[0] < 0:
            self.game_scroll[0] = 0
        if self.game_scroll[1] < 0:
            self.game_scroll[1] = 0
        if self.game_scroll[0] > self.wiggle[0]:
            self.game_scroll[0] = self.wiggle[0]
        if self.game_scroll[1] > self.wiggle[1]:
            self.game_scroll[1] = self.wiggle[1]

        window.blit(self.levelBG, (0 - self.game_scroll[0], 0 - self.game_scroll[1]))  # blit BG image for current level
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                # if self.board[i][j] == 0:  # 0 = background
                if self.board[i][j] == 1:  # 1 = bug
                    bugRect = bugImage.get_rect(center=(j * tile + tile // 2, i * tile + tile // 2))
                    window.blit(bugImage, (bugRect.x - self.game_scroll[0], bugRect.y - self.game_scroll[1]))
                # if self.board[i][j] == 2:  # 2 = empty, movable spot
                if self.board[i][j] == 3:  # 3 = rainbow bug
                    bugRect = bugImage4.get_rect(center=(j * tile + tile // 2, i * tile + tile // 2))
                    self.shakingImage(bugImage4, bugRect.x - self.game_scroll[0], bugRect.y - self.game_scroll[1])

        two_face_rotate = pygame.transform.rotate(two_face_img, self.two_face_angle)
        self.two_face_rect = two_face_img.get_rect(center=(floor(self.two_face[1] * tile + tile // 2),
                                                           floor(self.two_face[0] * tile + tile // 2)))
        window.blit(two_face_rotate, (self.two_face_rect.x - self.game_scroll[0],
                                   self.two_face_rect.y - self.game_scroll[1]))
        pygame.display.update()

    def mainMenu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.i = 0
                    self.state = "pre_level_1"
                if event.key == pygame.K_q:
                    pygame.quit()  # quit on keystroke q
                    sys.exit()

        # display screen
        # self.colorChanging(white)
        for i in range(0, menu_tiles):
            window.blit(menu_bg, (i * menu_bg_width + self.menu_scroll, 0))

        # scroll background
        self.menu_scroll -= .3

        # reset scroll
        if abs(self.menu_scroll) > menu_bg_width:
            self.menu_scroll = 0
        menu_title_shadow = title_font.render("two face.", False, (0, 0, 0))
        window.blit(menu_title_shadow, (0, 340))
        menu_title = title_font.render("two face.", False, (207, 198, 184))
        window.blit(menu_title, (8, 348))
        pygame.display.update()

    def prelevel1(self):
        window.fill((0, 0, 0))
        prelevel1_title = title_font.render("begin.", False, (207, 198, 184))
        if 200 < self.i < 500:
            window.blit(prelevel1_title, (center_w - 125, center_h - 125))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.i = 0  # resets global iterator to 0 for use elsewhere
                    self.state = "level_1"
                if event.key == pygame.K_q:
                    pygame.quit()  # quit on keystroke q
                    sys.exit()
        if self.i > 700:  # 7 seconds max on transition screen; can be skipped with p
            self.i = 0  # resets global iterator to 0 for use elsewhere
            self.state = "level_1"
        self.i += 1

    def level1(self):
        self.keyGetter()
        self.twoFaceMovement(level_1_layout)
        self.boardCreate()
        if self.keyScore == 1:
            self.i = 0
            self.state = "pre-level_2"
        if not self.stopped:  # while spacebar is not pressed down, continue to move
            self.moves += 1

    def stateManager(self):
        if self.state == "main_menu":
            self.mainMenu()
        if self.state == "pre_level_1":
            self.prelevel1()
        if self.state == "level_1":
            self.level1()


game = Game()
if __name__ == "__main__":
    while 1:  # game loop
        # clock.tick(FPS)
        game.stateManager()
