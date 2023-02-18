import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600 #dimensioni grafico
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #set display
pygame.display.set_caption("Planet simulation") #set titolo

WHITE = (255,255,255) #colore rgb
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 49, 50)
GREY = (80, 78, 81)
GREEN = (124,252,0)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = 149.6e6 * 1000 # astronomical unit
    G = 6.67428e-11
    SCALE = 150 / AU 
    TIMESTEP = 3600 * 24 # 1 ora
    
    def __init__(self, x, y, radius, color, mass): # elementi inizializzazione 
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.sun = False #non è sole
        self.distance_to_sun = 0
        self.orbit = []

        self.x_vel = 0 
        self.y_vel = 0

    def draw(self, WIN):
        x = self.x * self.SCALE + WIDTH / 2 #metto al centro 
        y = self.y * self.SCALE + HEIGHT / 2
        
        if len(self.orbit) > 2: # deve avere almeno 2 punti
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2

                updated_points.append((x,y))

            pygame.draw.lines(WIN, self.color, False, updated_points, 2) 
                # False: non ha una fine
                # 2 è spessore

        pygame.draw.circle(WIN, self.color, (x, y), self.radius) # disegna
        
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            WIN.blit(distance_text, (x - distance_text.get_width()/2, y + distance_text.get_height()/2))

    def attraction(self, other_planet):
        other_x, other_y = other_planet.x, other_planet.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y 
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other_planet.sun:
            self.distance_to_sun = distance
        force = self.G * self.mass * other_planet.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)

        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet: 
                continue # skip self

            fx, fy = self.attraction(planet)
            
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.mass * self.TIMESTEP # v = a * t
        self.y_vel += total_fy / self.mass * self.TIMESTEP 

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 2, YELLOW, 1.98892 * 10**30) # 30 sono px
    sun.sun = True
    earth = Planet(-1 * Planet.AU, 0, 5, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000
    mars = Planet(-1.54 * Planet.AU, 0, 5, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000
    mercury = Planet(-0.387 * Planet.AU, 0, 5, GREEN, 3.3 * 10**23)
    mercury.y_vel = 47.4 * 1000
    venus = Planet(-0.723 * Planet.AU, 0, 5, WHITE, 4.8685 * 10**24)
    venus.y_vel = 35.02 * 1000
    moon = Planet((-1 - 3.84e8 / Planet.AU) * Planet.AU, 0, 5, GREY, 7.3477 * 10**22)
    moon.y_vel = earth.y_vel + 1.022 * 1000 

    planets = [sun, earth, mars, mercury, venus, moon]

    while run: 
        clock.tick(300) #ripeto 300 volte ogni secondo 
        WIN.fill((0,0,0)) #riempio di nero, mi copre le posizioni precedenti ogni volta 

        for event in pygame.event.get(): #controllo tutti gli eventi e se c'è quit esco
            if event.type == pygame.QUIT: 
                run = False  

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        
        pygame.display.update() #aggiorno il display

    pygame.quit()

main()