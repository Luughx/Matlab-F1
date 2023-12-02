import pygame as py
from components.functions import draw_text
import re 

class TextInput():
    def __init__(self, x=0, y=0, width=120, height=30, label="", units=""):
        self.input = py.Surface((width, height))
        self.input.set_alpha(128)

        self.input.fill((0, 0, 0))

        self.input.fill((0, 0, 0)) #165
        self.inputRect = py.Rect(x, y, width, height)
        self.active = False
        self.userText = ""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.units = units

        self.time = py.time.get_ticks()

    def events(self, event):
        if event.type == py.MOUSEBUTTONDOWN: 
            if self.inputRect.collidepoint(event.pos): 
                self.active = True
            else: 
                self.active = False

        if event.type == py.KEYDOWN and self.active:

            self.time = py.time.get_ticks()
            self.userText = self.userText.replace("|", "")

            if event.key == py.K_BACKSPACE: 
                self.userText = self.userText[:-1] 
            elif len(self.userText) <= 10 and re.match(r'^[0-9.-]+$', event.unicode): 
                self.userText += event.unicode.lower()

    def main(self, surface):

        if py.time.get_ticks() - self.time > 950 and self.active:
            self.userText += "|"
            self.time = py.time.get_ticks()
        
        if py.time.get_ticks() - self.time > 500:
            self.userText = self.userText.replace("|", "")

        draw_text(self.label, py.font.Font("assets/Pixellari.ttf", 20), (0, 0, 0), surface, self.x, self.y-27)
        surface.blit(self.input, (self.x, self.y))
        textSurface = py.font.Font("assets/Pixellari.ttf", 20).render(self.userText, True, (255, 255, 255))
        surface.blit(textSurface, (self.x+8, self.y+12))
        draw_text(self.units, py.font.Font("assets/Pixellari.ttf", 20), (0, 0, 0), surface, self.x+self.width+10, self.y+10)

    def set_text(self, value):
        self.userText = f"{value:.2f}"

    def get_text(self):
        return self.userText.strip().replace("|", "")
    
    def clear_text(self):
        self.userText = ""