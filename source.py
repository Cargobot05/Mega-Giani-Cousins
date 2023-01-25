import pygame, sys

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, picture_path):
        super().__init__()
        image_not_scaled = pygame.image.load(picture_path)
        image_size = image_not_scaled.get_size()
        self.image = pygame.transform.scale(image_not_scaled, (image_size[0]*4, image_size[1]*4))

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.direction = "right"

        self.speed = 5
        self.const_jump_vel = 16
        self.jump_vel = self.const_jump_vel
        self.lives = 3

        self.is_jumping = False

    def flip(self):
        image_not_scaled = pygame.image.load("giani_idle_" + self.direction + "_1.png")
        image_size = image_not_scaled.get_size()
        self.image = pygame.transform.scale(image_not_scaled, (image_size[0]*4, image_size[1]*4))

class Block(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, picture_path):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        image_not_scaled = pygame.image.load(picture_path)
        image_size = image_not_scaled.get_size()
        self.image = pygame.transform.scale(image_not_scaled, (image_size[0]*4, image_size[1]*4))

        self.rect = self.image.get_rect()

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
player = Player(viewport_width/2, viewport_height/2, "giani_idle_right_1.png")
player.rect.y = viewport_height - floor_height - player.rect.height

playerGroup = pygame.sprite.Group()
playerGroup.add(player)

#! Floor tiles and sprite group
# floorGroup = pygame.sprite.Group()


# block_size = pygame.image.load("block.png").get_size()
# for i in range(0, viewport_width//block_size[1], 1):
#     floor = Block(i * block_size[1], viewport_height - block_size[0], "block.png")
#     floorGroup.add(floor)


# Jump function
# def jump():

# Move function

def playerMove():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= player.speed
        if (player.direction != "left"): 
            player.direction = "left"
            player.flip()

    if keys[pygame.K_RIGHT]:
        player.rect.x += player.speed
        if (player.direction != "right"): 
            player.direction = "right"
            player.flip()
    
    if player.is_jumping is False and keys[pygame.K_UP]:
        player.is_jumping = True
        player.const_jump_vel = player.jump_vel
    
    if player.is_jumping is True:
        player.rect.y -= player.jump_vel
        player.jump_vel -= 1
        if player.jump_vel < -player.const_jump_vel:
            player.is_jumping = False
            player.jump_vel = player.const_jump_vel


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
        i -= player.speed
        player.rect.x -= player.speed
    if (player.rect.x < 200):
        i += player.speed
        player.rect.x += player.speed

    playerGroup.draw(viewport)
    #floorGroup.draw(viewport)

    # applyGravity()
    playerMove()
 
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.flip()
    clock.tick(60)