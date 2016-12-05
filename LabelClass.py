import pygame
from pygame.locals import *

class Label:
    def __init__(self, surface, centerx, centery,
          fontsize, caption, forecolor, backcolor):
        self.screen = surface
        self.forecolor = forecolor
        self.backcolor = backcolor
        self.font = pygame.font.SysFont(None,fontsize)
        self.centerx = centerx
        self.centery = centery
        self.caption = caption
        self.visible = False # tells if the label is visible

    def draw(self):
        self.text = self.font.render(self.caption,
            True, self.forecolor, self.backcolor)
        self.rect = self.text.get_rect()
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
        self.screen.blit(self.text, self.rect)
        pygame.display.update([self.rect])
        self.visible = True

    def undraw(self):
        self.text.fill(self.backcolor)
        self.screen.blit(self.text,self.rect)
        pygame.display.update([self.rect])
        self.visible = False
