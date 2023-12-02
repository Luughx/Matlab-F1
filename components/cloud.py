import random
import pygame as py
import os

class Cloud():
    def __init__(self):
        self.images = []        
        with os.scandir(os.path.join("assets", "clouds")) as files:
            for file in files:
                self.images.append(file.name)

        self.get_values()
    
    def move(self, surface, dt):
        if self.right:
            self.x += self.velocity * dt
            if self.x > surface.get_width():
                self.get_values()
            else:   
                surface.blit(self.image, (self.x, self.y))
        else:
            self.x -= self.velocity * dt
            if self.x < 0 - self.image.get_width():
                self.get_values()
            else:   
                surface.blit(self.image, (self.x, self.y))

    def get_values(self):
        self.velocity = random.uniform(0.6, 2.3)
        imageRaw = py.image.load(os.path.join("assets/clouds", self.images[random.randrange(0, len(self.images))]))
        imageRaw.set_alpha(random.uniform(20, 70))
        #rand = random.uniform(100, 170)
        randRight = random.randrange(1, 3, 1)
        self.right = True
        
        if randRight == 1: 
            self.right = True
        else: 
            self.right = False

        width = imageRaw.get_width() * 1.5
        height = imageRaw.get_height() * 1.5
        self.image = py.transform.scale(imageRaw, (width, height))
        if self.right:
            self.x = 0 - width - random.uniform(100, 500)
        else:
            self.x = 1280 + width + random.uniform(100, 500)

        self.y = random.uniform(80, 550)