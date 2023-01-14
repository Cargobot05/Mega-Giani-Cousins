import pygame, sys
from pygame_functions import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]


pygame.init()
clock = pygame.time.Clock()

# Game screen
viewport_width = 1280
viewport_height = 720
viewport = pygame.display.set_mode([viewport_width, viewport_height])
pygame.display.set_caption("Mega Giani Cousins")

# Player object
player = Player(viewport_width/2, viewport_height/2, "giani_sprite.png")
sprite_image = pygame.image.load("giani_sprite.png")

playerGroup = pygame.sprite.Group()
playerGroup.add(player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.flip()
    playerGroup.draw(viewport)
    clock.tick(60)