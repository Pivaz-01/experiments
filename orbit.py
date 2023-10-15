import pygame
import math 
import numpy as np

pygame.init()

AU = 1.496e8 * 1000 # astronomical unit (m)
G = 6.67428e-11
SCALE = 50000000 / AU # m/AU 
TIMESTEP = 2 # 1 = 100 sec -> per luna usa 1000, per iss 0.01
SUBSTEPS = 100 

YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 49, 50)
GREEN = (0,128,0)

WIDTH, HEIGHT = 900, 600 #dimensioni grafico
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #set display
pygame.display.set_caption("Orbits simulation") #set titolo

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.dx, self.dy = 0, 0
        self.mx, self.my = 0, 0
        self.magnification = 1.

    def scroll(self, dx = 0, dy = 0):
        self.dx += dx * self.width / (self.magnification * 10)
        self.dy += dy * self.height / (self.magnification * 10)

    def zoom(self, zoom):
        self.magnification *= zoom
        self.dx = (1 - zoom) * self.width / 2 + zoom * self.dx
        self.dy = (1 - zoom) * self.height / 2 + zoom * self.dy
        global SCALE
        SCALE *= zoom
    
    def reset(self):
        (self.dx, self.dy) = (0,0)
        (self.mx, self.my) = (0,0)
        self.magnification = 1.

class Body:
    def __init__(self, x, y, mass, color):
        self.x = x
        self.y = y
        self.mass = mass
        self.color = color

        self.x_vel = 0
        self.y_vel = 0

        self.orbit = []
        self.max_orbit_points = 1000

    def interpolate_orbit(self): # devo capirla 
        x_values, y_values = zip(*self.orbit)
        t_values = np.linspace(0, 1, self.max_orbit_points)
        
        interpolated_x = np.interp(t_values, np.linspace(0, 1, len(self.orbit)), x_values)
        interpolated_y = np.interp(t_values, np.linspace(0, 1, len(self.orbit)), y_values)
        
        interpolated_orbit = [(x * SCALE + WIDTH / 2, y * SCALE + HEIGHT / 2) for x, y in zip(interpolated_x, interpolated_y)]
        
        return interpolated_orbit

    def draw(self, WIN, screen):
        if len(self.orbit) > 2:
            if len(self.orbit) > self.max_orbit_points:
                interpolated_orbit = self.interpolate_orbit()
                pygame.draw.lines(WIN, self.color, False, interpolated_orbit, 1)
            else:
                orbit_points = [((point[0] - screen.dx) * screen.magnification * SCALE + screen.mx + WIDTH / 2, (point[1] - screen.dy) * screen.magnification * SCALE + screen.my + HEIGHT / 2) for point in self.orbit]
                pygame.draw.lines(WIN, self.color, False, orbit_points, 1)

        pygame.draw.circle(WIN, self.color, ((self.x - screen.dx) * screen.magnification * SCALE + screen.mx + WIDTH / 2, (self.y - screen.dy) * screen.magnification * SCALE + screen.my + HEIGHT / 2), 3)

    def attraction(self, other):
        distance_x = other.x - self.x 
        distance_y = other.y - self.y
        distance_squared = (distance_x ** 2) + (distance_y ** 2)
        theta = math.atan2(distance_y, distance_x)

        f = G * self.mass * other.mass / (distance_squared)

        f_x = math.cos(theta) * f
        f_y = math.sin(theta) * f

        return f_x, f_y

    def move(self, bodies):
        for _ in range(SUBSTEPS):
            fx = fy = 0
            for body in bodies:
                if body == self:
                    continue
                
                else:
                    f_x, f_y = self.attraction(body)
                    fx += f_x
                    fy += f_y

            self.x_vel += (fx / self.mass) * TIMESTEP / SUBSTEPS
            self.y_vel += (fy / self.mass) * TIMESTEP / SUBSTEPS
            self.x += self.x_vel * TIMESTEP / SUBSTEPS
            self.y += self.y_vel * TIMESTEP / SUBSTEPS

            if len(self.orbit) >= self.max_orbit_points:
                self.orbit.pop(0)  # Rimuovi il punto più vecchio

            self.orbit.append((self.x, self.y))

def main():
    universe_screen = Screen(WIDTH, HEIGHT)
    
    key_to_function = { 
        pygame.K_a: (lambda x: x.scroll(dx = -1e3)),
        pygame.K_d: (lambda x: x.scroll(dx = 1e3)),
        pygame.K_s: (lambda x: x.scroll(dy = 1e3)),
        pygame.K_w: (lambda x: x.scroll(dy = -1e3)),
        pygame.K_UP: (lambda x: x.zoom(1.2)),
        pygame.K_DOWN: (lambda x: x.zoom(0.8)),
        pygame.K_r: (lambda x: x.reset())
    }
    
    run = True
    paused = False

    clock = pygame.time.Clock()

    earth = Body(0, 0, 5.972e24, BLUE)

    sun = Body(150e9, 0, 2e30, YELLOW)
    sun.y_vel = 3e4
    
    moon = Body(0, 384.4e6, 7.348e22, RED)
    moon.x_vel = 1.022e3
    
    iss = Body(-408000, 0, 419725, YELLOW)
    iss.y_vel = 7.660e3

    tiangong = Body(400000, 0, 66000, GREEN)
    tiangong.y_vel = -7.68e3

    bodies = [earth, moon]

    while run: 
        clock.tick(1000) # FPS  
        WIN.fill((0,0,0)) #riempio di nero, mi copre le posizioni precedenti ogni volta 

        for event in pygame.event.get(): #controllo tutti gli eventi e se c'è quit esco
            if event.type == pygame.QUIT: 
                run = False  

            if event.type == pygame.KEYDOWN:
                    key = event.key
                    if key in key_to_function:
                        key_to_function[key](universe_screen)
                    if event.key == pygame.K_SPACE:
                        paused = not paused
        for _ in range(SUBSTEPS):
            for body in bodies:
                if not paused:
                    body.move(bodies)

        for body in bodies:
            body.draw(WIN, universe_screen)

        pygame.display.update() #aggiorno il display

    pygame.quit()

main()