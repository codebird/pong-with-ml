import math
import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# This class represents the ball
# It derives from the "Sprite" class in Pygame
class Ball(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create the image of the ball
        self.image = pygame.Surface([10, 10])

        # Color the ball
        self.image.fill(WHITE)

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # Get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        # Speed in pixels per cycle
        self.speed = 0

        # Floating point representation of where the ball is
        self.x = 0
        self.y = 0

        # Direction of ball in degrees
        self.direction = 0

        # Height and width of the ball
        self.width = 10
        self.height = 10

        # Set the initial ball speed and position
        self.reset()

    def reset(self):
        self.x = 400.0
        self.y = random.randrange(50, 500)
        self.speed = 8.0

        # Direction of ball (in degrees)
        self.direction = 90 #random.randrange(-15, 15)

        # Flip a 'coin'
        if random.randrange(2) == 0:
            # Reverse ball direction, let the other guy get it first
            self.direction += 180
            self.y = 50

    # This function will bounce the ball off a horizontal surface (not a vertical one)
    def bounce_x(self, diff):
        self.direction = (180 - self.direction) % 360
        self.direction -= diff

        # Speed the ball up
        self.speed *= 1.1
    def bounce_y(self, diff):
        self.direction = (360 - self.direction) % 360
        self.direction -= diff

        # Speed the ball up
        self.speed *= 1.1

    # Update the position of the ball
    def update(self):
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        if self.x < -700 or self.x > 1500:
            print(self.x)
            self.reset()

        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y

        # Do we bounce off the left of the screen?
        if self.y <= 0 or self.y > self.screenheight - self.height:
            self.bounce_x(0)


# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self, x_pos, width, height):
        # Call the parent's constructor
        super().__init__()

        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect.x = x_pos
        self.rect.y = 0

    # Update the player
    def update(self):
        # Move x according to the axis. We multiply by 15 to speed up the movement.
        self.rect.y = int(pygame.mouse.get_pos()[1])
        # Make sure we don't push the player paddle off the right side of the screen
        if self.rect.y > self.screenheight - self.height:
            self.rect.y = self.screenheight - self.height
        if self.rect.y < 0:
            self.rect.y = 0 + self.height / 2
    def update_where_ball_is(self, ball):
        horiz_axis_pos = ball.rect.x
        self.rect.y = int(ball.rect.y) - self.height / 2
        # Make sure we don't push the player paddle off the right side of the screen
        if self.rect.y > self.screenheight - self.height:
            self.rect.y = self.screenheight - self.height
        if self.rect.y < 0:
            self.rect.y = 0 + self.height / 2


score1 = 0
score2 = 0

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

# Set the title of the window
pygame.display.set_caption('Pong')

# Enable this to make the mouse disappear when over our window
pygame.mouse.set_visible(1)

# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Create the ball
ball = Ball()
# Create a group of 1 ball (used in checking collisions)
balls = pygame.sprite.Group()
balls.add(ball)

# Create the player paddle object
player1 = Player(785, 15, 75)
player2 = Player(0, 15, 75)

movingsprites = pygame.sprite.Group()
movingsprites.add(player1)
movingsprites.add(player2)
movingsprites.add(ball)

clock = pygame.time.Clock()
done = False
exit_program = False
f = open('data', 'w')
print('bx,by,bdirection,bspeed,py', file=f)
while not exit_program:

    # Clear the screen
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True

    # Stop the game if there is an imbalance of 3 points
    #if abs(score1 - score2) > 3:
    #    done = True

    if not done:
        # Update the player and ball positions
        print(f'{ball.x},{ball.y},{ball.direction},{ball.speed},{player1.rect.y}', file=f)
        player1.update()
        player2.update_where_ball_is(ball)
        ball.update()

    # If we are done, print game over
    if done:
        text = font.render("Game Over", 1, (200, 200, 200))
        textpos = text.get_rect(centerx=background.get_width() / 2)
        textpos.top = 50
        screen.blit(text, textpos)

    # See if the ball hits the player paddle
    if pygame.sprite.spritecollide(player1, balls, False):
        # The 'diff' lets you try to bounce the ball left or right depending where on the paddle you hit it
        diff = (player1.rect.x + player1.width / 2) - (ball.rect.x + ball.width / 2)
        # Set the ball's y position in case we hit the ball on the edge of the paddle
        ball.x = 784
        ball.bounce_y(diff)
        score1 += 1

    # See if the ball hits the player paddle
    if pygame.sprite.spritecollide(player2, balls, False):
        # The 'diff' lets you try to bounce the ball left or right depending where on the paddle you hit it
        diff = (player2.rect.x + player2.width / 2) - (ball.rect.x + ball.width / 2)
        # Set the ball's y position in case we hit the ball on the edge of the paddle
        ball.x = 16
        ball.bounce_y(diff)
        score2 += 1

    # Print the score
    scoreprint = "Player 1: " + str(score1)
    text = font.render(scoreprint, 1, WHITE)
    textpos = (0, 0)
    screen.blit(text, textpos)

    scoreprint = "Player 2: " + str(score2)
    text = font.render(scoreprint, 1, WHITE)
    textpos = (300, 0)
    screen.blit(text, textpos)

    # Draw Everything
    movingsprites.draw(screen)

    # Update the screen
    pygame.display.flip()

    clock.tick(30)

pygame.quit()