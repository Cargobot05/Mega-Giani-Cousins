import pygame, random, sys

PLAYER_JUMP_VEL = -16
PLAYER_SPEED = 5
GRAVITY = 1
DIRECTION_LEFT = "left"
DIRECTION_RIGHT = "right"

VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 720
VIEWPORT_EDGE_PADDING = 400

FLOOR_HEIGHT = 97
MAX_BLOCK_HEIGHT = 500

score = 0

surface_normal = 0

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image_path):
        super().__init__()
        image_size = pygame.image.load(image_path).get_size()
        self.image = pygame.transform.scale(pygame.image.load(image_path), (image_size[0]*4, image_size[1]*4))

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.direction = DIRECTION_RIGHT

        self.speed = 0
        self.vel_y = 0
        self.lives = 3

        self.is_jumping = False
        self.is_falling = False

    def flip(self):
        image_size = pygame.image.load("player_idle_" + self.direction + "_1.png").get_size()
        self.image = pygame.transform.scale(pygame.image.load("player_idle_" + self.direction + "_1.png"), (image_size[0]*4, image_size[1]*4))

class Block(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image_path):
        super().__init__()
        image_size = pygame.image.load(image_path).get_size()
        self.image = pygame.transform.scale(pygame.image.load(image_path), (image_size[0]*3, image_size[1]*3))

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image_path):
        super().__init__()
        image_size = pygame.image.load(image_path).get_size()
        self.image = pygame.transform.scale(pygame.image.load(image_path), (image_size[0], image_size[1]))

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

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
coinGroup = pygame.sprite.Group()

original_block_image_size = pygame.image.load("block.png").get_size()
BLOCK_SIZE = pygame.transform.scale(pygame.image.load("block.png"), (original_block_image_size[0]*3, original_block_image_size[1]*3)).get_size()

# Random block position generator
for i in range(0, VIEWPORT_WIDTH//BLOCK_SIZE[1]):

    platform_pos_y = random.randint(VIEWPORT_HEIGHT -  MAX_BLOCK_HEIGHT, VIEWPORT_HEIGHT - FLOOR_HEIGHT - BLOCK_SIZE[1])
    platform_length = random.randint(1,3)
    
    block = Block(i*BLOCK_SIZE[0]*2, platform_pos_y, "block.png")
    blockGroup.add(block)

    if (random.randint(0, 1) == 1):
        coin = Coin(0, 0, "coin_img.jpg")
        coin.rect.bottom = block.rect.top - coin.rect.height
        coin.rect.x = block.rect.x
        coinGroup.add(coin)

def applyPlayerGravity(surface_normal):
    player.vel_y += GRAVITY
    player.vel_y += surface_normal
    player.rect.bottom += player.vel_y

def coinCollect():
    global score
    global collisionCoin 
    collisionCoin = pygame.sprite.spritecollideany(player, coinGroup)

    if (collisionCoin != None):
        collisionCoin.kill()
        score += 1

# Move function

def movePlayer():
    
    global surface_normal
    surface_normal = 0

    if (player.vel_y > 0):
        player.is_falling = True

    if (player.rect.bottom >= VIEWPORT_HEIGHT - FLOOR_HEIGHT):
        player.rect.bottom = VIEWPORT_HEIGHT - FLOOR_HEIGHT
        player.vel_y = 0
        player.is_jumping = False
        player.is_falling = False
        surface_normal = -GRAVITY

    collisionBlock = pygame.sprite.spritecollideany(player, blockGroup)
    if(collisionBlock != None):
        
        if (player.rect.bottom >= collisionBlock.rect.top and player.rect.top < collisionBlock.rect.top and player.is_falling == True):
            
            player.rect.bottom = collisionBlock.rect.top
            player.vel_y = 0
            player.is_jumping = False
            player.is_falling = False
            surface_normal = -GRAVITY
        
        elif (player.rect.top < collisionBlock.rect.bottom and player.rect.top > collisionBlock.rect.top and player.is_jumping == True):
            
            player.vel_y = 0
            player.rect.top = collisionBlock.rect.bottom
        
        else:
            if (player.rect.right > collisionBlock.rect.left and player.rect.right < collisionBlock.rect.right):
            
                player.speed = 0
                player.vel_y = 0
                player.rect.right = collisionBlock.rect.left
        
            if (player.rect.left < collisionBlock.rect.right and player.rect.left > collisionBlock.rect.left):
                
                player.speed = 0
                player.vel_y = 0
                player.rect.left = collisionBlock.rect.right

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.speed = -PLAYER_SPEED
        if (player.direction != DIRECTION_LEFT): 
            player.direction = DIRECTION_LEFT
            player.flip()

    if keys[pygame.K_RIGHT]:
        player.speed = PLAYER_SPEED
        if (player.direction != DIRECTION_RIGHT): 
            player.direction = DIRECTION_RIGHT
            player.flip()

    if player.is_jumping is False and (keys[pygame.K_UP] or keys[pygame.K_SPACE]):
        player.is_jumping = True
        player.vel_y = PLAYER_JUMP_VEL

    player.rect.x += player.speed
    player.speed = 0
    applyPlayerGravity(surface_normal)


def moveBackground():
    global bg_offset
    
    viewport.blit(bg_img, (bg_offset, 0))
    viewport.blit(bg_img, (VIEWPORT_WIDTH + bg_offset, 0))
    viewport.blit(bg_img, (-VIEWPORT_WIDTH + bg_offset, 0))
    
    if (bg_offset <= -VIEWPORT_WIDTH):
        viewport.blit(bg_img, (VIEWPORT_WIDTH + bg_offset, 0))
        bg_offset = 0
    
    if (bg_offset >= VIEWPORT_WIDTH):
        viewport.blit(bg_img, (-VIEWPORT_WIDTH + bg_offset, 0))
        bg_offset = 0

def moveWorldSprites(objectGroup):

    for element in objectGroup.sprites():
        if (player.direction == DIRECTION_RIGHT):
            element.rect.x -= PLAYER_SPEED
        if (player.direction == DIRECTION_LEFT):
            element.rect.x += PLAYER_SPEED

bg_offset = 0

running = True

while running:

    moveBackground()

    blockGroup.draw(viewport)
    coinGroup.draw(viewport)
    viewport.blit(player.image, (player.rect.x, player.rect.y))
    font = pygame.font.SysFont('Bahnschrift', 36, False, False)
    text = font.render(f"valoare: {score}", False, (255,255,255))
    surface = text.get_rect()
    viewport.blit(text, surface)

    if (player.rect.x > VIEWPORT_WIDTH - VIEWPORT_EDGE_PADDING): 
        bg_offset -= PLAYER_SPEED
        moveWorldSprites(blockGroup)
        moveWorldSprites(coinGroup)
        player.rect.x -= PLAYER_SPEED
    if (player.rect.x < VIEWPORT_EDGE_PADDING):
        bg_offset += PLAYER_SPEED
        moveWorldSprites(blockGroup)
        moveWorldSprites(coinGroup)
        player.rect.x += PLAYER_SPEED

    movePlayer()
    coinCollect()
 
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.flip()
    clock.tick(60)