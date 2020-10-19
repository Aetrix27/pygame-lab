import time
import pygame
import random

# Initialize Pygame
pygame.init()
pygame.display.set_caption('Get Big')

################################################################################
# VARIABLES
################################################################################

def main():
    clock = pygame.time.Clock()

    # Constants
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800
    CHARACTER_WIDTH = 40
    CHARACTER_HEIGHT = 40
    ENEMY_WIDTH = 40
    ENEMY_HEIGHT = 40
    enemy_dead = False
    player_dead = False
    player_wins = False
    enemy_wins = False
    target_player = False
    player_square_size=50
    AI_square_size=50
    time_elapsed=0

    # Color constants
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # Player Variables
    player_x = 50
    player_y = 50

    # Target Variables
    target_x = 600
    target_y = 750
    points = 0
    velocity = 10
    enemy_velocity = 10
    points = 0
    enemy_points = 0

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    circles = []

    class Circle:
        def __init__(self):
            self.x = random.randint(30,900)
            self.y = random.randint(30,700)
            self.pos = (self.x, self.y)
            self.color = GREEN
            self.size = 10

        def draw(self):
            pygame.draw.circle(screen, self.color, self.pos, self.size)

    class TextBox:
        def __init__(self, position_x, position_y, height, width, inner_color):
            self.position_x = position_x
            self.position_y = position_y
            self.size_height = height
            self.size_width = width
            self.inner_color = inner_color
            self.rect = pygame.Rect(self.position_x,self.position_y,self.size_width,self.size_height)

        def display(self, screen):
            pygame.draw.rect(screen, self.inner_color, (self.position_x, self.position_y, self.size_width, self.size_height))

    ################################################################################
    # HELPER FUNCTIONS
    ################################################################################
            
    def is_colliding(x1, y1, x2, y2, width, height, width2, height2):
        """Returns True if two shapes are colliding, or False otherwise"""
        # If one rectangle is on left side of the other 
        if (x1 >= x2 + width2) or (x2 >= x1 + width):
            return False
    
        # If one rectangle is above the other
        if (y1 >= y2 + height2) or (y2 >= y1 + height):
            return False
    
        return True

    def draw_text(text, color, font_size, x, y):
        font = pygame.font.SysFont(None, font_size)
        img = font.render(text, True, color)
        screen.blit(img, (x, y))

    intro = True
    myTextBox = TextBox(500, 200, 100, 200, WHITE)
    boxes = [myTextBox]
    myTextBox2 = TextBox(500, 400, 100, 200, WHITE)
    myTextBox3 = TextBox(500, 600, 100, 200, WHITE)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                x,y = event.pos
                if myTextBox.rect.collidepoint(x,y): 
                    intro=False
                
        screen.fill(WHITE)
        myTextBox.display(screen)
        draw_text(text=f'Start Game', color=GREEN, font_size=24, x=500, y=200)
        draw_text(text=f'Instructions: Collect dots to get bigger, the bigger square can eat the other and win.', 
        color=RED, font_size=24, x=50, y=300)
        pygame.display.update()
        clock.tick(15)
        
    ################################################################################
    # GAME LOOP
    ################################################################################

    for i in range(40):
        sizes = [10,15,20]
        current_circle=Circle()
        current_circle.size=random.choice(sizes)
        circles.append(current_circle)

    # Run until the user asks to quit

    random_circle = random.choice(circles)
    random_y = random_circle.y
    random_x = random_circle.x
    random_size = random_circle.size

    running = True
    while running:
        # Advance the clock
        clock.tick(30)
        time_delta = clock.tick(30)
        time_elapsed += time_delta

        # Did the user click the window close button?
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Update the player
        if keys[pygame.K_LEFT]:
            player_x -= velocity
        if keys[pygame.K_RIGHT]:
            player_x += velocity
        if keys[pygame.K_UP]:
            player_y -= velocity
        if keys[pygame.K_DOWN]:
            player_y += velocity

        # If target went off the screen, reset it
        if player_y < 0:
            player_y = 0
        elif player_y > SCREEN_HEIGHT:
            player_y = SCREEN_HEIGHT

        if player_x < 0: 
            player_x = 0
        elif player_x > SCREEN_WIDTH:
            player_x = SCREEN_WIDTH

        if target_y < 0:
            target_y = 0
        elif is_colliding(target_x, target_y, random_x, random_y, ENEMY_WIDTH, ENEMY_HEIGHT, random_size,random_size) and target_x > 0 and target_y>0:
            target_x += random.randint(-10,10)
            target_y += random.randint(-10,10)
        elif not is_colliding(target_x, target_y, random_x, random_y, ENEMY_WIDTH, ENEMY_HEIGHT, random_size,random_size) and target_x>0 and target_y>0:
            target_y -= random_y/30
            target_x -= random_x/30
        if time_elapsed > 500:
            target_y = target_y
            target_x = target_x
            target_y += random.randint(-10,10)
            target_y += random.randint(-10,10)

        if target_y > SCREEN_HEIGHT:
            target_y = SCREEN_HEIGHT
        if target_x < 0: 
            target_x = 0
            target_x += 10
        elif target_x > SCREEN_WIDTH:
            target_x = SCREEN_WIDTH
       
        # If player collides with target, reset it & increment points
        if is_colliding(player_x, player_y, target_x, target_y, CHARACTER_WIDTH, CHARACTER_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT):
            CHARACTER_WIDTH += enemy_points
            CHARACTER_HEIGHT += enemy_points
            if(points > enemy_points):
                enemy_dead=True
            elif(enemy_points > points):
                player_dead= True
        
        # Fill screen with white
        screen.fill(WHITE)
        for circle in circles:
            circle.draw()
        
        for circle in circles:
            if is_colliding(player_x, player_y, circle.x, circle.y, CHARACTER_WIDTH, CHARACTER_HEIGHT, circle.size, circle.size):
                circles.remove(circle)
                if circle.size == 10:
                    CHARACTER_WIDTH+=2
                    CHARACTER_HEIGHT+=2
                    points += 2
                elif circle.size == 15:
                    CHARACTER_WIDTH+=5
                    CHARACTER_HEIGHT+=5
                    points += 5
                elif circle.size == 20:
                    CHARACTER_WIDTH += 10
                    CHARACTER_HEIGHT += 10
                    points += 10

        for circle in circles:
            if is_colliding(target_x, target_y, circle.x, circle.y, ENEMY_WIDTH, ENEMY_HEIGHT, circle.size, circle.size):
                circles.remove(circle)
                if circle.size == 10:
                    ENEMY_WIDTH+=2
                    ENEMY_HEIGHT+=2
                    enemy_points += 2
                elif circle.size == 15:
                    ENEMY_WIDTH+=5
                    ENEMY_HEIGHT+=5
                    enemy_points += 5
                elif circle.size == 20:
                    ENEMY_WIDTH += 10
                    ENEMY_HEIGHT += 10
                    enemy_points += 10

        if enemy_dead==False:
            pygame.draw.rect(screen, RED, (target_x, target_y, ENEMY_WIDTH, ENEMY_HEIGHT))
        elif enemy_dead==True:
            player_wins = True
            running = False

        if player_dead == False:
            pygame.draw.rect(screen, BLUE, (player_x, player_y, CHARACTER_WIDTH, CHARACTER_HEIGHT))
        elif player_dead == True:
            enemy_wins = True
            running = False

        # Draw the points
        draw_text(text=f'Score: {points}', color=BLACK, font_size=24, x=20, y=20)
        # Update the game display
        pygame.display.update() 

    while player_wins == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                x,y = event.pos
                if myTextBox.rect.collidepoint(x,y): 
                    player_wins = False
                    return main()
                elif myTextBox3.rect.collidepoint(x,y):
                    pygame.quit()
                    quit()

        screen.fill(WHITE)
        myTextBox2.display(screen)
        myTextBox3.display(screen)
        draw_text(text=f'Game Over!, You Win!', color=GREEN, font_size=35, x=500, y=200)
        draw_text(text=f'Play Again?', color=BLACK, font_size=35, x=500, y=400)
        draw_text(text=f'Quit', color=BLACK, font_size=35, x=500, y=600)
        pygame.display.update()
        clock.tick(15)

    while enemy_wins == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                x,y = event.pos
                if myTextBox2.rect.collidepoint(x,y): 
                    enemy_wins = False
                    return main()
                elif myTextBox3.rect.collidepoint(x,y):
                    pygame.quit()
                    quit()

        screen.fill(WHITE)
        myTextBox2.display(screen)
        myTextBox3.display(screen)
        draw_text(text=f'Game Over!, You Lose!', color=RED, font_size=35, x=500, y=200)
        draw_text(text=f'Play Again?', color=BLACK, font_size=35, x=500, y=400)
        draw_text(text=f'Quit', color=BLACK, font_size=35, x=500, y=600)
        pygame.display.update()
        clock.tick(15)

main()

