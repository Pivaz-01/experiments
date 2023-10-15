import random
import pygame
import utilities as ut

class universeScreen:
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
        self.mx = (1 - self.magnification) * self.width/2
        self.my = (1 - self.magnification) * self.height/2
    
    def reset(self):
        (self.dx, self.dy) = (0,0)
        (self.mx, self.my) = (0,0)
        self.magnification = 1.

def calculateRadius(mass):
    return 0.4 * mass**0.5

# creo ambiente
(WIDTH, HEIGHT) = (800, 600)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particles simulation")

universe = ut.Environment((WIDTH,HEIGHT))
universe.color = (0,0,0)
universe.addFunction(['move','attraction','combine']) # NOTA 1
universe_screen = universeScreen(WIDTH, HEIGHT)

for p in range(100):
    particle_mass = random.randint(10,40)
    particle_size = calculateRadius(particle_mass)
    universe.addParticle(mass = particle_mass, size = particle_size, color = (255,255,255))

# NOTA 2
key_to_function = { 
    pygame.K_a: (lambda x: x.scroll(dx = 1)),
    pygame.K_d: (lambda x: x.scroll(dx = -1)),
    pygame.K_s: (lambda x: x.scroll(dy = -1)),
    pygame.K_w: (lambda x: x.scroll(dy = 1)),
    pygame.K_UP: (lambda x: x.zoom(1.5)),
    pygame.K_DOWN: (lambda x: x.zoom(0.75)),
    pygame.K_r: (lambda x: x.reset())
}

run = True
paused = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False    
        if event.type == pygame.KEYDOWN:
            if event.key in key_to_function:
                key_to_function[event.key](universe_screen)
            elif event.key == pygame.K_SPACE:
                paused = not paused
        
    if not paused:
        universe.update()
        
    WIN.fill(universe.color)

    particles_to_remove = []
    for p in universe.particles:
        if 'collide_with' in p.__dict__:
            particles_to_remove.append(p.collide_with)
            p.size = calculateRadius(p.mass)
            del p.__dict__['collide_with']
        
        mag = universe_screen.magnification
        x = int(universe_screen.mx + (p.x + universe_screen.dx) * mag)
        y = int(universe_screen.my + (p.y + universe_screen.dy) * mag)
        size = int(p.size * mag)
        
        if p.size < 2:
            pygame.draw.rect(WIN, p.color, (x, y, 2, 2)) # 2x2
        else:
            pygame.draw.circle(WIN, p.color, (x, y), p.size, 0) # spessore = 0

    for p in particles_to_remove:
        if p in universe.particles:
            universe.particles.remove(p)

    pygame.display.flip()        

pygame.quit()

# NOTA 1: Qui è possibile inserire a proprio piacimento le funzioni presenti nel 
# function_dict della classe Enviroment (utilities.py), per meglio adattare l'ambiente al
# tipo di simulazione ricercata.

# NOTA 2: Possibili comandi di visualizzazione AD-SW per traslazione, 
# frecia in su e giù per zoom. R per reset.