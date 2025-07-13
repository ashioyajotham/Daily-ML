import pygame
import sys
import math

# --- Setup ---
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bouncing Ball in a Spinning Hexagon")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
blue = (100, 149, 237)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# --- Physics and Game Constants ---
gravity = 0.3  # A constant downward force
friction = 0.99 # Energy loss on bounce (0.99 means 1% loss)

# --- Ball Properties ---
ball_radius = 15
# Using pygame.Vector2 for position and velocity simplifies physics calculations
ball_pos = pygame.Vector2(screen_width / 2, screen_height / 2)
ball_vel = pygame.Vector2(0, 0)

# --- Hexagon Properties ---
hexagon_center = pygame.Vector2(screen_width / 2, screen_height / 2)
hexagon_radius = 300  # Distance from center to a vertex
hexagon_angle = 0  # Initial angle in radians
hexagon_spin_speed = 0.01  # Radians per frame

def get_hexagon_points(center, radius, angle):
    """Calculates the 6 vertices of a regular hexagon."""
    points = []
    for i in range(6):
        # 60 degrees = pi/3 radians. We calculate each point around the circle.
        point_angle = angle + i * (math.pi / 3)
        x = center.x + radius * math.cos(point_angle)
        y = center.y + radius * math.sin(point_angle)
        points.append(pygame.Vector2(x, y))
    return points

def game_loop():
    """Main loop for the physics simulation and rendering."""
    global ball_pos, ball_vel, hexagon_angle

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- Physics Update ---

        # 1. Apply gravity to the ball's velocity
        ball_vel.y += gravity

        # 2. Update the ball's position
        ball_pos += ball_vel
        
        # 3. Update the hexagon's rotation
        hexagon_angle += hexagon_spin_speed

        # --- Collision Detection and Response ---
        
        # Get the current, rotated points of the hexagon
        hex_points = get_hexagon_points(hexagon_center, hexagon_radius, hexagon_angle)

        # Check collision against each of the 6 walls
        for i in range(6):
            p1 = hex_points[i]
            p2 = hex_points[(i + 1) % 6]  # Wrap around to the first point for the last wall

            # This is the complex part: vector projection to find the closest point
            # on the wall segment to the ball.
            line_vec = p2 - p1
            point_vec = ball_pos - p1
            line_len_sq = line_vec.length_squared()

            if line_len_sq == 0: continue # Should not happen with a hexagon

            t = point_vec.dot(line_vec) / line_len_sq
            t = max(0, min(1, t)) # Clamp t to be on the segment

            closest_point = p1 + t * line_vec
            distance_vec = ball_pos - closest_point
            
            if distance_vec.length() < ball_radius:
                # A collision has occurred!
                
                # 1. Correct position to prevent sinking into the wall
                overlap = ball_radius - distance_vec.length()
                ball_pos += distance_vec.normalize() * overlap

                # 2. Calculate the reflection vector
                # The normal is perpendicular to the wall's surface
                normal = distance_vec.normalize()
                
                # Use the reflection formula: v' = v - 2 * (v . n) * n
                reflection = ball_vel - 2 * ball_vel.dot(normal) * normal
                ball_vel = reflection * friction


        # --- Drawing ---
        screen.fill(black)
        
        # Draw the spinning hexagon
        pygame.draw.polygon(screen, blue, hex_points, 5) # 5 is the line thickness

        # Draw the ball
        pygame.draw.circle(screen, yellow, (int(ball_pos.x), int(ball_pos.y)), ball_radius)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate to 60 FPS
        clock.tick(60)

if __name__ == "__main__":
    game_loop()
