import pygame
import sys
import random
import asyncio

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15
PADDLE_SPEED = 5
BALL_SPEED = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Set up the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Font for scoring
font = pygame.font.Font(None, 74)

# Initialize sound effects with silent defaults
try:
    paddle_sound = pygame.mixer.Sound("paddle.wav")
    score_sound = pygame.mixer.Sound("score.wav")
except:
    # If sound files are missing, create silent sounds
    paddle_sound = pygame.mixer.Sound(buffer=bytes([0]*44))  # Empty sound
    score_sound = pygame.mixer.Sound(buffer=bytes([0]*44))   # Empty sound

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.score = 0
        self.speed = PADDLE_SPEED

    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        if not up and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.rect = pygame.Rect(WINDOW_WIDTH // 2 - BALL_SIZE // 2,
                              WINDOW_HEIGHT // 2 - BALL_SIZE // 2,
                              BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED * random.choice((1, -1))
        self.speed_y = BALL_SPEED * random.choice((1, -1))

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Ball collision with top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.speed_y *= -1

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

def handle_collision():
    # Ball collision with paddles
    if ball.rect.colliderect(player.rect) or ball.rect.colliderect(opponent.rect):
        ball.speed_x *= -1.1  # Increase speed slightly on paddle hits
        paddle_sound.play()

def handle_scoring():
    # Ball out of bounds
    if ball.rect.left <= 0:
        opponent.score += 1
        score_sound.play()
        return True
    elif ball.rect.right >= WINDOW_WIDTH:
        player.score += 1
        score_sound.play()
        return True
    return False

def draw_game():
    screen.fill(BLACK)
    
    # Draw center line
    pygame.draw.aaline(screen, WHITE, (WINDOW_WIDTH // 2, 0), (WINDOW_WIDTH // 2, WINDOW_HEIGHT))
    
    # Draw scores
    player_text = font.render(str(player.score), True, WHITE)
    opponent_text = font.render(str(opponent.score), True, WHITE)
    screen.blit(player_text, (WINDOW_WIDTH // 4, 20))
    screen.blit(opponent_text, (3 * WINDOW_WIDTH // 4, 20))
    
    # Draw game objects
    player.draw()
    opponent.draw()
    ball.draw()
    
    pygame.display.flip()

async def main():
    global player, opponent, ball
    
    # Create game objects
    player = Paddle(50, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    opponent = Paddle(WINDOW_WIDTH - 50 - PADDLE_WIDTH, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    # Reset game
                    ball.reset()
                    player.score = opponent.score = 0
        
        keys = pygame.key.get_pressed()
        
        # Player 1 controls (W/S keys)
        if keys[pygame.K_w]:
            player.move(up=True)
        if keys[pygame.K_s]:
            player.move(up=False)
            
        # Player 2 controls (Up/Down arrows)
        if keys[pygame.K_UP]:
            opponent.move(up=True)
        if keys[pygame.K_DOWN]:
            opponent.move(up=False)
        
        # Move ball
        ball.move()
        
        # Handle collisions
        handle_collision()
        
        # Handle scoring
        if handle_scoring():
            ball.reset()
        
        # Draw everything
        draw_game()
        
        # Control game speed
        clock.tick(FPS)
        
        # Required for web deployment
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main()) 