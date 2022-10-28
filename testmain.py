# Flying Squirrel presents two face
import pygame
import sys
from math import floor, ceil
from pygame.locals import *
from layouts import main_level_layout

pygame.mixer.pre_init()
pygame.init()
flags = FULLSCREEN | DOUBLEBUF | SCALED  # fullscreen, double buffering, scaled resolution
pygame.display.set_caption('two-face.')  # caption of window
clock = pygame.time.Clock()
FPS = 120  # limit frame rate to 120 fps
pygame.mouse.set_visible(False)  # invisible mouse cursor
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

tile = 80  # tile size in pixels (higher # = higher quality, slower)
width, height = (1280, 800)
center_w = width / 2
center_h = height / 2
window = pygame.display.set_mode((width, height), flags)

two_face_dark_img = pygame.image.load("imgs/twoface_dark.png").convert_alpha()
two_face_dark_img = pygame.transform.scale(two_face_dark_img, ((tile + tile) // 3, (tile + tile) // 3))
two_face_light_img = pygame.image.load("imgs/twoface_light.png").convert_alpha()
two_face_light_img = pygame.transform.scale(two_face_light_img, ((tile + tile) // 3, (tile + tile) // 3))
shard_img = pygame.image.load("imgs/shard.png").convert_alpha()
shard_img = pygame.transform.scale(shard_img, (tile // 2, tile // 2))
light_img = pygame.image.load("imgs/lightsource.png").convert_alpha()
light_img = pygame.transform.scale(light_img, (1500, 1500))
main_level_img = pygame.image.load("imgs/mainlevel.png").convert()
main_level_img = pygame.transform.scale(main_level_img, (tile * 25, tile * 13))
menu_bg = pygame.image.load("imgs/twofacemenuBG.png").convert()
menu_bg = pygame.transform.scale(menu_bg, (width, height))
menu_bg_width = menu_bg.get_width()
menu_tiles = ceil(width / menu_bg_width) + 1  # creates tiles for menu screen scroll

title_font = pygame.font.Font("fonts/VCR_OSD_MONO.ttf", 125)
sub_font = pygame.font.Font("fonts/VCR_OSD_MONO.ttf", 85)

glass_break = pygame.mixer.Sound("audio/glass_break.wav")
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
        self.two_face = [4, 2]
        self.moves, self.move_delay = 0, 2
        self.speed = 1 / 32
        self.dir = self.new_dir = 0
        self.two_face_img = two_face_dark_img
        self.two_face_rect = Rect(tile, tile, tile, tile)
        self.stopped = False
        self.state = "main_menu"
        self.level_bg = main_level_img
        self.layout = main_level_layout
        self.game_scroll = [0, 0]
        self.wiggle = [0, 0]
        self.menu_scroll = 0
        self.i = 0
        self.shard_score = 0
        self.house_score = 0
        self.cave_score = 0

    def twoFaceMovement(self, layout):
        if self.moves == self.move_delay:
            self.moves = 0
            if self.new_dir == 0:
                if moveCheck(layout, floor(self.two_face[0] - self.speed), self.two_face[1]) \
                        and self.two_face[1] % 1.0 == 0:
                    self.two_face[0] -= self.speed
                    self.dir = self.new_dir
                    return
            elif self.new_dir == 1:
                if moveCheck(layout, self.two_face[0], ceil(self.two_face[1] + self.speed)) \
                        and self.two_face[0] % 1.0 == 0:
                    self.two_face[1] += self.speed
                    self.dir = self.new_dir
                    self.two_face_img = two_face_dark_img
                    return
            elif self.new_dir == 2:
                if moveCheck(layout, ceil(self.two_face[0] + self.speed), self.two_face[1]) \
                        and self.two_face[1] % 1.0 == 0:
                    self.two_face[0] += self.speed
                    self.dir = self.new_dir
                    return
            elif self.new_dir == 3:
                if moveCheck(layout, self.two_face[0], floor(self.two_face[1] - self.speed)) \
                        and self.two_face[0] % 1.0 == 0:
                    self.two_face[1] -= self.speed
                    self.dir = self.new_dir
                    self.two_face_img = two_face_light_img
                    return

            if self.dir == 0:  # dir handler
                if moveCheck(layout, floor(self.two_face[0] - self.speed), self.two_face[1]) \
                        and self.two_face[1] % 1.0 == 0:
                    self.two_face[0] -= self.speed
            elif self.dir == 1:
                if moveCheck(layout, self.two_face[0], ceil(self.two_face[1] + self.speed)) \
                        and self.two_face[0] % 1.0 == 0:
                    self.two_face[1] += self.speed
            elif self.dir == 2:
                if moveCheck(layout, ceil(self.two_face[0] + self.speed), self.two_face[1]) \
                        and self.two_face[1] % 1.0 == 0:
                    self.two_face[0] += self.speed
            elif self.dir == 3:
                if moveCheck(layout, self.two_face[0], floor(self.two_face[1] - self.speed)) \
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

    def eventHandler(self, board):
        if self.two_face[0] % 1.0 == 0 and self.two_face[1] % 1.0 == 0:  # event logic handler
            if board[int(self.two_face[0])][int(self.two_face[1])] == 1:  # glass shard
                self.shard_score += 1
                pygame.mixer.Sound.play(glass_break)
                board[int(self.two_face[0])][int(self.two_face[1])] = 2  # after getting, set to empty space
            if self.layout[int(self.two_face[0])][int(self.two_face[1])] == 3:  # enter
                self.house_score += 1
            if board[int(self.two_face[0])][int(self.two_face[1])] == 4:  # cave
                self.cave_score += 1

    def layoutCreate(self):
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

        window.blit(self.level_bg, (0 - self.game_scroll[0], 0 - self.game_scroll[1]))  # blit BG image for level
        for i in range(len(self.layout)):
            for j in range(len(self.layout[0])):
                # if self.layout[i][j] == 0:  # 0 = background
                if self.layout[i][j] == 1:  # 1 = bug
                    shard_rect = shard_img.get_rect(center=(j * tile + tile // 2, i * tile + tile // 2))
                    window.blit(shard_img, (shard_rect.x - self.game_scroll[0], shard_rect.y - self.game_scroll[1]))
                # if self.layout[i][j] == 2:  # 2 = empty, movable spot
                # if self.layout[i][j] == 3:  # 3 = rainbow bug
                # bugRect = bugImage4.get_rect(center=(j * tile + tile // 2, i * tile + tile // 2))
                # self.shakingImage(bugImage4, bugRect.x - self.game_scroll[0], bugRect.y - self.game_scroll[1])

        self.two_face_rect = self.two_face_img.get_rect(center=(floor(self.two_face[1] * tile + tile // 2),
                                                                floor(self.two_face[0] * tile + tile // 2)))
        window.blit(self.two_face_img, (self.two_face_rect.x - self.game_scroll[0],
                                        self.two_face_rect.y - self.game_scroll[1]))
        cover_layer = pygame.surface.Surface((width, height))
        cover_layer.fill((255, 255, 255))
        cover_layer.blit(light_img, (self.two_face_rect.x - 715 - self.game_scroll[0],
                                     self.two_face_rect.y - 730 - self.game_scroll[1]))
        window.blit(cover_layer, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        pygame.display.flip()

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
        wasd_title = sub_font.render("wasd + space.", False, (207, 198, 184))
        if 200 < self.i < 500:
            window.blit(prelevel1_title, (500, 348))
            window.blit(wasd_title, (400, 560))
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
        self.eventHandler(main_level_layout)
        self.twoFaceMovement(main_level_layout)
        self.layoutCreate()
        if self.house_score == 1:
            self.i = 0
            self.state = "house"
            self.house_score = 0
            self.stopped = True
        if self.cave_score == 1:
            self.i = 0
            self.state = "cave"
            self.cave_score = 0
            self.stopped = True
        if not self.stopped:  # while spacebar is not pressed down, continue to move
            self.moves += 1

    def cave(self):
        self.keyGetter()
        self.eventHandler()
        self.twoFaceMovement()
        self.layoutCreate()
        if not self.stopped:  # while spacebar is not pressed down, continue to move
            self.moves += 1

    def house(self):
        self.keyGetter()
        self.eventHandler()
        self.twoFaceMovement()
        self.layoutCreate()
        if not self.stopped:  # while spacebar is not pressed down, continue to move
            self.moves += 1

    def stateManager(self):
        if self.state == "main_menu":
            self.mainMenu()
        if self.state == "pre_level_1":
            self.prelevel1()
        if self.state == "level_1":
            self.level1()
        if self.state == "cave":
            self.cave()
        if self.state == "house":
            self.house()


game = Game()
if __name__ == "__main__":
    while 1:  # game loop
        # clock.tick(FPS)
        game.stateManager()
