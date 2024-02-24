import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 1600, 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Boids Simulation")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# World limits
world_x1,world_xlen = screen_width/10, screen_width - 2*(screen_width/10)
world_y1,world_ylen = screen_height/10, screen_height - 2*(screen_height/10)

# Seperation


# Dynamic constraints


# Define Boid class
class Boid:
    def __init__(self):
        self.x = 1000 # random.randint(world_x1, world_x1+world_xlen)
        self.y = 700 # random.randint(world_y1, world_y1+world_ylen)
        self.v = 4 #random.randint(3,6)
        self.theta = random.uniform(0, math.pi * 2)
        self.phi = -math.atan2(screen_height/2 - self.y, self.x - screen_width/2)
        print(self.x, self.y)

    def update(self):
        self.x += self.v * math.cos(self.theta)
        self.y += self.v * math.sin(self.theta)
        # self.theta = self.phi+math.pi/2
        self.phi = -math.atan2(screen_height/2 - self.y, self.x - screen_width/2)
        print(self.x, self.y)

        # Wrap around screen edges
        if self.x < world_x1:
            self.theta -= 0.1*(self.theta - self.phi + math.pi)
        elif self.x > screen_width-world_x1:
            self.theta -= 0.1*(self.theta - self.phi + math.pi)
        if self.y < world_y1:
            self.theta -= 0.1*(self.theta - self.phi + math.pi)
        elif self.y > screen_height-world_y1:
            self.theta -= 0.1*(self.theta - self.phi + math.pi)

    def draw(self):
        # Calculate vertices of the triangle
        x1 = self.x + 10 * math.cos(self.theta)
        y1 = self.y + 10 * math.sin(self.theta)
        x2 = self.x + 5 * math.cos(self.theta - (2/3) * math.pi)
        y2 = self.y + 5 * math.sin(self.theta - (2/3) * math.pi)
        x3 = self.x + 5 * math.cos(self.theta + (2/3) * math.pi)
        y3 = self.y + 5 * math.sin(self.theta + (2/3) * math.pi)

        # Draw the triangle
        pygame.draw.polygon(screen, WHITE, [(x1, y1), (x2, y2), (x3, y3)])

               # Draw line from center to boid
        pygame.draw.line(screen, RED, (screen_width // 2, screen_height // 2), (self.x, self.y))

        # Calculate endpoint of line from boid in its direction
        line_length = 20  # Adjust length of line as needed
        end_x = self.x + line_length * math.cos(self.theta)
        end_y = self.y + line_length * math.sin(self.theta)
        
        # Draw line from boid out in its direction
        pygame.draw.line(screen, GREEN, (self.x, self.y), (end_x, end_y))

        # Draw text displaying angle at the center of the screen
        font = pygame.font.Font(None, 36)
        angle_text = font.render(f"Angle: {math.degrees(self.phi):.2f}", True, WHITE)
        angle_text_rect = angle_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(angle_text, angle_text_rect)

                # Draw text displaying angle next to the boid
        font = pygame.font.Font(None, 24)
        angle_text = font.render(f"{(math.degrees(self.theta))%360:.2f}°", True, WHITE)
        angle_text_rect = angle_text.get_rect(center=(self.x + 20, self.y - 20))
        screen.blit(angle_text, angle_text_rect)



# Create initial set of boids
num_boids = 1
boids = [Boid() for _ in range(num_boids)]

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill((0, 0, 0))

    # pygame.draw.rect(screen, WHITE, [(x1, y1), (x2, y2)])
    pygame.draw.rect(screen, WHITE, pygame.Rect(world_x1, world_y1, world_xlen, world_ylen), width=1)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update boid positions
    for boid in boids:
        boid.update()

    # Draw boids
    for boid in boids:
        boid.draw()

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
