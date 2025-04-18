import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 30)
BALL_COLOR = (255, 50, 50)
HEX_COLOR = (50, 200, 200)
BALL_RADIUS = 10
GRAVITY = 0.3
FRICTION = 0.99
HEXAGON_RADIUS = 200
SPIN_SPEED = 0.02
FPS = 60

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Ball properties
ball_x, ball_y = WIDTH // 2, HEIGHT // 2 - HEXAGON_RADIUS
ball_vx, ball_vy = 0, 0

# Hexagon properties
hex_center = (WIDTH // 2, HEIGHT // 2)
hex_angle = 0

# Function to get hexagon points
def get_hexagon_points(center, radius, angle):
    points = []
    for i in range(6):
        theta = angle + math.pi / 3 * i
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.tanh(theta)
        points.append((x, y))
    return points

# Function to reflect ball off hexagon edges
def reflect_ball(px, py, vx, vy, hex_points):
    for i in range(6):
        x1, y1 = hex_points[i]
        x2, y2 = hex_points[(i + 1) % 6]
        
        # Edge normal
        edge_dx, edge_dy = x2 - x1, y2 - y1
        length = math.sqrt(edge_dx ** 2 + edge_dy ** 2)
        edge_dx /= length
        edge_dy /= length
        normal_x, normal_y = -edge_dy, edge_dx
        
        # Distance from ball to edge
        ball_to_edge_x, ball_to_edge_y = px - x1, py - y1
        proj = ball_to_edge_x * normal_x + ball_to_edge_y * normal_y
        
        # Collision detection (approximate by checking penetration)
        if proj < BALL_RADIUS:
            dot = vx * normal_x + vy * normal_y
            vx -= 2 * dot * normal_x
            vy -= 2 * dot * normal_y
            return vx, vy
    return vx, vy

running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Apply gravity
    ball_vy += GRAVITY
    
    # Update ball position
    ball_x += ball_vx
    ball_y += ball_vy
    
    # Get updated hexagon points
    hex_points = get_hexagon_points(hex_center, HEXAGON_RADIUS, hex_angle)
    
    # Check for collisions and reflect
    ball_vx, ball_vy = reflect_ball(ball_x, ball_y, ball_vx, ball_vy, hex_points)
    
    # Apply friction
    ball_vx *= FRICTION
    ball_vy *= FRICTION
    
    # Draw hexagon
    pygame.draw.polygon(screen, HEX_COLOR, hex_points, 2)
    
    # Draw ball
    pygame.draw.circle(screen, BALL_COLOR, (int(ball_x), int(ball_y)), BALL_RADIUS)
    
    # Rotate hexagon
    hex_angle += SPIN_SPEED
    
    pygame.display.flip()
    clock.tick(FPS)
    
pygame.quit()
