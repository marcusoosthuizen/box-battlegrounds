#Importing and Initing Pygame
import pygame
import random
import time
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
sWidth = 1080
sHeight = 720
screen = pygame.display.set_mode((sWidth,sHeight))
pygame.display.set_caption('Box Battlegrounds')
icon = pygame.image.load(resource_path('./sprites/icon.ico'))
pygame.display.set_icon(icon)

last_time = time.time()
dttimer = 0


#Variables
mousedown = False

orbSpawnCount = 0
orbs = []
particles = []

slowmotion = 1

screenShake = 0
shakeX = 0
shakeY = 0

xFace = 0
yFace = 0

run = False
gameStart = False
startCountdown = -100

roundover = False

menu = True
menuTrans = False

plLose = 14
loseTF = True

currentMode = 0
modeCount = 0
localVar = 0

wlightTimer = 150

modes = ['Gravity Mayhem', 'Lights Out', 'Super Speed', 'Rumble Showdown', 'Black Holes!', 'Orb Drought', 'Reversed Controls?!']
playedModes = []

#Images
blank = pygame.image.load(resource_path('./sprites/blank.png'))

Img3 = pygame.image.load(resource_path('./sprites/3.png'))
Img3size = 0
Img2 = pygame.image.load(resource_path('./sprites/2.png'))
Img2size = 0
Img1 = pygame.image.load(resource_path('./sprites/1.png'))
Img1size = 0
ImgGO = pygame.image.load(resource_path('./sprites/Go.png'))
ImgGOsize = 0
ImgKNOCKOUT = pygame.image.load(resource_path('./sprites/Knockout.png'))
ImgKNOCKOUTsize = 0

redImg = 0
blueImg = 0
dashImg = 0
redSize = 0

modeImg = pygame.image.load(resource_path('./sprites/modes/mode' + '1' + '.png'))
modeImg = pygame.transform.scale(modeImg, (0,0))

logoX = sWidth / 2 - 238

logoImg = pygame.image.load(resource_path("./sprites/menu/Logo.png"))

playX = sWidth / 2 - 132

playImg = pygame.image.load(resource_path("./sprites/menu/Play.png"))
playImg = pygame.transform.scale(playImg, (264, 171)) # 88, 57
playHImg = pygame.image.load(resource_path("./sprites/menu/PlayH.png"))
playHImg = pygame.transform.scale(playHImg, (264, 171)) # 88, 57

redWinsImg = pygame.image.load(resource_path('./sprites/redWins.png'))
blueWinsImg = pygame.image.load(resource_path('./sprites/blueWins.png'))

tutorialImg = pygame.image.load(resource_path('./sprites/howToPlay.png'))

crownImg = pygame.image.load(resource_path('./sprites/crown.png'))
crownImg = pygame.transform.scale(crownImg, (75, 75))

#Fonts
pyfont = pygame.font.Font(None, 50)

modeText = pyfont.render('Gravity Mayhem', False, (0, 0, 0))


#Global Functions
def collisionCheck():
    if pl1.x < pl2.x + pl2.size and pl1.x + pl1.size > pl2.x:
        if pl1.y < pl2.y + pl2.size and pl1.y + pl1.size > pl2.y:
            knockbackCalc()

def knockbackCalc():
    global run
    global roundover
    global screenShake

    pl1.size -= positiveOf(pl2.xVel) + positiveOf(pl2.yVel) / 7
    pl2.size -= positiveOf(pl1.xVel) + positiveOf(pl1.yVel) / 7

    if pl1.size < 50:
        pl1.dead = True
        run = False
        roundover = True
        pygame.mixer.music.stop()



    if pl2.size < 50:
        pl2.dead = True
        run = False
        roundover = True
        pygame.mixer.music.stop()


    pl1.xVel *= -1
    pl2.xVel *= -1
    pl1.yVel *= -1
    pl2.yVel *= -1

    if pl1.x > pl2.x:
        xFace = -1
        pl1.xVel += pl2.size / 5
        pl2.xVel -= pl1.size / 5


    else:
        xFace = 1
        pl1.xVel -= pl2.size / 5
        pl2.xVel += pl1.size / 5
    if pl1.y > pl2.y:
        yFace = -1
        pl1.yVel += pl2.size / 5
        pl2.yVel -= pl1.size / 5
    else:
        yFace = 1
        pl1.yVel -= pl2.size / 5
        pl2.yVel += pl1.size / 5

    for i in range(int(pl1.size / 3)):
        pX = pl1.x + (pl1.size / 2)
        pY = pl1.y + (pl1.size / 2)
        particles.append( Particle(pX,pY,pl1.size,(255,0,0),0) )
    for i in range(int(pl1.size / 3)):
        pX = pl2.x + (pl2.size / 2)
        pY = pl2.y + (pl2.size / 2)
        particles.append( Particle(pX,pY,pl2.size,(0,0,255),0) )

    pl1.x += pl1.xVel
    pl2.x += pl2.xVel
    pl1.y += pl1.yVel
    pl2.y += pl2.yVel

    screenShake = 5


def shakeScreen():
    global shakeX
    global shakeY
    global screenShake

    shakeX = random.randint(0,16) - 4
    shakeY = random.randint(0, 16) - 4
    screenShake -= 1


def countdown():
    global startCountdown
    global Img3
    global Img2
    global Img1
    global ImgGO
    global Img3size
    global Img2size
    global Img1size
    global ImgGOsize
    global gameStart



    startCountdown += 1

    if startCountdown >= 30 and startCountdown <= 45:
        Img3size += 10
        Img3 = pygame.image.load(resource_path('./sprites/3.png'))
        Img3 = pygame.transform.scale(Img3, (Img3size, Img3size))

    elif startCountdown >= 45 and startCountdown <= 60:
        Img3size -= 10
        Img3 = pygame.image.load(resource_path('./sprites/3.png'))
        Img3 = pygame.transform.scale(Img3, (Img3size, Img3size))

    elif startCountdown >= 60 and startCountdown <= 75:
        Img3size = 0
        Img2size += 10
        Img2 = pygame.image.load(resource_path('./sprites/2.png'))
        Img2 = pygame.transform.scale(Img2, (Img2size, Img2size))

    elif startCountdown >= 75 and startCountdown <= 90:
        Img2size -= 10
        Img2 = pygame.image.load(resource_path('./sprites/2.png'))
        Img2 = pygame.transform.scale(Img2, (Img2size, Img2size))

    elif startCountdown >= 90 and startCountdown <= 105:
        Img2size = 0
        Img1size += 10
        Img1 = pygame.image.load(resource_path('./sprites/1.png'))
        Img1 = pygame.transform.scale(Img1, (Img1size, Img1size))

    elif startCountdown >= 105 and startCountdown <= 120:
        Img1size -= 10
        Img1 = pygame.image.load(resource_path('./sprites/1.png'))
        Img1 = pygame.transform.scale(Img1, (Img1size, Img1size))

    elif startCountdown >= 120 and startCountdown <= 135:
        Img1size = 0
        ImgGOsize += 10
        ImgGO = pygame.image.load(resource_path('./sprites/Go.png'))
        ImgGO = pygame.transform.scale(ImgGO, (ImgGOsize * 2, ImgGOsize))

    elif startCountdown >= 135 and startCountdown <= 140:
        gameStart = True


    elif startCountdown >= 180 and startCountdown <= 194:
        ImgGOsize -= 10
        ImgGO = pygame.image.load(resource_path('./sprites/Go.png'))
        ImgGO = pygame.transform.scale(ImgGO, (ImgGOsize * 2, ImgGOsize))

    elif startCountdown >= 196:
        ImgGOsize = 0
        startCountdown = 2000


def positiveOf(num):
    if num < 0:
        return -1 * num
    else:
        return num


def displayResults():
    global startCountdown
    global loser
    global redImg
    global blueImg
    global dashImg
    global screen
    global redSize
    global redWinsImg
    global blueWinsImg

    if startCountdown <= 175 and startCountdown >= 100:
        redImg = pygame.image.load(resource_path('./sprites/red' + str(pl1.score) + '.png'))
        redSize = (startCountdown - 100) * 2
        redImg = pygame.transform.scale(redImg, (redSize, redSize))
        blueImg = pygame.image.load(resource_path('./sprites/blue' + str(pl2.score) + '.png'))
        blueImg = pygame.transform.scale(blueImg, (redSize, redSize))
        dashImg = pygame.image.load(resource_path('./sprites/dash.png'))
        dashImg = pygame.transform.scale(dashImg, (redSize, redSize))

    elif startCountdown == 300:
        if loser == 1:
            pl2.score += 1
        elif loser == 2:
            pl1.score += 1


        redImg = pygame.image.load(resource_path('./sprites/red' + str(pl1.score) + '.png'))
        redImg = pygame.transform.scale(redImg, (redSize, redSize))
        blueImg = pygame.image.load(resource_path('./sprites/blue' + str(pl2.score) + '.png'))
        blueImg = pygame.transform.scale(blueImg, (redSize, redSize))
        dashImg = pygame.image.load(resource_path('./sprites/dash.png'))
        dashImg = pygame.transform.scale(dashImg, (redSize, redSize))

    elif startCountdown <= 637 and startCountdown >= 600:
        redImg = pygame.image.load(resource_path('./sprites/red' + str(pl1.score) + '.png'))
        redSize = (637 - startCountdown) * 4
        redImg = pygame.transform.scale(redImg, (redSize, redSize))
        blueImg = pygame.image.load(resource_path('./sprites/blue' + str(pl2.score) + '.png'))
        blueImg = pygame.transform.scale(blueImg, (redSize, redSize))
        dashImg = pygame.image.load(resource_path('./sprites/dash.png'))
        dashImg = pygame.transform.scale(dashImg, (redSize, redSize))

    elif startCountdown >= 637 and startCountdown <= 675:
        if pl1.score == 3:

            redWinsImg = pygame.image.load(resource_path('./sprites/redWins.png'))
            redSize = (startCountdown - 637) * 2
            redWinsImg = pygame.transform.scale(redWinsImg, (redSize * 10, redSize * 2))

        elif pl2.score == 3:

            blueWinsImg = pygame.image.load(resource_path('./sprites/blueWins.png'))
            redSize = (startCountdown - 637) * 2
            blueWinsImg = pygame.transform.scale(blueWinsImg, (redSize * 10, redSize * 2))

        else:
            redImg = pygame.image.load(resource_path('./sprites/next-round.png'))
            redSize = (startCountdown - 637) * 2
            redImg = pygame.transform.scale(redImg, (redSize * 8, redSize))

            blueImg = pygame.image.load(resource_path('./sprites/box.png'))
            blueImg = pygame.transform.scale(blueImg, (int(redSize * 1.5), int(redSize * 1.5)))

    elif startCountdown >= 937 and startCountdown <= 975:
        if pl1.score != 3 and pl2.score != 3:
            redImg = pygame.image.load(resource_path('./sprites/next-round.png'))
            redSize = (975 - startCountdown) * 2
            redImg = pygame.transform.scale(redImg, (redSize * 8, redSize))

            blueImg = pygame.image.load(resource_path('./sprites/box.png'))
            blueImg = pygame.transform.scale(blueImg, (int(redSize * 1.5), int(redSize * 1.5)))


    if startCountdown >= 100 and startCountdown <= 637:
        screen.blit(redImg, (sWidth / 4 - redSize / 2, sHeight / 4 - redSize / 2))
        screen.blit(blueImg, ((sWidth / 4) * 3 - redSize / 2, sHeight / 4 - redSize / 2))
        screen.blit(dashImg, ((sWidth / 2) - redSize / 2, sHeight / 4 - redSize / 2))
    elif startCountdown >= 637:
        if pl1.score == 3:
            screen.blit(redWinsImg, ((sWidth / 2) - (redSize / 2) * 10, sHeight / 4 - redSize))
        elif pl2.score == 3:
            screen.blit(blueWinsImg, ((sWidth / 2) - (redSize / 2) * 10, sHeight / 4 - redSize))
        else:
            screen.blit(redImg, ((sWidth / 2) - (redSize / 2) * 8, sHeight / 4 - redSize / 2))
            screen.blit(blueImg, ((sWidth / 2) - (int(redSize * 1.5) / 2), (sHeight / 5) * 2 - int(redSize * 1.5) / 2))


def relocatePl():
    global startCountdown
    global pl1X
    global pl1Y
    global pl1S
    global pl2X
    global pl2Y
    global pl2S

    startCountdown += 1


    if startCountdown <= 200 and startCountdown >= 101:
        pl1.x += ((sWidth / 4) - pl1X) / 100
        pl1.y += ((sHeight / 4) * 3 - pl1Y) / 100
        pl1.size += (75 - pl1S) / 100

        pl2.x += ((sWidth / 4) * 3 - pl2X) / 100
        pl2.y += ((sHeight / 4) * 3 - pl2Y) / 100
        pl2.size += (75 - pl2S) / 100

    else:
        pl1.xVel = 0
        pl1.yVel = 0
        pl2.xVel = 0
        pl2.yVel = 0


def moveKnockout(num):
    global ImgKNOCKOUTsize
    if num >= 100 and ImgKNOCKOUTsize >= 150:
        return (num - 100) * 10
    else:
        return 0


def modeShuffle():
    global startCountdown
    global redSize
    global modeImg
    global modeCount
    global currentMode
    global screen
    global localVar
    global modeText
    global modes
    global playedModes
    global light
    global lightTimer

    if pl1.score != 3 and pl2.score != 3:

        if startCountdown == 825:
            randomVar = True
            while randomVar:
                randomVar = False
                currentMode = random.randint(1, 7)
                for i in playedModes:
                    if i == currentMode:
                        randomVar = True

            playedModes.append(currentMode)

            light = 0
            lightTimer = 150
            modeImg = pygame.image.load(resource_path('./sprites/modes/mode' + str(currentMode) + '.png'))
            modeImg = pygame.transform.scale(modeImg, (redSize, redSize))
            modeText = pyfont.render(modes[currentMode - 1], False, (0, 0, 0))
        elif startCountdown >= 675 and startCountdown < 825:

            localVar = str(startCountdown)
            localVar = localVar[2]



            if localVar == '5':

                modeCount += 1
                if modeCount > 7:
                    modeCount = 1

                modeImg = pygame.image.load(resource_path('./sprites/modes/mode' + str(modeCount) + '.png'))
                modeImg = pygame.transform.scale(modeImg, (redSize, redSize))
                modeText = pyfont.render(modes[modeCount - 1], False, (0, 0, 0))

        if startCountdown >= 675 and startCountdown <= 937:
            screen.blit(modeImg, (sWidth / 2 - redSize + 39, sHeight / 2 - redSize - 34))
            if startCountdown >= 825 and startCountdown <= 937:
                screen.blit(modeText, (sWidth / 2 - len(modes[currentMode - 1]) * 9, sHeight / 2 + 10))
            elif startCountdown >= 675 and startCountdown <= 825:
                screen.blit(modeText, (sWidth / 2 - len(modes[modeCount - 1]) * 9, sHeight / 2 + 10))


def lightsOut():
    global light
    global lightTimer

    lightTimer += 1

    if lightTimer >= 100 and lightTimer <= 150:
        light -= 5

    elif lightTimer >= 151 and lightTimer <= 201:
        light += 5

    elif lightTimer == 202:
        lightTimer = 0


#Declaring Classes
class Player:
    def __init__(self, x, y, size, color, score):
        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0
        self.size = size
        self.color = color
        self.dead = False
        self.hitCount = 0
        self.score = score

    def boundaryCheck(self):
        if self.x < 0:
            self.x = 0
            self.xVel = 0
        elif self.x + self.size > sWidth:
            self.x = sWidth - self.size
            self.xVel = 0

        if self.y < 0:
            self.y = 0
            self.yVel = 0
        elif self.y + self.size > sHeight:
            self.y = sHeight - self.size
            self.yVel = 0

    def updateHitbox(self):
        self.hitbox = [self.x, self.y, self.x + self.size, self.y + self.size]


    def velApply(self):
        self.xVel -= self.xVel / 25 * slowmotion

        if currentMode == 1 and roundover == False or currentMode == 1 and startCountdown == 2000:
            self.yVel += 1
            if self.y + self.size > sHeight:
                self.y = sHeight - self.size + 1
                self.yVel = 0
        else:
            self.yVel -= self.yVel / 25 * slowmotion

        if self.xVel > -0.5 and self.xVel < 0.5:
            self.xVel = 0
        if self.yVel > -0.5 and self.yVel < 0.5:
            self.yVel = 0

        if currentMode != 3:
            if self.xVel > self.size / 10:
                self.xVel = self.size / 10
            elif self.xVel < -1 * (self.size / 10):
                self.xVel = -1 * (self.size / 10)

            if currentMode == 1:
                if self.yVel < -30:
                    self.yVel = -30
            else:
                if self.yVel > self.size / 10:
                    self.yVel = self.size / 10
                elif self.yVel < -1 * (self.size / 10):
                    self.yVel = -1 * (self.size / 10)

        self.x += self.xVel * slowmotion
        self.y += self.yVel * slowmotion

    def render(self):
        pygame.draw.rect(screen, self.color, (self.x + shakeX, self.y + shakeY, self.size, self.size))

        if self.hitCount == 0:
            eyeX1 = (self.x + (self.size / 5) * 2) + self.xVel
            eyeY1 = (self.y + (self.size / 7)) + self.yVel
            eyeX2 = (self.x + (self.size / 5) * 2) + self.xVel
            eyeY2 = (self.y + (self.size / 7) * 4) + self.yVel
            pygame.draw.line(screen, (0,0,0), (eyeX1 + shakeX, eyeY1 + shakeY), (eyeX2 + shakeX, eyeY2 + shakeY), int(self.size / 12))

            eyeX1 = (self.x + self.size - (self.size / 5) * 2) + self.xVel
            eyeY1 = (self.y + (self.size / 7)) + self.yVel
            eyeX2 = (self.x + self.size - (self.size / 5) * 2) + self.xVel
            eyeY2 = (self.y + (self.size / 7) * 4) + self.yVel
            pygame.draw.line(screen, (0, 0, 0), (eyeX1 + shakeX, eyeY1 + shakeY), (eyeX2 + shakeX, eyeY2 + shakeY), int(self.size / 12))
        else:
            self.hitCount -= 1

            eyeX1 = (self.x + (self.size / 7) * 1) + self.xVel
            eyeY1 = (self.y + (self.size / 14) * 1) + self.yVel
            eyeX2 = (self.x + (self.size / 7) * 3) + self.xVel
            eyeY2 = (self.y + (self.size / 14) * 3) + self.yVel
            eyeX3 = (self.x + (self.size / 7) * 1) + self.xVel
            eyeY3 = (self.y + (self.size / 14) * 5) + self.yVel

            pygame.draw.lines(screen,(0,0,0), False, ((eyeX1,eyeY1),(eyeX2,eyeY2),(eyeX3,eyeY3)), int(self.size / 12))

            eyeX1 = (self.x + self.size - (self.size / 7) * 1) + self.xVel
            eyeY1 = (self.y + (self.size / 14) * 1) + self.yVel
            eyeX2 = (self.x  + self.size - (self.size / 7) * 3) + self.xVel
            eyeY2 = (self.y + (self.size / 14) * 3) + self.yVel
            eyeX3 = (self.x  + self.size - (self.size / 7) * 1) + self.xVel
            eyeY3 = (self.y + (self.size / 14) * 5) + self.yVel

            pygame.draw.lines(screen, (0, 0, 0), False, ((eyeX1, eyeY1), (eyeX2, eyeY2), (eyeX3, eyeY3)),int(self.size / 12))




class Orb:
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.size = size
        self.growing = True
        self.life = 0
        self.dead = False

        if run:
            self.maxSize = random.randint(10,20)

        else:
            self.maxSize = random.randint(10, 30)

        if currentMode == 5 and run:
            self.color = (0, 0, 0)
        else:
            self.color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))


    def updateSize(self):
        if self.dead:
            self.life += 1
            self.size -= self.maxSize / 5

            if self.size <= 5:
                    orbs.remove(self)

        else:
            self.life += 1
            if self.maxSize > self.size and self.growing == True:
                self.size += self.maxSize / 5
            elif self.maxSize < self.size:
                self.growing = False

    def orbCollision(self):
        global run
        global roundover

        if self.growing == False:

            if self.x < pl2.x + pl2.size and self.x + self.size > pl2.x:
                if self.y < pl2.y + pl2.size and self.y + self.size > pl2.y:
                    self.size -= 1
                    if currentMode == 5:
                        pl2.size -= 0.5

                        if pl2.size < 50:
                            pl2.dead = True
                            run = False
                            roundover = True
                    else:
                        pl2.size += 0.5


            if self.x < pl1.x + pl1.size and self.x + self.size > pl1.x:
                if self.y < pl1.y + pl1.size and self.y + self.size > pl1.y:
                    self.size -= 1
                    if currentMode == 5:
                        pl1.size -= 0.5

                        if pl1.size < 50:
                            pl1.dead = True
                            run = False
                            roundover = True
                    else:
                        pl1.size += 0.5

            if self.size <= 5:
                    orbs.remove(self)


class Particle:
    def __init__(self,x,y,plSize,color,type):
        self.plSize = plSize
        self.x = x + random.randint(0, int(self.plSize))

        if type == 0:
            self.y = y + random.randint(0, int(self.plSize))
        else:
            self.y = y - 25

        self.tx = random.randint(-50,50)
        self.ty = random.randint(-50,50)
        self.size = 10
        self.type = type
        self.color = color
        if slowmotion != 1:
            self.life = 20
        else:
            self.life = 10

    def particleUpdate(self):
        self.x += self.tx / 10 * slowmotion
        self.y += self.ty / 10 * slowmotion
        self.life -= 1
        if self.life <= 0:
            self.size -= 1
            if self.size <= 1:
                particles.remove(self)

    def pRender(self):
        if self.type == 0:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))


for i in range(25):
    orbx = random.randint(50, sWidth - 50)
    orby = random.randint(50, sHeight - 50)
    orbs.append(Orb(orbx, orby, 1))
    orbSpawnCount = 0


tutorial = True

while True:
    while menu:

        dt = time.time() - last_time
        last_time = time.time()
        dttimer += dt

        # Checks for exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousedown = True

        if dttimer > 1 / 60:
            dttimer = 0

            # Generates orbs
            orbSpawnCount += 1
            if orbSpawnCount > 100:
                orbx = random.randint(50, sWidth - 50)
                orby = random.randint(50, sHeight - 50)
                orbs.append(Orb(orbx, orby, 1))
                orbs[random.randint(0, len(orbs) - 1)].dead = True
                orbSpawnCount = 0

            for o in orbs:
                o.updateSize()

            keys = pygame.key.get_pressed()

            for k in keys:
                if k == 1 and logoX <= sWidth + 476 and playX >= sWidth:
                    tutorial = False


            # Menu Transition
            if menuTrans:
                logoX -= 40

                if playX <= sWidth:
                    playX += 35

                if logoX <= sWidth + 476 and playX >= sWidth:

                    if tutorial == False:
                        pygame.mixer.music.stop()
                        menu = False
                        menuTrans = False
                        run = True
                        gameStart = False

                        pl1 = Player(sWidth / 4 - 37.5, sHeight / 2 - 37.5, 75, (255, 0, 0), 0)
                        pl2 = Player((sWidth / 4) * 3 - 37.5, sHeight / 2 - 37.5, 75, (0, 0, 255), 0)

                        orbs.clear()

                        for i in range(10):
                            orbx = random.randint(50, sWidth - 50)
                            orby = random.randint(50, sHeight - 50)
                            orbs.append(Orb(orbx, orby, 1))
                            orbSpawnCount = 0



            # Updates Screen
            screen.fill((255, 255, 255))

            for o in orbs:
                pygame.draw.circle(screen, o.color, (o.x + shakeX, o.y + shakeY), o.size)

            screen.blit(logoImg, (logoX, 50))
            if pygame.mouse.get_pos()[0] > sWidth / 2 - 132 and pygame.mouse.get_pos()[0] < sWidth / 2 + 132 and pygame.mouse.get_pos()[1] > sHeight / 2 and pygame.mouse.get_pos()[1] < sHeight / 2 + 171 and menuTrans == False:

                screen.blit(playHImg, (playX, sHeight / 2))

                if mousedown:
                    menuTrans = True

            else:
                screen.blit(playImg, (playX, sHeight / 2))

            if tutorial and logoX <= sWidth + 476 and playX >= sWidth:
                screen.blit(tutorialImg, (0, 0))

            pygame.display.update()

            mousedown = False



    while run:

        dt = time.time() - last_time
        last_time = time.time()
        dttimer += dt

        if dttimer > 1 / 60:
 
            #Checks for exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            

            if gameStart:
                #Checks for inputs
                keys = pygame.key.get_pressed()

                if keys[pygame.K_w]:
                    if currentMode == 1:
                        if pl1.y + pl1.size >= sHeight:
                            pl1.yVel -= 30
                    else:
                        if currentMode != 7:
                            pl1.yVel -= pl1.size / 50
                        else:
                            pl1.yVel += pl1.size / 50
                if keys[pygame.K_s]:
                    if currentMode != 1:
                        if currentMode != 7:
                            pl1.yVel += pl1.size / 50
                        else:
                            pl1.yVel -= pl1.size / 50
                if keys[pygame.K_a]:
                    if currentMode != 7:
                        pl1.xVel -= pl1.size / 50
                    else:
                        pl1.xVel += pl1.size / 50
                if keys[pygame.K_d]:
                    if currentMode != 7:
                        pl1.xVel += pl1.size / 50
                    else:
                        pl1.xVel -= pl1.size / 50


                if keys[pygame.K_UP]:
                    if currentMode == 1:
                        if pl2.y + pl2.size >= sHeight:
                            pl2.yVel -= 30
                    else:
                        if currentMode != 7:
                            pl2.yVel -= pl2.size / 50
                        else:
                            pl2.yVel += pl2.size / 50
                if keys[pygame.K_DOWN]:
                    if currentMode != 1:
                        if currentMode != 7:
                            pl2.yVel += pl2.size / 50
                        else:
                            pl2.yVel -= pl2.size / 50
                if keys[pygame.K_LEFT]:
                    if currentMode != 7:
                        pl2.xVel -= pl2.size / 50
                    else:
                        pl2.xVel += pl2.size / 50
                if keys[pygame.K_RIGHT]:
                    if currentMode != 7:
                        pl2.xVel += pl2.size / 50
                    else:
                        pl2.xVel -= pl2.size / 50


            #Applies Velocity
            pl1.velApply()
            pl2.velApply()

            #Generates orbs
            if currentMode != 6:
                orbSpawnCount += 1
                if orbSpawnCount > 50:
                    orbx = random.randint(50, sWidth - 50)
                    orby = random.randint(50, sHeight - 50)
                    orbs.append(Orb(orbx,orby,1))
                    orbSpawnCount = 0

                for o in orbs:
                    o.updateSize()

            #Checks for collisions
            collisionCheck()
            pl1.boundaryCheck()
            pl2.boundaryCheck()

            for p in particles:
                p.particleUpdate()
            if gameStart:
                for o in orbs:
                    o.orbCollision()

        #Updates and displays sprites
            shakeY = 0
            shakeX = 0

            if currentMode == 4:
                screenShake = 1

            if screenShake > 0:
                shakeScreen()

        screen.fill((255,255,255))

        for o in orbs:
            pygame.draw.circle(screen, o.color, (o.x + shakeX, o.y + shakeY), o.size)

        pl1.render()
        pl2.render()

        for p in particles:
            p.pRender()

        
        if dttimer > 1 / 60:
            dttimer = 0
            if startCountdown < 199:
                countdown()
        if Img3size != 0:
            screen.blit(Img3, (sWidth / 2 - Img3size / 2, sHeight / 2 - Img3size / 2))
        if Img2size != 0:
            screen.blit(Img2, (sWidth / 2 - Img2size / 2, sHeight / 2 - Img2size / 2))
        if Img1size != 0:
            screen.blit(Img1, (sWidth / 2 - Img1size / 2, sHeight / 2 - Img1size / 2))
        if ImgGOsize != 0:
            screen.blit(ImgGO, (sWidth / 2 - ImgGOsize, sHeight / 2 - ImgGOsize / 2))

        if currentMode == 2:
            if gameStart:
                lightsOut()

            blank.set_alpha(light)
            screen.blit(blank, (0, 0))

        pygame.display.update()


    while roundover:

        dt = time.time() - last_time
        last_time = time.time()
        dttimer += dt

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        if dttimer > 1 / 60:
            dttimer = 0

            slowmotion = 0.5

            plwait = 0

            if pl1.dead:
                for i in range(int(pl1.size * 2)):
                    pX = pl1.x + (pl1.size / 2)
                    pY = pl1.y + (pl1.size / 2)
                    particles.append(Particle(pX, pY, pl1.size, (255, 0, 0),0))

                pl1.x = -100
                pl1.xVel = 0
                pl1.dead = False
                loser = 1

            elif pl2.dead:
                for i in range(int(pl1.size * 2)):
                    pX = pl2.x + (pl2.size / 2)
                    pY = pl2.y + (pl2.size / 2)
                    particles.append(Particle(pX, pY, pl2.size, (0, 0, 255),0))

                pl2.x = sWidth + 100
                pl2.xVel = 0
                pl2.dead = False
                loser = 2

            

            pl1.velApply()
            pl2.velApply()

            for p in particles:
                p.particleUpdate()

            shakeY = 0
            shakeX = 0
            if screenShake > 0:
                shakeScreen()

            screen.fill((255, 255, 255))

            for o in orbs:
                pygame.draw.circle(screen, o.color, (o.x + shakeX, o.y + shakeY), o.size)

            if startCountdown >= 300 and ImgKNOCKOUTsize >= 151 and startCountdown <= 600 or pl1.score == 3 or pl2.score == 3:
                if loser == 1:
                    pl1.yVel = 10

                    if loseTF:
                        plLose += 1
                    else:
                        plLose -= 1

                    pl1.xVel = plLose

                    if plLose == 15:
                        loseTF = False
                    elif plLose == -15:
                        loseTF = True

                    pl1.x = sWidth / 4 - 37.5
                    pl1.y = (sHeight / 4) * 3 - 37.5

                    pl2.x = (sWidth / 4) * 3 - 37.5
                    pl2.y = (sHeight / 4) * 3 - 75 + ( int(plLose / 3) ** 2 ) * 2

                elif loser == 2:
                    pl2.yVel = 10

                    if loseTF:
                        plLose += 1
                    else:
                        plLose -= 1

                    pl2.xVel = plLose

                    if plLose == 15:
                        loseTF = False
                    elif plLose == -15:
                        loseTF = True

                    pl1.x = sWidth / 4 - 37.5
                    pl1.y = (sHeight / 4) * 3 - 75 + ( int(plLose / 3) ** 2 ) * 2

                    pl2.x = (sWidth / 4) * 3 - 37.5
                    pl2.y = (sHeight / 4) * 3 - 37.5

            elif startCountdown >= 600 and ImgKNOCKOUTsize >= 151 and startCountdown <= 675:


                pl1.x = sWidth / 4 - 37.5
                pl1.y = (sHeight / 4) * 3 - 37.5

                pl2.x = (sWidth / 4) * 3 - 37.5
                pl2.y = (sHeight / 4) * 3 - 37.5

            elif startCountdown >= 675 and ImgKNOCKOUTsize >= 151 and startCountdown <= 936:

                modeShuffle()

                pl1.xVel = 10
                pl1.yVel = -7

                pl2.xVel = -10
                pl2.yVel = -7

                pl1.x = sWidth / 4 - 37.5
                pl1.y = (sHeight / 4) * 3 - 37.5

                pl2.x = (sWidth / 4) * 3 - 37.5
                pl2.y = (sHeight / 4) * 3 - 37.5

            elif startCountdown >= 937 and ImgKNOCKOUTsize >= 151 and startCountdown <= 975:

                pl1.x = sWidth / 4 - 37.5
                pl1.y -= (sHeight / 4) / 38

                pl2.x = (sWidth / 4) * 3 - 37.5
                pl2.y -= (sHeight / 4) / 38




            pl1.render()
            pl2.render()

            for p in particles:
                p.pRender()

            for o in orbs:
                if startCountdown >= 300 and ImgKNOCKOUTsize >= 151:
                    o.size -= 0.1

            if ImgKNOCKOUTsize <= 150 and pl1.xVel == 0 and pl1.yVel == 0 and pl2.xVel == 0 and pl2.yVel == 0:
                if ImgKNOCKOUTsize == 150:
                    startCountdown = 0
                    pl1X = pl1.x + 37.5
                    pl1Y = pl1.y + 37.5
                    pl2X = pl2.x + 37.5
                    pl2Y = pl2.y + 37.5
                    pl1S = pl1.size
                    pl2S = pl2.size

                ImgKNOCKOUTsize += 10
                ImgKNOCKOUT = pygame.image.load(resource_path('./sprites/Knockout.png'))
                ImgKNOCKOUT = pygame.transform.scale(ImgKNOCKOUT, (ImgKNOCKOUTsize * 5, ImgKNOCKOUTsize))

            if startCountdown < 2000:
                relocatePl()
                displayResults()



            if pl1.xVel == 0 and pl1.yVel == 0 and pl2.xVel == 0 and pl2.yVel == 0 or startCountdown < 2000 and sHeight / 2 - ImgKNOCKOUTsize / 2 - moveKnockout(startCountdown) > 0:
                screen.blit(ImgKNOCKOUT, (sWidth / 2 - ImgKNOCKOUTsize * 5 / 2, sHeight / 2 - ImgKNOCKOUTsize / 2 - moveKnockout(startCountdown)))

            if pl1.score == 3:
                screen.blit(crownImg, (sWidth / 4 - 37.5, sHeight / 2))
            elif pl2.score == 3:
                screen.blit(crownImg, ((sWidth / 4) * 3 - 37.5, sHeight / 2))

            if startCountdown >= 750 and ImgKNOCKOUTsize >= 151:
                if pl1.score == 3 or pl2.score == 3:
                    continueText = pyfont.render('Press any key to continue', False, (0, 0, 0))
                    screen.blit(continueText, (sWidth / 2 - 220, (sHeight / 10) * 9))


                    keys = pygame.key.get_pressed()
                    for k in keys:
                        if k == 1:
                            roundover = False
                            menu = True
                            menuTrans = False
                            logoX = sWidth / 2 - 238
                            playX = sWidth / 2 - 132
                            startCountdown = -100
                            slowmotion = 1
                            ImgKNOCKOUTsize = 0
                            currentMode = 0
                            playedModes = []
                            plLose = 14


            pygame.display.update()

            if startCountdown >= 976 and ImgKNOCKOUTsize >= 151:
                if pl1.score != 3 and pl2.score != 3:
                    roundover = False
                    run = True
                    gameStart = False
                    startCountdown = 0
                    pl1 = Player(sWidth / 4 - 37.5, sHeight / 2 - 37.5, 75, (255, 0, 0), pl1.score)
                    pl2 = Player((sWidth / 4) * 3 - 37.5, sHeight / 2 - 37.5, 75, (0, 0, 255), pl2.score)
                    slowmotion = 1
                    ImgKNOCKOUTsize = 0


    if currentMode != 6:
        for i in range(10):
            orbx = random.randint(50, sWidth - 50)
            orby = random.randint(50, sHeight - 50)
            orbs.append(Orb(orbx, orby, 1))
            orbSpawnCount = 0