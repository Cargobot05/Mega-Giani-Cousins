import pygame, sys

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, picture_path):
        super().__init__()
        image_not_scaled = pygame.image.load(picture_path)
        image_size = image_not_scaled.get_size()
        self.image = pygame.transform.scale(image_not_scaled, (image_size[0]/3, image_size[1]/3))

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.direction = "right"

    def flip(self):
        image_not_scaled = pygame.image.load("giani_sprite_" + self.direction + ".png")
        image_size = image_not_scaled.get_size()
        self.image = pygame.transform.scale(image_not_scaled, (image_size[0]/3, image_size[1]/3))

pygame.init()
clock = pygame.time.Clock()

# Game screen
viewport_width = 1280
viewport_height = 720
viewport = pygame.display.set_mode([viewport_width, viewport_height])
pygame.display.set_caption("Mega Giani Cousins")

# Defining floor value

floor_height = 97

# Background
bg_img = pygame.image.load("background.jpg")
bg_img = pygame.transform.scale(bg_img, (viewport_width, viewport_height))

# Player object
player = Player(viewport_width/2, viewport_height/2, "giani_sprite_right.png")
player.rect.y = viewport_height - floor_height - player.rect.height

playerGroup = pygame.sprite.Group()
playerGroup.add(player)

# Jump function
def jump():
    player.rect.y -= 150

# Move function

def playerMove():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= 5
        if (player.direction != "left"): 
            player.direction = "left"
            player.flip()

    if keys[pygame.K_RIGHT]:
        player.rect.x += 5
        if (player.direction != "right"): 
            player.direction = "right"
            player.flip()
# Input function

def checkUserInput(e):
    if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_SPACE: return "jump"
        if e.key == pygame.K_UP: return "jump"
        if e.key == pygame.K_RIGHT: return "right"
        if e.key == pygame.K_LEFT: return "left"

def applyGravity():
    if player.rect.y < viewport_height - floor_height - player.rect.height:
        player.rect.y += 3.5


running = True
i = 0

while running:
    
    viewport.fill((0,0,0))
    viewport.blit(bg_img, (i, 0))
    viewport.blit(bg_img, (viewport_width+i, 0))
    viewport.blit(bg_img, (-viewport_width+i, 0))
    if (i <= -viewport_width):
        viewport.blit(bg_img, (viewport_width+i, 0))
        i = 0
    if (i >= viewport_width):
        viewport.blit(bg_img, (-viewport_width+i, 0))
        i = 0
    if (player.rect.x > viewport_width - 200): 
        i -= 5
        player.rect.x -= 5
    if (player.rect.x < 200):
        i += 5
        player.rect.x += 5

    playerGroup.draw(viewport)

    applyGravity()
    playerMove()

    
    for event in pygame.event.get():
        if checkUserInput(event) == "jump": 
            jump()
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.flip()
    clock.tick(60)