import pygame
import math

pygame.init()


WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.SysFont('Calibri', 36)
text_color = (255, 255, 255)
fps = 60
timer = pygame.time.Clock()

gravity = 0.5
bounce_stop = 0.3
mouse_trajectory = []
colCount = 0

class Ball:
    def __init__(self, x_pos, y_pos, radius, color, mass, retention, y_speed, x_speed, id, friction):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color
        self.mass = mass
        self.retention = retention
        self.y_speed = y_speed
        self.x_speed = x_speed
        self.id = id
        self.circle = ''
        self.selected = False
        self.friction = friction
        
    def draw(self):
        self.circle = pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)
    
    def check_gravity(self):
        if not self.selected:
            if self.y_pos < HEIGHT - self.radius - 5:
                self.y_speed += gravity
            else:
                if self.y_speed > bounce_stop:
                    self.y_speed = self.y_speed * -1 * self.retention
                else:
                    if abs(self.y_speed) <= bounce_stop:
                        self.y_speed = 0
            if (self.x_pos < self.radius + 5 and self.x_speed < 0) or (self.x_pos > WIDTH - self.radius - 5 and self.x_speed > 0):
                self.x_speed *= -1 * self.retention
                if abs(self.x_speed) < bounce_stop:
                    self.x_speed = 0
            if self.y_speed == 0 and self.x_speed != 0:
                if self.x_speed > 0:
                    self.x_speed -= self.friction
                elif self.x_speed < 0:
                    self.x_speed += self.friction
            
        else:
            self.x_speed = x_push
            self.y_speed = y_push
        return self.y_speed
        
            
    
    def update_pos(self, mouse):
        if not self.selected:
            self.y_pos += self.y_speed
            self.x_pos += self.x_speed
        else:
            self.x_pos = mouse[0]
            self.y_pos = mouse[1]
    
    def check_select(self, pos):
        self.selected = False
        if self.circle.collidepoint(pos):
            self.selected = True
        return self.selected
        
def draw_collision_counter(screen, font, count):
    text_surface = font.render(f"Collisions: {count}", True, text_color)
    screen.blit(text_surface, (10, 10))

def draw_walls():
    left = pygame.draw.line(screen, 'white', (0,0), (0, HEIGHT), 10)
    right = pygame.draw.line(screen, 'white', (WIDTH,0), (WIDTH, HEIGHT), 10)
    top = pygame.draw.line(screen, 'white', (0,0), (WIDTH, 0), 10)
    bottom = pygame.draw.line(screen, 'white', (0,HEIGHT), (WIDTH, HEIGHT), 10)
    wall_list = [left, right, top, bottom]
    return wall_list
def calc_motion_vector():
    x_speed = 0
    y_speed = 0
    if len(mouse_trajectory) > 10:
        x_speed = ((mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / len(mouse_trajectory))
        y_speed = ((mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / len(mouse_trajectory))
    return x_speed, y_speed
def check_ball_collision(ball1, ball2):
    global colCount
    dx = ball2.x_pos - ball1.x_pos
    dy = ball2.y_pos - ball1.y_pos
    distance = math.hypot(dx, dy)
    min_dist = ball1.radius + ball2.radius

    if distance < min_dist: 
        colCount += 1 
        if distance == 0:  
            nx, ny = 1, 0  
        else:
            nx = dx / distance
            ny = dy / distance
        rvx = ball2.x_speed - ball1.x_speed
        rvy = ball2.y_speed - ball1.y_speed
        vel_along_normal = rvx * nx + rvy * ny   
              
        if vel_along_normal > 0:
            return         
        
        e = min(ball1.retention, ball2.retention)    
        j = -(1 + e) * vel_along_normal
        j /= (1 / ball1.mass + 1 / ball2.mass)   
        impulse_x = j * nx
        impulse_y = j * ny
        
        ball1.x_speed -= impulse_x / ball1.mass
        ball1.y_speed -= impulse_y / ball1.mass
        ball2.x_speed += impulse_x / ball2.mass
        ball2.y_speed += impulse_y / ball2.mass
        
        
        penetration_depth = min_dist - distance
        percent = 0.4  
        correction = penetration_depth * percent / (1 / ball1.mass + 1 / ball2.mass)
        
        correction_x = correction * nx
        correction_y = correction * ny
        
        ball1.x_pos -= correction_x / ball1.mass
        ball1.y_pos -= correction_y / ball1.mass
        ball2.x_pos += correction_x / ball2.mass
        ball2.y_pos += correction_y / ball2.mass

ball1 = Ball(50, 50, 30, 'crimson', 100, .9, 0, 0, 1, 0.02)
ball2 = Ball(500, 500, 50, 'indigo', 400, .9, 0, 0, 2, 0.03)
ball3 = Ball(200, 200, 40, 'beige', 300, .9, 0, 0, 3, 0.04)
balls = [ball1, ball2, ball3]



run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    draw_collision_counter(screen, font, colCount)
    mouse_coords = pygame.mouse.get_pos()
    mouse_trajectory.append(mouse_coords)
    if len(mouse_trajectory) > 20:
        mouse_trajectory.pop(0)
    x_push, y_push = calc_motion_vector()

    
    walls = draw_walls()

    
    for ball in balls:
        ball.update_pos(mouse_coords)
    
    
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            check_ball_collision(balls[i], balls[j])
            

    
    for ball in balls:
        ball.y_speed = ball.check_gravity()

    
    for ball in balls:
        ball.draw()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for ball in balls:
                    ball.check_select(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for ball in balls:
                    ball.selected = False 
    pygame.display.flip()
pygame.quit()