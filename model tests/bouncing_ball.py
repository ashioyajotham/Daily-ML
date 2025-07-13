import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bouncing Ball")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)

# Ball properties
ball_radius = 20
ball_x = screen_width // 4
ball_y = screen_height // 2
ball_speed_x = 4
ball_speed_y = 4

# Shape properties (a rectangle)
shape_rect = pygame.Rect(50, 50, screen_width - 100, screen_height - 100)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

def game_loop():
    """Main loop for the bouncing ball animation."""
    global ball_x, ball_y, ball_speed_x, ball_speed_y

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move the ball
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Collision with the shape's walls
        if ball_x + ball_radius > shape_rect.right or ball_x - ball_radius < shape_rect.left:
            ball_speed_x *= -1
        if ball_y + ball_radius > shape_rect.bottom or ball_y - ball_radius < shape_rect.top:
            ball_speed_y *= -1

        # Drawing everything
        screen.fill(black)  # Background
        pygame.draw.rect(screen, white, shape_rect, 2)  # Draw the shape outline
        pygame.draw.circle(screen, yellow, (ball_x, ball_y), ball_radius)  # Draw the ball

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    game_loop()
