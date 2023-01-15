import pygame, sys

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, picture_path):
        super().__init__()
        image_not_scaled = pygame.image.load(picture_path)
        image_size = image_not_scaled.get_size()
        self.image = pygame.transform.scale(image_not_scaled, (image_size[0]/4, image_size[1]/4))

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

pygame.init()
clock = pygame.time.Clock()

# Game screen
viewport_width = 1280
viewport_height = 720
viewport = pygame.display.set_mode([viewport_width, viewport_height])
pygame.display.set_caption("Mega Giani Cousins")

# Defining floor value

floor_height = 95

# Background
bg_img = pygame.image.load("background.jpg")
bg_img = pygame.transform.scale(bg_img, (viewport_width, viewport_height))

# Player object
player = Player(viewport_width/2, viewport_height/2, "giani_sprite.png")
player.rect.y = viewport_height - floor_height - player.rect.height

playerGroup = pygame.sprite.Group()
playerGroup.add(player)

# Jump function
def jump():
    player.rect.y -= 150

# Input function

def checkJump(e):
    if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_SPACE: return True
    
    return False

def applyGravity():
    if player.rect.y < viewport_height - floor_height - player.rect.height:
        player.rect.y += 3.5


running = True
i = 0

while running:
    
    viewport.fill((0,0,0))
    viewport.blit(bg_img, (i, 0))
    viewport.blit(bg_img, (viewport_width+i, 0))
    if (i == -viewport_width):
        viewport.blit(bg_img, (viewport_width+i, 0))
        i = 0
    i -= 1
    playerGroup.draw(viewport)

    applyGravity()
    
    for event in pygame.event.get():
        if checkJump(event): 
           jump()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.flip()
    clock.tick(60)