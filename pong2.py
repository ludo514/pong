import pygame
from random import *

global POINT
POINT = 0

class Player(pygame.sprite.Sprite):

    # sprite pour le Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (LARGEUR / 2, HAUTEUR - 30)

    def update(self):

        self.speed = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speed = - 10
        if keystate[pygame.K_RIGHT]:
            self.speed = 10

        self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > LARGEUR:
            self.rect.right = LARGEUR


class Balle(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 15))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (LARGEUR / 2, HAUTEUR / 2)
        self.dy = 5
        self.dx = 5
        self.hit = False

    def update(self):

        self.rect.x += self.dx #on fait avancez la balle en diagonale
        self.rect.y += self.dy
        # self.rect.move_ip((self.dx, self.dy))

        #vérification de collision avec les bords de la fenêtre
        if self.rect.collidepoint((self.rect.x, 480)):
            #self.dy = - self.dy
            self.rect.center = (LARGEUR / 2, HAUTEUR / 2) 
        if self.rect.collidepoint((640, self.rect.y)):
            self.dx = - self.dx
        if self.rect.collidepoint((self.rect.x, 0)):
            self.dy = - self.dy
        if self.rect.collidepoint((0, self.rect.y)):
            self.dx = - self.dx
        #véréfication si il y à collisition avec la raquette (player)
        if self.rect.colliderect(player.rect):
            self.hit = True
            if self.hit:
                self.dy = - self.dy


class Bricks(pygame.Rect):

    def __init__(self, x, y, width, height):
        pygame.Rect.__init__(self, x, y, width, height)


class Mur(pygame.sprite.Sprite):

    def __init__(self, aire):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.mur = []
        self.position_initialex = 120
        self.position_initialey = 120
        self.x = self.position_initialex
        self.y = self.position_initialey
        self.ligne = 6
        self.colonne = 15
        self.aire = aire
        self.brique = 0
        self.hit = False

        for i in range(self.ligne):#double boucle pour crée une brique dans la class mur
            for j in range(self.colonne):
                self.brique = Bricks(self.x, self.y, 25, 15)
                self.mur.append(self.brique)
                self.x = self.x + 27
            self.y = self.y + 20
            self.x = self.position_initialex


    def update(self):

        for i in self.mur:
            if balle.rect.colliderect(i):
                self.hit = True
                if self.hit:
                    self.mur.remove(i)
                    balle.dy = - balle.dy
                    return True

    def draw(self):
        for i in self.mur:
            pygame.draw.rect(self.aire, WHITE, i)

if __name__ == '__main__':

    LARGEUR = 640
    HAUTEUR = 480
    FPS = 60

    # couleur
    WHITE = (255, 255, 255)
    NOIR = (0, 0, 0)

    # initialisation de pygame et création de la fenêtre
    pygame.init()
    screen = pygame.display.set_mode((LARGEUR, HAUTEUR))

    pygame.display.set_caption("Pong")#nom de la fenêtre
    clock = pygame.time.Clock()
    police = pygame.font.SysFont("comicsansms", 30, 1)

    # création des objets
    global player
    global balle
    player = Player()
    balle = Balle()
    mur = Mur(screen)
    # ajout des sprite à la liste

    all_sprtites = pygame.sprite.Group()

    all_sprtites.add(player)
    all_sprtites.add(balle)

    # Boucle de jeu
    launched = True
    while launched:
        # vitesse de boucle (FPS)
        clock.tick(FPS)
        # récupération d'un event

        for event in pygame.event.get():
            #
            if event.type == pygame.QUIT:
                launched = False

        # Update

        all_sprtites.update()
        if mur.update():
            POINT += 5

        # Draw / rendue

        screen.fill(NOIR)
        all_sprtites.draw(screen)#affiche tous les sprites qui font partie du groupe
        mur.draw()
        point_text = police.render("{}".format(POINT), True, WHITE)
        screen.blit(point_text, [10,10])

        # après avoir tout déssiner

        pygame.display.flip()

pygame.quit()
