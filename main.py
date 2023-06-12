import asyncio
from math import floor
import pygame, random, sys

PLAYER_JUMP_VEL = -18
PLAYER_SPEED = 5
GRAVITY = 1
DIRECTION_LEFT = "left"
DIRECTION_RIGHT = "right"

VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 720
VIEWPORT_EDGE_PADDING = 400

original_block_image_size = pygame.image.load("block.png").get_size()
BLOCK_SIZE = pygame.transform.scale(pygame.image.load("block.png"), (original_block_image_size[0]*3, original_block_image_size[1]*3)).get_size()[0]

FLOOR_HEIGHT = 97
MAX_BLOCK_HEIGHT = BLOCK_SIZE * 5 - pygame.image.load("player_idle_left_1.png").get_size()[0]

COINS = "coins"
GROUND_FIGHT = "ground fight"
BIRD_ATTACK_ = "bird attack"

score = 0

surface_normal = 0
bg_offset = 0

generate_platforms = True
game_stage = COINS

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image_path):
        super().__init__()
        image_size = pygame.image.load(image_path).get_size()
        self.image = pygame.transform.scale(pygame.image.load(image_path), (BLOCK_SIZE - 5, (BLOCK_SIZE - 5)*image_size[1]/image_size[0]))

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
        self.image = pygame.transform.scale(pygame.image.load("player_idle_" + self.direction + "_1.png"),  (BLOCK_SIZE - 5, (BLOCK_SIZE - 5)*image_size[1]/image_size[0]))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, pos_x, bottom_pos_y, movement_speed, image_path):
        super().__init__()
        image_size = pygame.image.load(image_path).get_size()
        self.image = pygame.transform.scale(pygame.image.load(image_path), (BLOCK_SIZE, (BLOCK_SIZE)*image_size[1]/image_size[0]))

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.bottom = bottom_pos_y

        self.type = type

        self.movement_speed = movement_speed
        self.direction = DIRECTION_LEFT

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def attack(self):
        if (self.direction == DIRECTION_RIGHT):
            if (self.rect.x < player.rect.x):
                self.rect.x += self.movement_speed
            else:
                #await asyncio.sleep(2)
                self.direction = DIRECTION_LEFT
                self.flip()
        if (self.direction == DIRECTION_LEFT):
            if (self.rect.x > player.rect.x):
                self.rect.x -= self.movement_speed
            else:
                #await asyncio.sleep(2)
                self.direction = DIRECTION_RIGHT
                self.flip()
        
class Block(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image_path):
        super().__init__()
        image_size = pygame.image.load(image_path).get_size()
        self.image = pygame.transform.scale(pygame.image.load(image_path), (image_size[0]*3, image_size[1]*3))

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image_path, value):
        super().__init__()
        image_size = pygame.image.load(image_path).get_size()

        self.image = pygame.transform.scale(pygame.image.load(image_path), (image_size[0], image_size[1]))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        if (value == 1):
            self.value = 1
        if (value == 2):
            self.value = 5
        if (value == 3):
            self.value = 10

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
block_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# Random block position generator
def apply_player_gravity(surface_normal):
    player.vel_y += GRAVITY
    player.vel_y += surface_normal
    player.rect.bottom += player.vel_y

def collect_coin():
    global score
    global collision_coin
    collision_coin = pygame.sprite.spritecollideany(player, coin_group)

    if (collision_coin != None):
        score += collision_coin.value
        collision_coin.kill()

def check_top_collision(collision_block):
    return (player.rect.bottom >= collision_block.rect.top and 
                player.rect.bottom <= collision_block.rect.bottom - 5 and 
                player.rect.top < collision_block.rect.top)

def check_bottom_collision(collision_block):
    return (player.rect.top < collision_block.rect.bottom and 
            player.rect.top > collision_block.rect.top and player.is_jumping == True)

def check_left_collision(collision_block):
    return (player.rect.right > collision_block.rect.left and player.rect.right < collision_block.rect.right)

def check_right_collision(collision_block):
    return (player.rect.left < collision_block.rect.right and player.rect.left > collision_block.rect.left)


# Move function
def move_player():
    global surface_normal
    surface_normal = 0

    if (player.vel_y > 0):
        player.is_falling = True
    if (player.vel_y < 0):
        player.is_jumping = True

    if (player.rect.bottom >= VIEWPORT_HEIGHT - FLOOR_HEIGHT):
        player.rect.bottom = VIEWPORT_HEIGHT - FLOOR_HEIGHT
        player.vel_y = 0
        player.is_jumping = False
        player.is_falling = False
        surface_normal = -GRAVITY
    
    for i in range(0, 2):
        collision_block = pygame.sprite.spritecollideany(player, block_group)
        if(collision_block != None):
            if (check_top_collision(collision_block)): 
                player.rect.bottom = collision_block.rect.top
                player.vel_y = 0
                player.is_jumping = False
                player.is_falling = False
                surface_normal = -GRAVITY
            
            elif (check_bottom_collision(collision_block)):
                player.vel_y = 0
                player.rect.top = collision_block.rect.bottom
            
            else:
                if (check_left_collision(collision_block)):
                    player.speed = 0
                    player.vel_y = 0
                    player.rect.right = collision_block.rect.left
            
                if (check_right_collision(collision_block)):
                    
                    player.speed = 0
                    player.vel_y = 0
                    player.rect.left = collision_block.rect.right

    for block in block_group:
        if check_top_collision(block) and (check_left_collision(block) or check_right_collision(block)):
            surface_normal = -GRAVITY


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
    apply_player_gravity(surface_normal)


def move_background():
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

def move_world_sprites(objectGroup):
    for element in objectGroup.sprites():
        if (player.direction == DIRECTION_RIGHT):
            element.rect.x -= PLAYER_SPEED
        if (player.direction == DIRECTION_LEFT):
            element.rect.x += PLAYER_SPEED

running = True
stage_start = False
scene_count = 0

while running:
    print (surface_normal)
    move_background()
    move_player()
    collect_coin()

    block_group.draw(viewport)
    coin_group.draw(viewport)
    enemy_group.draw(viewport)
    viewport.blit(player.image, (player.rect.x, player.rect.y))
    font = pygame.font.SysFont('Bahnschrift', 36, False, False)
    text = font.render(f"valoare: {score}", False, (255,255,255))
    surface = text.get_rect()
    viewport.blit(text, surface)

    if (generate_platforms == True and bg_offset == 0 and game_stage == COINS):
        for i in range(1, VIEWPORT_WIDTH//(BLOCK_SIZE), 3):
            platform_pos_y = random.randint(1, 6) * (BLOCK_SIZE) + MAX_BLOCK_HEIGHT
            platform_pos_x = VIEWPORT_WIDTH + i*BLOCK_SIZE

            platform_block_number = random.randint(1, 4)
            
            for j in range(1, platform_block_number, 1):
                block = Block(platform_pos_x + j*BLOCK_SIZE, platform_pos_y, "block.png")
                if (random.randint(0, 5) == 1):
                    coin_value = random.randint(1, 3)
                    coin = Coin(0, 0, "coin_img_" + str(coin_value) + ".jpg", coin_value)
                    coin.rect.bottom = block.rect.top - coin.rect.height
                    coin.rect.x = block.rect.x
                    coin_group.add(coin)
                block_group.add(block)

    if (bg_offset == -VIEWPORT_WIDTH + 5): scene_count += 1
    
    generate_platforms = False

    if (game_stage == GROUND_FIGHT):
        if (stage_start == True):
            crow = Enemy("stabby crow", VIEWPORT_WIDTH, VIEWPORT_HEIGHT - FLOOR_HEIGHT, 2, "stabby_crow.png")
            enemy_group.add(crow)
            stage_start = False
        crow.attack()

    if (game_stage == COINS):
        if (player.rect.x > VIEWPORT_WIDTH - VIEWPORT_EDGE_PADDING): 
            bg_offset -= PLAYER_SPEED
            move_world_sprites(block_group)
            move_world_sprites(coin_group)
            move_world_sprites(enemy_group)
            player.rect.x -= PLAYER_SPEED
        if (player.rect.x < VIEWPORT_EDGE_PADDING):
            bg_offset += PLAYER_SPEED
            move_world_sprites(block_group)
            move_world_sprites(coin_group)
            move_world_sprites(enemy_group)
            player.rect.x += PLAYER_SPEED
    else:
        if (player.rect.right > VIEWPORT_WIDTH):
            player.rect.x -= PLAYER_SPEED
        if (player.rect.left < 0):
            player.rect.x += PLAYER_SPEED

    if (bg_offset != 0 and player.rect.x != 0 and scene_count <= 3):
        generate_platforms = True

    if (scene_count == 5 and game_stage == COINS):
        game_stage = GROUND_FIGHT
        stage_start = True
        block_group.empty() 
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.flip()
    clock.tick(60)