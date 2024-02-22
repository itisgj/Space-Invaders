from ast import keyword
from turtle import Screen, screensize
from webbrowser import BackgroundBrowser
from matplotlib.pyplot import text
import pygame
from sqlalchemy import false
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800,600))

background = pygame.image.load('finale.jpg')

mixer.music.load('challenger1.wav')
mixer.music.play(-1)

pygame.display.set_caption("Space Invaders")

icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0


enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = 'ready'

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf',64) 

def show_score(x,y):
    score = font.render("Score: "+str(score_value),True,(255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text, (200,250))


def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x , y + 10))

def isCollison(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:

    screen.fill((0,255,255))
    
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            print('Key is pressed')
            if event.key == pygame.K_LEFT:
                print('Left')
                playerX_change = -0.15
            if event.key == pygame.K_RIGHT:
                print('Right')
                playerX_change = 0.15
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound = mixer.Sound('beam.wav')
                    bullet_sound.play()
                    print('Space')
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print('Released')
                playerX_change = 0

    playerX += playerX_change

    if playerX <=0:
        playerX = 0
    elif playerX>=768:
        playerX = 768

    for i in range(num_of_enemies):

        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <=0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i]>=768:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        collision = isCollison(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound('uff.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change


    

    player(playerX,playerY)
    show_score(textX,textY)

    
    pygame.display.update()