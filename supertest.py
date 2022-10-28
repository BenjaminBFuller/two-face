import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
light = pygame.image.load('imgs/lightsource.png').convert_alpha()
light = pygame.transform.scale(light, (400, 400))
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: break
    else:
        screen.fill(pygame.color.Color('Red'))
        for x in range(0, 640, 20):
            pygame.draw.line(screen, pygame.color.Color('Green'), (x, 0), (x, 480), 3)
        cover = pygame.surface.Surface((640, 480))
        cover.fill((255, 255, 255))
        cover.blit(light, (100, 100))
        screen.blit(cover, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        pygame.display.flip()
        continue
    break
