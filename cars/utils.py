import pygame 

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle): # per ruotare la macchina
    rotated_image = pygame.transform.rotate(image, angle) # mi crea la ruotata
    new_rectangle = rotated_image.get_rect(center = image.get_rect(topleft = top_left).center) # tiene il centro fermo
    win.blit(rotated_image, new_rectangle.topleft)