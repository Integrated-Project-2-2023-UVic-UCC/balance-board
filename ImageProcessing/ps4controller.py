import pygame

pygame.init()
j = pygame.joystick.Joystick(0)

j.init()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.JOYBUTTONDOWN:
            print("Button pressed ", event.value)
