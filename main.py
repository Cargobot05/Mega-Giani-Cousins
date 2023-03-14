import pygame, random, sys

PLAYER_JUMP_VEL = 16
DIRECTION_LEFT = "left"
DIRECTION_RIGHT = "right"

VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 720
VIEWPORT_EDGE_PADDING = 400

FLOOR_HEIGHT = 97
MAX_BLOCK_HEIGHT = 500

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image_path):
        super().__init__()
        image_size = pygame.image.load(image_path).get_size()
        self.image = pygame.transform.scale(pygame.image.load(image_path), (image_size[0]*4, image_size[1]*4))

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.direction = DIRECTION_RIGHT

        self.speed = 5
        self.jump_vel = 0
        self.lives = 3

        self.is_jumping = False

    def flip(self):
        image_size = pygame.image.load("player_idle_" + self.direction + "_1.png").get_size()
        self.image = pygame.transform.scale(pygame.image.load("player_idle_" + self.direction + "_1.png"), (image_size[0]*4, image_size[1]*4))

class Block(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image_path):
        super().__init__()
        image_size = pygame.image.load(image_path).get_size()
        self.image = pygame.transform.scale(pygame.image.load(image_path), (image_size[0]*4, image_size[1]*4))

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

# Move function

def movePlayer():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= player.speed
        if (player.direction != DIRECTION_LEFT): 
            player.direction = DIRECTION_LEFT
            player.flip()

    if keys[pygame.K_RIGHT]:
        player.rect.x += player.speed
        if (player.direction != DIRECTION_RIGHT): 
            player.direction = DIRECTION_RIGHT
            player.flip()
    
    if player.is_jumping is False and (keys[pygame.K_UP] or keys[pygame.K_SPACE]):
        player.is_jumping = True
        player.jump_vel = PLAYER_JUMP_VEL
    
    if player.is_jumping is True:
        player.rect.y -= player.jump_vel
        player.jump_vel -= 1
        if player.jump_vel < -PLAYER_JUMP_VEL:
            player.is_jumping = False
            player.jump_vel = PLAYER_JUMP_VEL


def moveBackground(object, object_offset):
    viewport.blit(object, (object_offset, 0))
    viewport.blit(object, (VIEWPORT_WIDTH + object_offset, 0))
    viewport.blit(object, (-VIEWPORT_WIDTH + object_offset, 0))
    if (object_offset <= -VIEWPORT_WIDTH):
        viewport.blit(object, (VIEWPORT_WIDTH + object_offset, 0))
        object_offset = 0
    if (object_offset >= VIEWPORT_WIDTH):
        viewport.blit(object, (-VIEWPORT_WIDTH + object_offset, 0))
        object_offset = 0
    return bg_offset

def moveBlock():

    for element in blockGroup.sprites():
        if (player.direction == DIRECTION_RIGHT):
            element.rect.x -= player.speed
        if (player.direction == DIRECTION_LEFT):
            element.rect.x += player.speed

pygame.init()
clock = pygame.time.Clock()

# Game screen
viewport = pygame.display.set_mode([VIEWPORT_WIDTH, VIEWPORT_HEIGHT])
pygame.display.set_caption("Mega Giani Cousins")

# Background
bg_img = pygame.image.load("background.jpg")
bg_img = pygame.transform.scale(bg_img, (VIEWPORT_WIDTH, VIEWPORT_HEIGHT))

# Player object
player = Player(VIEWPORT_WIDTH/2, VIEWPORT_HEIGHT/2, "player_idle_right_1.png")
player.rect.y = VIEWPORT_HEIGHT - FLOOR_HEIGHT - player.rect.height

# Block objects and sprite group
blockGroup = pygame.sprite.Group()
original_block_image_size = pygame.image.load("block.png").get_size()
BLOCK_SIZE = pygame.transform.scale(pygame.image.load("block.png"), (original_block_image_size[0]*4, original_block_image_size[1]*4)).get_size()

# Random block position generator
for i in range(0, VIEWPORT_WIDTH//(2*BLOCK_SIZE[1]), 1):
    block = Block(i * 2 * BLOCK_SIZE[1], random.randint(VIEWPORT_HEIGHT -  MAX_BLOCK_HEIGHT, VIEWPORT_HEIGHT - FLOOR_HEIGHT - BLOCK_SIZE[1]), "block.png")
    blockGroup.add(block)

bg_offset = 0

running = True

while running:

    bg_offset = moveBackground(bg_img, bg_offset)

    viewport.blit(player.image, (player.rect.x, player.rect.y))
    blockGroup.draw(viewport)

    if (player.rect.x > VIEWPORT_WIDTH - VIEWPORT_EDGE_PADDING): 
        bg_offset -= player.speed
        moveBlock()
        player.rect.x -= player.speed
    if (player.rect.x < VIEWPORT_EDGE_PADDING):
        bg_offset += player.speed
        moveBlock()
        player.rect.x += player.speed

    movePlayer()
 
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.flip()
    clock.tick(60)