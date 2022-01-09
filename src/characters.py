
import pygame
from os import getcwd


class Character:
    def __init__(self, screen, position, character) -> None:
        self.screen = screen
        self.position = position

        self.character = character
        self.character_surface = pygame.image.load(f'{getcwd()}/static/images/{character}.png')

    def change_position(self, position):
        self.position = position
    
    def render(self):
        self.screen.blit(self.character_surface, self.position)

    def type(self):
        return self.character
