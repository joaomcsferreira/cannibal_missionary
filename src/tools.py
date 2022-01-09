import pygame
from os import getcwd

def button(size, msg, x, y, w, h, rect, action, screen):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + w and y < mouse[1] < y + h:
            button_config(size, msg, x, y, w, h, rect, screen, color=(255, 255, 255))
            if click[0] == 1 and action == 'play':
                return True
            elif click[0] == 1 and action == 'exit':
                exit()
        else:
            button_config(size, msg, x, y, w, h, rect, screen, color=(169, 169, 169))

def button_config(size, msg, x, y, w, h, rect, screen, color=(169, 169, 169)):
    """Render the message"""
    txt = pygame.font.Font(f'{getcwd()}/static/font/PressStart2P-Regular.ttf', size)

    if rect:
        pygame.draw.rect(screen, color, [x, y, w, h])
        txt_surf = txt.render(msg, True, (0, 0, 0))
    else:
        txt_surf = txt.render(msg, True, (255, 255, 255))
    txt_rect = txt_surf.get_rect()
    txt_rect.center = ((x + int(w / 2)), (y + int(h / 2)))

    screen.blit(txt_surf, txt_rect)
