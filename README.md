# Mega-Giani-Cousins

OBJECTS/CLASSES

player --> Player class object
 - attributes:
    > player.image = sprite image
    > player.rect.x / player.rect.y = position
    > player.direction = direction of movement
    > player.jump_vel = jump velocity
    > player.is_jumping = jump status (bool value)
    > player.lives  = number of lives
    > player.speed = movement speed of player sprite
 - methods:
    > flip --> changes the sprite image according to the direction of movement

block --> Block class object
 - attributes:
    > block.image = texture
    > block.rect = pygame rect attributes (position, width, height, limits)
    > block.rect.x = position on the x axis
    > block.rect.y = position on the y axis

FUNCTIONS

 - movePlayer --> handles all player movement
    > left/right movement:
        >> checks user input
        >> changes sprite direction if it differs from the one specified by the user
        >> calls the flip() function of the player object ( player.flip() ) to switch to the according texture
    > jumping:
        >> checks user input
        >> if player sprite isn't jumping, function initates the jumping process, setting player jumping status to true
        >> while the function is being called and the player status is set to jump, it modifies the parameters accordingly.

VARIABLES

 - viewport --> rendering surface
 - bg_img --> stores the background image scaled to the size of the viewport
 - running --> bool variable for controlling the execution loop
 - bg_offset --> counter variable for keeping track of the world movement

OTHER ALGORITHMS

 - "Random block position generator" --> creates block objects form Block class with random height postitions across the screen

EXECUTION LOOP

 - background is moved according to player movement
 - player sprite is drawn on the viewport
 - block sprite group is drawn on the viewport
 - player movement function is called ( playerMove() )
 - quit event is being monitored