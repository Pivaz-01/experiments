import math
import random

def addVector(vec1, vec2): # mi trova vettore differenza
    angle1, length1 = vec1
    angle2, length2 = vec2

    x = math.sin(angle1) * length1 + math.sin(angle2) * length2 
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2  

    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y ,x)

    return (angle, length)

def combine(p1, p2):
    if math.hypot(p1.x - p2.x, p1.y - p2.y) < p1.size + p2.size:
        total_mass = p1.mass + p2.mass
        p1.x = (p1.x * p1.mass + p2.x * p2.mass) / total_mass
        p1.y = (p1.y * p1.mass + p2.y * p2.mass) / total_mass

        (p1.angle, p1.vel) = addVector((p1.angle, p1.vel * p1.mass / total_mass), 
            (p2.angle, p2.vel * p2.mass / total_mass))
        
        p1.vel *= (p1.elasticity * p2.elasticity)
        p1.mass += p2.mass
        p1.collide_with = p2

def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    distance = math.hypot(dx, dy)

    if distance <= p1.size + p2.size: 
        angle = math.atan2(dy, dx) + 0.5 * math.pi 
        total_mass = p1.mass + p2.mass
        
        # NOTA 3
        (p1.angle, p1.vel) = addVector((p1.angle, p1.vel*(p1.mass-p2.mass)/total_mass), 
            (angle, 2*p2.vel*p2.mass/total_mass))
        (p2.angle, p2.vel) = addVector((p2.angle, p2.vel*(p2.mass-p1.mass)/total_mass), 
            (angle+math.pi, 2*p1.vel*p1.mass/total_mass))
        
        elasticity = p1.elasticity * p2.elasticity
        p1.vel *= elasticity
        p2.vel *= elasticity

        overlap = 0.5 * (p1.size + p2.size - distance + 1)
        
        p1.x += math.sin(angle) * overlap
        p1.y -= math.cos(angle) * overlap
        p2.x -= math.sin(angle) * overlap
        p2.y += math.cos(angle) * overlap

def printMeanV(particles):
    sum_v = 0
    n = 0
    for p in particles:
        sum_v += p.vel
        n += 1
    
    mean_v = sum_v / n
    return mean_v

class Particle:
    def __init__(self, pos, size, mass = 1):
        self.x, self.y = pos
        self.size = size
        self.color = (0,0,255)
        self.mass = mass

        self.vel = 0.
        self.angle = 0.

        self.drag = 1.
        self.elasticity = 1.

    def move(self):
        self.x += self.vel * math.sin(self.angle)
        self.y -= self.vel * math.cos(self.angle)

    def experienceDrag(self):
        self.vel *= self.drag
    
    def accelerate(self, vec):
        (self.angle, self.vel) = addVector((self.angle, self.vel), vec)
    
    def attraction(self, other):
        dx = (self.x - other.x)
        dy = (self.y - other.y)
        dist = math.hypot(dx, dy)
        
        if dist < self.size + other.size:
            return True
        
        theta = math.atan2(dy, dx)
        force = .2 * self.mass * other.mass / dist**2
        self.accelerate((theta - 0.5*math.pi, force/self.mass))
        other.accelerate((theta + 0.5*math.pi, force/other.mass))        

    def mouseMove(self, x, y):
        dx = x - self.x
        dy = y - self.y
        
        self.angle = 0.5*math.pi + math.atan2(dy, dx)
        self.vel = math.hypot(dx, dy) * 0.1

class Environment:
    def __init__(self, dim):
        self.width, self.height = dim
        self.particles = []

        self.color = (255,255,255)
        self.mass_air = 0.
        self.elasticity = 1.
        self.acceleration = (0,-.1)

        self.particle_functions1 = [] 
        self.particle_functions2 = [] 
        self.function_dict = { # NOTA 4
            'move': (1, lambda p: p.move()),
            'drag': (1, lambda p: p.experienceDrag()),
            'bounce': (1, lambda p: self.bounce(p)),
            'accelerate': (1, lambda p: p.accelerate(self.acceleration)),
            'collide': (2, lambda p1, p2: collide(p1, p2)),
            'combine': (2, lambda p1, p2: combine(p1, p2)),
            'attraction': (2, lambda p1, p2: p1.attraction(p2))
        }

    def addFunction(self, function_list):
        for func in function_list:
            (n, f) = self.function_dict.get(func, (-1, None))
            if n == 1:
                self.particle_functions1.append(f)
            elif n == 2:
                self.particle_functions2.append(f)
            else:
                print("No such function: %s" % f)

    def addParticle(self, n = 1, **kargs):
        for i in range(n):
            size = kargs.get('size', random.randint(10,20))
            mass = kargs.get('mass', random.randint(100,10000))
            x = kargs.get('x', random.uniform(size, self.width - size))
            y = kargs.get('y', random.uniform(size, self.height - size))

            particle = Particle((x, y), size, mass)
                             
            particle.vel = kargs.get('vel', 2* random.random()) 
            particle.angle = kargs.get('angle', random.uniform(0, 2 * math.pi))
            particle.color = kargs.get('color', (0,0,255))
            particle.drag = (particle.mass / (particle.mass + self.mass_air)) ** particle.size

            self.particles.append(particle)

    def update(self):
        for i, particle in enumerate(self.particles):
            for f in self.particle_functions1:
                f(particle)
            for particle2 in self.particles[i+1:]:
                for f in self.particle_functions2:
                    f(particle, particle2)
        print(printMeanV(self.particles))
    
    def bounce(self, particle):
        if particle.x >= self.width - particle.size:
            particle.x = 2 * (self.width - particle.size) - particle.x
            particle.angle = - particle.angle
            particle.vel *= self.elasticity
        elif particle.x <= particle.size:
            particle.x = 2 * particle.size - particle.x
            particle.angle = - particle.angle
            particle.vel *= self.elasticity
        
        if particle.y >= self.height - particle.size:
            particle.y = 2 * (self.height - particle.size) - particle.y
            particle.angle = math.pi - particle.angle
            particle.vel *= self.elasticity
        elif particle.y <= particle.size:
            particle.y = 2 * particle.size - particle.y
            particle.angle = math.pi - particle.angle
            particle.vel *= self.elasticity

    def findParticle(self, x, y):
        for particle in self.particles:
            if math.hypot(particle.x - x, particle.y - y) <= particle.size: 
                return particle
        return None

# NOTA 3: Quello seguente è un algoritmo trovato su internet che dovrebbe rappresentare 
# al meglio la collisione con rimbalzo fra due corpi. Probabilmente a causa di
# processore del pc e grafica pygame, penso possa essere migliorabile.

# NOTA 4: Queste sono le funzioni che si possono aggiungere al main tramite adFunction. 

# NOTA 5: Trattando le masse come cariche e invertendo il segno della forza nella 
# funzione di attrazione, si può ottenere il fenomeno di attrazione/repulsione EM, 
# più adatto per fisica della Materia