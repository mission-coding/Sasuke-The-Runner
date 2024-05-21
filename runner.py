import pygame
import sys
import random
pygame.init()

# Setup Screen/Window
screen_width = 600
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sasuke The Runner! by Vivek")

# Colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
skyblue = (135, 206, 235)

# Images
base1_img = pygame.image.load('gallery/base.png')
base1_img = pygame.transform.scale(base1_img, [screen_width, 100]).convert_alpha()

walk_img = [
    pygame.image.load('gallery/SR2.png'),
    pygame.image.load('gallery/SR3.png'),
    pygame.image.load('gallery/SR1.png')
]
jump_img = pygame.image.load('gallery/SR1.png')
suriken_img = pygame.image.load('gallery/s2.png')
die_img = pygame.image.load('gallery/Sd.png')

def game_loop():
    # Game Variables
    run = True
    over = False
    player_x = 30
    player_width = 40
    player_height = 40
    base_x = 0
    base_y = 200
    base_width = screen_width
    base_height = 100
    player_y = 115
    isjump = False
    jump_height = 7.5
    clock = pygame.time.Clock()
    fps = 30
    opstical_counter = 0
    opsticals = []
    score = 0
    walk_count = 0
    animation = True
    base1_x = 0
    base1_y = 200
    base2_x = screen_width
    base_speed = 10

    def redrawgamewin():
        nonlocal walk_count
        if animation:
            if walk_count+1 > 6:
                walk_count = 0
                
            if not isjump:
                screen.blit(walk_img[walk_count//2], (player_x, player_y))
                walk_count += 1

            if isjump:
                screen.blit(jump_img, (player_x, player_y))
                walk_count += 1

    # Making opstical and all the fuction of it
    class Opstical:
        def __init__(self):
            self.width = 40
            self.height = 40
            self.x = screen_width
            self.y = 150
            self.speed = 10
            self.ismoving = True

        def display(self):
            screen.blit(suriken_img, (self.x, self.y))
            # pygame.draw.rect(screen, red, [self.x, self.y, self.width, self.height])
            # pygame.display.update()

        def move(self):
            if self.ismoving:
                self.x -= self.speed
        
        def collision(self):
            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

            if player_rect.colliderect(self.rect) or self.rect.colliderect(player_rect):
                self.ismoving = False
    
    # Fuction to display a text
    def draw_text(text, size, color, x, y):
        font = pygame.font.Font('gallery/minecraft.otf', size)
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))
          
    while run:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()

        if not over:
            # Importing hiscore
            with open("gallery/Hiscore.txt", "r") as f:
                hiscore = f.read()

            # Making jumping effect
            if not isjump:
                if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                    isjump = True

            if isjump:
                if jump_height >= -7.5:
                    neg = 1

                    if jump_height < 0:
                        neg = -1

                    player_y -= (jump_height**2) * 0.5 * neg
                    jump_height -= 1

                else:
                    jump_height = 7.5
                    isjump = False

            # Generating opstical at some distance from each other
            if opstical_counter >= random.randint(30, 50):
                opsticals.append(Opstical())
                opstical_counter = 0
            opstical_counter += 1

            # Background
            screen.fill(skyblue)
            
            # Display, moving of opstical and collison with player
            for ops in opsticals:
                ops.move()
                ops.collision()
                if not ops.ismoving:
                    over = True

            # Movig Base
            base1_x -= base_speed
            base2_x -= base_speed

            if base1_x <= -screen_width:
                base1_x = screen_width
            if base2_x <= -screen_width:
                base2_x = screen_width
            
            # Inscreasing score
            score+=1
           
            # Increasing Hiscore
            if score >= int(hiscore):  
                hiscore = score


        if over:
            base_speed = 0
            screen.blit(die_img, [player_x, player_y])
            animation = False
            draw_text("Press Enter to Play again!", 22, red, 160, 100)

            # Restarting the game
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                game_loop()

            # Upadting the hiscore
            with open("gallery/Hiscore.txt", "w") as f:
                f.write(str(hiscore))

        # Displaying everthing 
        screen.blit(base1_img, (base1_x,base1_y))
        screen.blit(base1_img, (base2_x,base1_y))
        redrawgamewin()
        for ops in opsticals:
            ops.display()
        draw_text("Hiscore : "+str(hiscore)+"  Score : "+str(score), 18, black, 320, 20)

        clock.tick(fps)
        pygame.display.update()

game_loop()

