import pygame
import random

pygame.mixer.pre_init(frequency = 44100, size = -16, channels = 1, buffer = 512)
pygame.init()

birdIcon = pygame.image.load('assets/bluebird-midflap.png')

width = 576 
height = 1024
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(birdIcon)
clock = pygame.time.Clock()
gameFont = pygame.font.Font("04B_19.ttf",40)

gravity = 0.25
birdMovement = 0
gameRunning = True
score = 0
highScore = 0

background = pygame.image.load('assets/background-night.png').convert()
background = pygame.transform.scale2x(background)

ground = pygame.image.load('assets/base.png').convert()
ground = pygame.transform.scale2x(ground)
groundX = 0

birdDownflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
birdMidflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
birdUpflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
birdFrames = [birdDownflap, birdMidflap, birdUpflap]
birdIndex = 0
bird = birdFrames[birdIndex]
birdRect = bird.get_rect(center = (100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipeSurface = pygame.image.load('assets/pipe-green.png').convert()
pipeSurface = pygame.transform.scale2x(pipeSurface)
pipeList = []
spawnPipe = pygame.USEREVENT
pygame.time.set_timer(spawnPipe, 1600)
pipeHeight = [400, 500, 600]

gameOverImg = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
gameOverRect = gameOverImg.get_rect(center = (288, 512))

flapSound = pygame.mixer.Sound('sound/sfx_wing.wav')
deathSound = pygame.mixer.Sound('sound/sfx_hit.wav')
scoreSound = pygame.mixer.Sound('sound/sfx_point.wav')
scoreSoundCountdown = 100

def drawGround():
    win.blit(ground, (groundX, 900))
    win.blit(ground, (groundX + 576, 900))


def createPipe():
    global topPipe
    global bottomPipe

    randomPipePos = random.choice(pipeHeight)
    bottomPipe = pipeSurface.get_rect(midtop = (700, randomPipePos))
    topPipe = pipeSurface.get_rect(midbottom = (700, randomPipePos - 300))
    return bottomPipe, topPipe


def movePipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes



def drawPipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            win.blit(pipeSurface,pipe)
        else:
            flipPipe = pygame.transform.flip(pipeSurface, False, True)
            win.blit(flipPipe, pipe)




def collision(pipes):
    for pipe in pipes: 
        if birdRect.colliderect(pipe):
            deathSound.play()
            return False
    
    if birdRect.top <= 0 or birdRect.bottom >= 900:
        deathSound.play()
        return False
    
    return True

def rotateBird(bird):
    newBird = pygame.transform.rotozoom(bird, -birdMovement * 3, 1)
    return newBird


def birdAnimation():
    newBird = birdFrames[birdIndex]
    newBirdRect = newBird.get_rect(center = (100, birdRect.centery))
    return newBird, newBirdRect

def displayScore(gameState):
    if gameState == "game running":
        scoreSurface = gameFont.render(str(int(score)), True, (255,255,255))
        scoreRect = scoreSurface.get_rect(center = (288, 100))
        win.blit(scoreSurface, scoreRect)
    if gameState == "game over":
        scoreSurface = gameFont.render(f'Score: {int(score)}', True, (255,255,255))
        scoreRect = scoreSurface.get_rect(center = (288, 100))
        win.blit(scoreSurface, scoreRect)

        highScoreSurface = gameFont.render(f'High Score: {int(highScore)}', True, (255,255,255))
        highScoreRect = highScoreSurface.get_rect(center = (288, 850))
        win.blit(highScoreSurface, highScoreRect)


def updateScore(score, highScore):
    if score > highScore:
        highScore = score

    return highScore

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameRunning == True:
                birdMovement = 0
                birdMovement -= 10
                flapSound.play()
            if event.key == pygame.K_SPACE and gameRunning == False:
                gameRunning = True
                pipeList.clear()
                birdRect.center = (100, 512)
                birdMovement = 0
                score = 0
            if event.key == pygame.K_q:
                pygame.quit()
            
        if event.type == spawnPipe:
            pipeList.extend(createPipe())

        if event.type == BIRDFLAP:
            if birdIndex < 2:
                birdIndex += 1
            else:
                birdIndex = 0

            bird, birdRect = birdAnimation()

    win.blit(background, (0,0))

    if gameRunning:
        # Bird
        birdMovement += gravity
        rotatedBird = rotateBird(bird)
        birdRect.centery += birdMovement
        win.blit(rotatedBird, birdRect)
        gameRunning = collision(pipeList)

        # Pipes
        pipeList = movePipes(pipeList) 
        drawPipe(pipeList)
        score += 0.01
        displayScore("game running")
        scoreSoundCountdown -= 1
        if scoreSoundCountdown <= 0:
            scoreSound.play()
            scoreSoundCountdown = 100

    else:
        win.blit(gameOverImg, gameOverRect)
        highScore = updateScore(score, highScore)
        displayScore("game over")

    # Floor
    groundX -= 1
    drawGround()
    if groundX <= -576:
        groundX = 0

    pygame.display.update()
    clock.tick(100)





