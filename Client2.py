import pygame
from Network import Network

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 1

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.rect = (self.x, self.y, self.width, self.height)

def redrawWindow(win, player, opp_pos):
    win.fill((255, 255, 255))
    player.draw(win)

    # Draw opponents
    if opp_pos != " ":
        filtered_pos = "".join(filter(lambda c: c not in ['(', "'", ',', ')'], opp_pos))
        opp_pos_list = filtered_pos.split()
        opp_x = int(opp_pos_list[0])
        opp_y = int(opp_pos_list[1])

        rect = (opp_x, opp_y, 50, 50)
        pygame.draw.rect(win, (150, 0, 50), rect)

    pygame.display.update()


def main():
    run = True
    n = Network()

    print('My id is ', n.id)
    print('My color is ', n.color)

    p = Player(30, 30, 50, 50, n.color)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        opp_pos = n.send_pos(p.x, p.y)
        print('Received ', opp_pos)
        p.move()
        redrawWindow(win, p, opp_pos)

main()