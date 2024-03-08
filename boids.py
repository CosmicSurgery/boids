import pygame
import random
import sys
from tkinter import Tk, Scale, Button
import math

# Define Boid class
class Boid:
    def __init__(self):
        self.x = random.randint(world_x1, world_x1+world_xlen)
        self.y = random.randint(world_y1, world_y1+world_ylen)
        self.vx = random.randint(MIN_SPEED,MAX_SPEED)*[-1,1][random.randint(0,1)]
        self.vy = random.randint(MIN_SPEED,MAX_SPEED)*[-1,1][random.randint(0,1)]
        self.theta = math.atan2(self.vy, self.vx)
        self.biasval = 0.001

        self.scout_group = random.random()
        if self.scout_group >=0.95:
            self.scout_group = 1
        elif self.scout_group <=0.5:
            self.scout_group = 2
        else:
            self.scout_group = 0

    def update(self):
        speed = math.sqrt(self.vx*self.vx + self.vy*self.vy)
        if self.scout_group == 1:
            self.vx = (1 - self.biasval)*self.vx + (self.biasval * 1)
        elif self.scout_group == 2:
            self.vx = (1 - self.biasval)*self.vx + (self.biasval * -1)

        self.x += self.vx
        self.y += self.vy
        self.theta = math.atan2(self.vy, self.vx)
        
        # Wrap around screen edges
        if self.x < world_x1:
            self.vx += turnfactor
        elif self.x > screen_width-world_x1:
            self.vx -= turnfactor
        if self.y < world_y1:
            self.vy += turnfactor
        elif self.y > screen_height-world_y1:
            self.vy -= turnfactor

        if speed>MAX_SPEED:
            self.vx = (self.vx/speed)*MAX_SPEED
            self.vy = (self.vy/speed)*MAX_SPEED
        elif speed<MIN_SPEED:
            self.vx = (self.vx/speed)*MIN_SPEED
            self.vy = (self.vy/speed)*MIN_SPEED

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
        # pygame.draw.circle(screen, GREEN, [self.x, self.y], VISIBLE_RANGE, 1)
        # pygame.draw.circle(screen, RED, [self.x, self.y], PROTECTED_RANGE, 1)

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the screen
    global screen_height
    global screen_width
    global screen

    screen_width, screen_height = 1600, 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Boids Simulation")

    # Define colors
    global WHITE
    global RED
    global GREEN

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    # World limits
    global world_x1
    global world_xlen
    global world_y1
    global world_ylen


    world_x1,world_xlen = screen_width/10, screen_width - 2*(screen_width/10)
    world_y1,world_ylen = screen_height/10, screen_height - 2*(screen_height/10)

    world_x1 = int(world_x1)
    world_y1 = int(world_y1)
    world_xlen = int(world_xlen)
    world_ylen = int(world_ylen)
    # Seperation

    # Dynamic constraints
    global MAX_SPEED
    global MIN_SPEED
    global PROTECTED_RANGE
    global VISIBLE_RANGE
    global MAX_BIAS
    
    global turnfactor
    global avoidfactor
    global matchingfactor
    global centeringfactor
    global bias_increment


    MAX_SPEED = 6
    MIN_SPEED = 3
    PROTECTED_RANGE = 8
    VISIBLE_RANGE = 40
    MAX_BIAS = 0.01

    turnfactor = 0.2
    avoidfactor = 0.03
    matchingfactor = 0.03
    centeringfactor = 0.005 
    bias_increment = 0.00004

    # Create initial set of boids
    num_boids = 50
    boids = [Boid() for _ in range(num_boids)]


    # Main loop
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((0, 0, 0))

        pygame.draw.rect(screen, WHITE, pygame.Rect(world_x1, world_y1, world_xlen, world_ylen), width=1)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update boid positions
        for boid1 in boids:
            close_dx, close_dy = 0, 0
            xvel_avg, yvel_avg, neighboring_boids = 0, 0, 0
            xpos_avg, ypos_avg = 0,0 

            for boid2 in boids:
                if boid1 != boid2:
                    if math.dist([boid1.x,boid1.y],[boid2.x,boid2.y]) <= PROTECTED_RANGE:
                        close_dx += boid1.x - boid2.x
                        close_dy += boid1.y - boid2.y
                    if math.dist([boid1.x,boid1.y],[boid2.x,boid2.y]) <= VISIBLE_RANGE:
                        xvel_avg += boid2.vx
                        yvel_avg += boid2.vy
                        xpos_avg += boid2.x
                        ypos_avg += boid2.y
                        neighboring_boids += 1
                    
            if neighboring_boids > 0:
                xvel_avg = xvel_avg/neighboring_boids
                yvel_avg = yvel_avg/neighboring_boids
                xpos_avg = xpos_avg/neighboring_boids
                ypos_avg = ypos_avg/neighboring_boids
                boid1.vx += (xpos_avg - boid1.x)*centeringfactor
                boid1.vy += (ypos_avg - boid1.y)*centeringfactor    
                boid1.vx += (xvel_avg - boid1.vx)*matchingfactor
                boid1.vy += (yvel_avg - boid1.vy)*matchingfactor       

            boid1.vx += close_dx*avoidfactor
            boid1.vy += close_dy*avoidfactor
            boid1.update()
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


if __name__ == '__main__':
    main()