import pygame
import math 

pygame.init()

AU = 1.496e8 * 1000 # astronomical unit (m)
G = 6.67428e-11
SCALE = 50000000 / AU 
TIMESTEP = 0.01 # 1 sec

YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 49, 50)

WIDTH, HEIGHT = 800, 600 #dimensioni grafico
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #set display
pygame.display.set_caption("Moon simulation") #set titolo

class Body:
    def __init__(self, x, y, mass, color):
        self.x = x
        self.y = y
        self.mass = mass
        self.color = color

        self.x_vel = 0
        self.y_vel = 0

        self.orbit = []

    def draw(self, WIN):
        x = self.x * SCALE + WIDTH / 2 #parto dal centro
        y = self.y * SCALE + WIDTH / 2
        
        if len(self.orbit) > 2:
            new = []
            for point in self.orbit:
                x, y = point
                x = x * SCALE + WIDTH / 2
                y = y * SCALE + HEIGHT / 2

                new.append((x, y))

            pygame.draw.lines(WIN, self.color, False, new, 1) 

        pygame.draw.circle(WIN, self.color, (x, y), 5)

    def attraction(self, other):
        distance_x = other.x - self.x 
        distance_y = other.y - self.y
        distance = math.sqrt((distance_x ** 2) + (distance_y ** 2))
        theta = math.atan2(distance_y, distance_x)

        f = G * self.mass * other.mass / (distance ** 2)

        f_x = math.cos(theta) * f
        f_y = math.sin(theta) * f

        return f_x, f_y

    def move(self, bodies):
        fx = fy = 0
        for body in bodies:
            if body == self:
                continue
            
            f_x, f_y = self.attraction(body)
            fx += f_x
            fy += f_y
        
        self.x_vel += (fx / self.mass) * TIMESTEP
        self.y_vel += (fy / self.mass) * TIMESTEP
        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP
        
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    earth = Body(0, 0, 5.972 * (10**24), BLUE)
    # moon = Body(-2.5 * (10 ** -3) * AU, 0, 7.348 * (10**22), RED)
    # moon.y_vel = 1022 # m/s 
    iss = Body(-408000, 0, 419725, YELLOW)
    iss.y_vel = 7660  # m/s

    bodies = [earth, iss]

    while run: 
        clock.tick(1000)  
        WIN.fill((0,0,0)) #riempio di nero, mi copre le posizioni precedenti ogni volta 

        for event in pygame.event.get(): #controllo tutti gli eventi e se c'è quit esco
            if event.type == pygame.QUIT: 
                run = False  
        
        for body in bodies:
            body.move(bodies)
            body.draw(WIN)
        
        pygame.display.update() #aggiorno il display

    pygame.quit()

main()