import pygame
pygame.init()
win = pygame.display.set_mode((1000, 500))#horizontal vertical

# Program name
pygame.display.set_caption("Chapri Game")
scr_width=1000
scr_height=500

x = 500 #x,y is the character position
y = 250
width = 40
height = 60
vel = 10

run = True
while run:
    pygame.time.delay(100)  # milliseconds

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Continuous key press detection
    keys = pygame.key.get_pressed()

    # Coordinates are from the top left
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
    if keys[pygame.K_RIGHT]and x < (scr_width-width-vel):# note character is also seen from top left so only screen length can cause it to be off screen
        x += vel
    if keys[pygame.K_UP]and y > vel:
        y -= vel
    if keys[pygame.K_DOWN]and y < (scr_height-height-vel) :#so character height and length are also subed,-vel for not touching the border
        y += vel

    # Update window
    win.fill((0, 0, 0))  # Fills black background to erase past positions
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))  # Draws the rectangle
    pygame.display.update()  # Update display

pygame.quit()


  