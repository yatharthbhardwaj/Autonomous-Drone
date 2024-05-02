import pygame

def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))

def getKey(keyName):
    asw = False
    for eve in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame,'K_{}'.format(keyName))
    if keyInput[myKey]:
        asw = True
    pygame.display.update()
    return asw

def main():
    if getKey("LEFT"):
        print("Left Key Pressed")
    if getKey("RIGHT"):
        print("Right Key Pressed")

if __name__ == '__main__':
    init()
    while True:
        main()