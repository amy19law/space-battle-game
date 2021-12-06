import pygame
import random

# Initialising Pygame
pygame.init()

# Declaring Sprites
icon = pygame.image.load('sprites/icon.png')
background = pygame.image.load('sprites/background.png')
planets = pygame.image.load('sprites/planets.png')
spaceship1 = pygame.image.load('sprites/spaceship1.png')
spaceship2 = pygame.image.load('sprites/spaceship2.png')
spaceshipDamaged1 = pygame.image.load('sprites/spaceshipdamaged1.png')
spaceshipDamaged2 = pygame.image.load('sprites/spaceshipdamaged2.png')
rivalSpaceship1 = pygame.image.load('sprites/rivalspaceship1.png')
rivalSpaceship2 = pygame.image.load('sprites/rivalspaceship2.png')
asteroid = pygame.image.load('sprites/asteroid.png')
rivalShooter = pygame.image.load('sprites/rivalshooter.png')
life = pygame.image.load('sprites/life.png')
spaceshipCrash1 = pygame.image.load('sprites/spaceshipcrash1.png')
spaceshipCrash2 = pygame.image.load('sprites/spaceshipcrash2.png')
spaceshipCrash3 = pygame.image.load('sprites/spaceshipcrash3.png')
spaceshipCrash4 = pygame.image.load('sprites/spaceshipcrash4.png')

spaceshipList = [spaceship1, spaceship2]
damagedSpaceshipList = [spaceshipDamaged1, spaceshipDamaged2]
rivalSpaceshipList = [rivalSpaceship1, rivalSpaceship2]

sprites = [icon, background, planets, spaceship1, spaceship2, spaceshipDamaged1,
               spaceshipDamaged2, rivalSpaceship1, rivalSpaceship2, asteroid, rivalShooter,
               life, spaceshipCrash1, spaceshipCrash2, spaceshipCrash3, spaceshipCrash4,]

# Declaring Colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
grey = (50, 50, 50)

# Declaring Font
font = "Symtext.ttf"

# Declaring Framerate
clock = pygame.time.Clock()
FPS = 35

# Spaceship Class
class Spaceship(object):

    health = 3
    animationNumber = 0
    animationList = spaceshipList
    counter = 0
    current = spaceshipList[animationNumber]
    crashCounter = 0
    damagedCounter = 0
    damaged = False
    wreckStart = False
    wrecked = False

    x = 0
    y = 0

    movingUp = False
    movingLeft = False
    movingDown = False
    movingRight = False

    next1 = True
    next2 = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def wreck(self):
        self.wreckStart = True
        self.crashCounter += 1
        if 5 <= self.crashCounter < 10:
            self.current = spaceshipCrash1
        if 10 <= self.crashCounter < 20:
            self.current = spaceshipCrash2
        if 20 <= self.crashCounter < 30:
            self.current = spaceshipCrash3
        if self.crashCounter >= 30:
            self.current = spaceshipCrash4
            self.crashCounter = 0
            self.wreckStart = False
            self.wrecked = True

    def damage(self):
        self.animationList = damagedSpaceshipList
        self.damagedCounter += 1
        if self.damagedCounter >= 15:
            self.animationList = spaceshipList
            self.damaged = False
            self.damagedCounter = 0

    def movement(self):

        speed = 10

        if not self.wreckStart:
            if (self.movingUp and self.movingLeft) or (self.movingDown and self.movingLeft):
                speed *= 0.8
            if (self.movingUp and self.movingRight) or (self.movingDown and self.movingRight):
                speed *= 0.8

            if self.movingUp:
                self.y -= speed
            if self.movingLeft:
                self.x -= speed
            if self.movingDown:
                self.y += speed
            if self.movingRight:
                self.x += speed*2

            if self.x > 200:
                self.x -= speed*2
            elif self.x > 100:
                self.x -= speed/2

            if self.x < 0:
                self.x += speed
            elif self.x < 100:
                self.x += speed/2

        if self.y < 0:
            self.y = 0

        if self.y > 550:
            self.health = 0

    def animation(self):

        self.counter += 1

        if self.counter == 2:

            if self.next1:
                self.current = self.animationList[0]
                self.next1 = False
                self.next2 = True
            elif self.next2:
                self.current = self.animationList[1]
                self.next2 = False
                self.next1 = True

            self.counter = 0

    def player_init(self):
        self.animation()
        self.movement()
        if self.damaged:
            self.damage()

# Rival Spaceship Class
class RivalSpaceship(object):

    shoot = False
    shootCounter = 0
    bullets = []

    animationNumber = 0
    counter = 0
    current = rivalSpaceshipList[animationNumber]

    crashCounter = 0

    wreckStart = False
    wrecked = False

    speed = 15

    x = 0
    y = 0

    movingUp = True
    movingLeft = False
    movingDown = False
    movingRight = False

    next1 = True
    next2 = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def movement(self):
        if self.x > 600:
            self.x -= 10
        else:
            if self.y > 100 and self.movingUp:
                self.y -= 2
            else:
                self.movingUp = False
                self.movingDown = True

            if self.y < 400 and self.movingDown:
                self.y += 2
            else:
                self.movingDown = False
                self.movingUp = True

    def animation(self):

        self.counter += 1

        if self.counter == 2:

            if self.next1:
                self.current = rivalSpaceshipList[0]
                self.next1 = False
                self.next2 = True
            elif self.next2:
                self.current = rivalSpaceshipList[1]
                self.next2 = False
                self.next1 = True

            self.counter = 0

    def shoot(self):

            self.shootCounter += 1

            if self.shootCounter >= 30:
                if not self.x > 600 and not self.x < 400:
                    self.bullets.append([self.x, self.y])
                    self.shootCounter = 0

    def init(self):
        self.movement()
        self.animation()
        self.shoot()

# Creating The Game Display
pygame.display.set_icon(icon)
displayWidth = 800
displayHeight = 600
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))


# Function For Text Rendering 
def messageDisplayed(message, textfont, size, color):
    myFont = pygame.font.Font(textfont, size)
    myMessage = myFont.render(message, 0, color)

    return myMessage

# Variables

# Player Variables
player = Spaceship(100, displayHeight/2-40)
moving = True

# Score Variables
score = 0
highscoreFile = open('highscore.dat', "r")
highscoreInt = int(highscoreFile.read())

# Planets Variables
planets_x = 800
planets_y = random.randint(0, 400)

# Rival Spaceship Variables
rivalSpaceship = RivalSpaceship(-200, displayHeight/2-40)
rivalSpaceshipAlive = False

# Rival Shooter Variables
rivalShooter_x = 800
rivalShooter_y = random.randint(0, 400)
rivalShooterAlive = False
rivalShooterHitPlayer = False

# Warning Variables
warningOnce = True
warning = False
warningCounter = 0
warningMessage = messageDisplayed("LAUNCH INCOMING", font, 60, red)

# Asteroid Variables
asteroid_x = 800
asteroid_y = random.randint(0, 400)

# Bullet Variables
bullets = []

# Declaring Sounds
shootBullet = pygame.mixer.Sound('sounds/shoot.wav')
collision = pygame.mixer.Sound('sounds/collision.wav')
crash = pygame.mixer.Sound('sounds/crash.wav')
optionSelected = pygame.mixer.Sound('sounds/select.wav')
rivalShooterWarning = pygame.mixer.Sound('sounds/warning.wav')
rivalShooterMoving = pygame.mixer.Sound('sounds/rival_shooter_moving.wav')

# Main Menu
def main_menu():

    menu = True
    selected = "play"
    while menu:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "play"
                elif event.key == pygame.K_DOWN:
                    selected = "exit game"
                if event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(optionSelected)
                    if selected == "play":
                        menu = False
                    if selected == "exit game":
                        pygame.quit()
                        quit()
                        
        # Displaying Background
        gameDisplay.blit(background, (0, 0))

        global planets_x
        global planets_y
        gameDisplay.blit(planets, (planets_x, planets_y))
        if planets_x <= 800 - 1100:
            planets_x = 800
            planets_y = random.randint(0, 400)
        else:
            if not player.wreckStart:
                planets_x -= 5

        # Displaying Text
        title = messageDisplayed("SPACE BATTLE", font, 80, white)
        controls1 = messageDisplayed("use the ARROW KEYS to move", font, 15, white)
        controls2 = messageDisplayed("SPACE to shoot and P to pause", font, 15, white)
        if selected == "play":
            play = messageDisplayed("PLAY", font, 60, white)
        else:
            play = messageDisplayed("PLAY", font, 55, grey)
        if selected == "exit game":
            exitGame = messageDisplayed("EXIT GAME", font, 60, white)
        else:
            exitGame = messageDisplayed("EXIT GAME", font, 55, grey)

        titleRect = title.get_rect()
        controls1Rect = controls1.get_rect()
        controls2Rect = controls2.get_rect()
        playRect = play.get_rect()
        exitGameRect = exitGame.get_rect()
        
        gameDisplay.blit(title, (displayWidth/2 - (titleRect[2]/2), 40))
        gameDisplay.blit(controls1, (displayWidth/2 - (controls1Rect[2]/2), 150))
        gameDisplay.blit(controls2, (displayWidth/2 - (controls2Rect[2]/2), 170))
        gameDisplay.blit(play, (displayWidth/2 - (playRect[2]/2), 230))
        gameDisplay.blit(exitGame, (displayWidth/2 - (exitGameRect[2]/2), 300))

        pygame.display.update()
        clock.tick(FPS)
            
                  
# Creating the Game Loop
def main_game():
    
    global rivalSpaceshipAlive
    global rivalShooter_x
    global rivalShooter_y
    global rivalShooterAlive
    global rivalShooterHitPlayer
    global warning
    global warningCounter
    global warningOnce
    global bullets
    global moving
    global highscoreFile
    global highscoreInt
    global score
    global planets_x
    global planets_y
    global asteroid_x
    global asteroid_y


    gameExit = False
    gameOver = False

    gameOverSelected = "play again"

    while not gameExit:
        while gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if score > highscoreInt:
                        highscoreFile = open('highscore.dat', "w")
                        highscoreFile.write(str(score))
                        highscoreFile.close()
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        gameOverSelected = "play again"
                    elif event.key == pygame.K_DOWN:
                        gameOverSelected = "exit game"
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.Sound.play(optionSelected)
                        if gameOverSelected == "play again":
                            if score > highscoreInt:
                                highscoreFile = open('highscore.dat', "w")
                                highscoreFile.write(str(score))
                                highscoreFile.close()
                            gameOver = False

                            score = 0
                            asteroid_x = 800
                            rivalSpaceship.x = -200
                            rivalSpaceshipAlive = False
                            rivalSpaceship.bullets = []
                            rivalShooter_x = 800
                            rivalShooterAlive = False
                            warning = False
                            warningCounter = 0
                            warningCounter = 0
                            player.wreckStart = False
                            player.y = displayHeight/2-40
                            player.x = 100
                            player.wrecked = False
                            player.health = 3
                            bullets = []

                            main_game()
                            
                        if gameOverSelected == "exit game":
                            pygame.quit()
                            quit()

            gameOverText = messageDisplayed("GAME OVER", font, 100, white)
            userScore = messageDisplayed("YOUR SCORE WAS: " + str(score), font, 50, white)
            if gameOverSelected == "play again":
                playAgain = messageDisplayed("PLAY AGAIN", font, 60, white)
            else:
                playAgain = messageDisplayed("PLAY AGAIN", font, 60, grey)
            if gameOverSelected == "exit game":
                exitGame = messageDisplayed("EXIT GAME", font, 60, white)
            else:
                exitGame = messageDisplayed("EXIT GAME", font, 60, grey)

            gameOverRect = gameOverText.get_rect()
            userScoreRect = userScore.get_rect()
            playAgainRect = playAgain.get_rect()
            exitGameRect = exitGame.get_rect()

            gameDisplay.blit(gameOverText, (displayWidth/2 - gameOverRect[2]/2, 20))
            gameDisplay.blit(userScore, (displayWidth/2 - (userScoreRect[2]/2+5), 150))
            gameDisplay.blit(playAgain, (displayWidth/2 - playAgainRect[2]/2, 240))
            gameDisplay.blit(exitGame, (displayWidth/2 - exitGameRect[2]/2, 300))

            pygame.display.update()
            clock.tick(10)

        # Event Handlers
        # Saving Score
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                if score > highscoreInt:
                    highscoreFile = open('highscore.dat', "w")
                    highscoreFile.write(str(score))
                    highscoreFile.close()
                pygame.quit()
                quit()
                
        # Player Inputs for Movements
            if moving:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player.movingUp = True
                    if event.key == pygame.K_LEFT:
                        player.movingLeft = True
                    if event.key == pygame.K_DOWN:
                        player.movingDown = True
                    if event.key == pygame.K_RIGHT:
                        player.movingRight = True
                    if event.key == pygame.K_SPACE:
                        if not player.wreckStart:
                            pygame.mixer.Sound.play(shootBullet)
                            bullets.append([player.x, player.y])
                    if event.key == pygame.K_p:
                        pygame.mixer.Sound.play(optionSelected)
                        pause()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        player.movingUp = False
                    if event.key == pygame.K_LEFT:
                        player.movingLeft = False
                    if event.key == pygame.K_DOWN:
                        player.movingDown = False
                    if event.key == pygame.K_RIGHT:
                        player.movingRight = False

        if player.health < 1:
            pygame.mixer.Sound.play(collision)
            player.wreck()

        if player.wrecked:
            gameOver = True

        # Displaying Background
        gameDisplay.blit(background, (0, 0))

        # Producing Position for Planets
        gameDisplay.blit(planets, (planets_x, planets_y))
        if planets_x <= 800 - 1100:
            planets_x = 800
            planets_y = random.randint(0, 400)
        else:
            if not player.wreckStart:
                planets_x -= 5
                
        # Displaying Score
        gameDisplay.blit(messageDisplayed("SCORE: {0}".format(score), font, 20, white), (10, 560))

        # Displaying High Score
        if score < highscoreInt:
            highScoreMessage = messageDisplayed("HIGH SCORE: {0}".format(highscoreInt), font, 20, white)
        else:
            highscoreFile = open('highscore.dat', "w")
            highscoreFile.write(str(score))
            highscoreFile.close()
            highscoreFile = open('highscore.dat', "r")
            highscoreInt = int(highscoreFile.read())
            highscoreFile.close()
            highScoreMessage = messageDisplayed("NEW HIGH SCORE: {0}".format(score), font, 20, white)
            
        highScoreMessageRect = highScoreMessage.get_rect()
        gameDisplay.blit(highScoreMessage, (800-highScoreMessageRect[2]-10, 560))

        # Displaying Health
        gameDisplay.blit(messageDisplayed("LIVES:".format(score), font, 20, white), (10, 10))
        if player.health >= 1:
            gameDisplay.blit(life, (90, 10))
            if player.health >= 2:
                gameDisplay.blit(life, (130, 10))
                if player.health >= 3:
                    gameDisplay.blit(life, (170, 10))
                            


        # Displaying Player
        gameDisplay.blit(player.current, (player.x, player.y))

        # Producing Position for Asteroid
        gameDisplay.blit(asteroid, (asteroid_x, asteroid_y))
        if asteroid_x <= 800 - 850:
            asteroid_x = 800
            asteroid_y = random.randint(0, 400)
        else:
            if not player.wreckStart:
                asteroid_x = asteroid_x - 10

        # Displaying Rival Spaceship
        gameDisplay.blit(rivalSpaceship.current, (rivalSpaceship.x, rivalSpaceship.y))

        # Displaying Rival Shooter
        gameDisplay.blit(rivalShooter, (rivalShooter_x, rivalShooter_y))

        # Enabling Animations/Movement
        player.player_init()
        rivalSpaceship.init()

        # Rendering Bullets
        if not player.wreckStart and not player.wrecked:
            for drawBullet in bullets:
                pygame.draw.rect(gameDisplay, yellow, (drawBullet[0]+120, drawBullet[1]+30, 20, 10))
            for moveBullet in range(len(bullets)):
                bullets[moveBullet][0] += 40
            for deleteBullet in bullets:
                if deleteBullet[0] >= 800:
                    bullets.remove(deleteBullet)
                  
        # Rendering Rival bullets
        if not player.wreckStart and not player.wrecked and not gameOver:
            for drawBullet in rivalSpaceship.bullets:
                pygame.draw.rect(gameDisplay, red, (drawBullet[0]+80, drawBullet[1]+30, 20, 10))
            for moveBullet in range(len(rivalSpaceship.bullets)):
                rivalSpaceship.bullets[moveBullet][0] -= 20
            for deleteBullet in rivalSpaceship.bullets:
                if deleteBullet[0] <= -50:
                    rivalSpaceship.bullets.remove(deleteBullet)

        # Spawning Opponents
        
        # Spawn Rival Spaceship at Random
        rivalSpawnNumber = random.randint(0, 100)
        if not rivalSpaceshipAlive and score > 500 and rivalSpawnNumber == 25:
            rivalSpaceshipAlive = True
            rivalSpaceship.x = 800
            
        # Spawn Rival Shooter at Random
        rivalShooterSpawnNumber = random.randint(0, 200)
        if not rivalShooterAlive and score > 1000 and rivalShooterSpawnNumber == 25:
            warning = True

        # Display Warning before Rival Shooter is Spawned
        if warning:
            if warningOnce:
                pygame.mixer.Sound.play(rivalShooterWarning)
                gameDisplay.blit(warningMessage, (100, 100))
                warningOnce = False
            if warningCounter > 40:
                pygame.mixer.Sound.play(rivalShooterMoving)
                rivalShooterAlive = True
                warningCounter = 0
                warning = False
                warningOnce = True
            else:
                warningCounter = warningCounter + 1

        # Setting Rival Shooter's Movement
        if rivalShooterAlive:
            rivalShooter_x = rivalShooter_x - 30
        if rivalShooter_x < -100:
            rivalShooterHitPlayer = False
            rivalShooterAlive = False
            rivalShooter_x = 800
            rivalShooter_y = random.randint(0, 400)


        # Detecting Collisions

        # Producing Position for Asteroids and Setting Them to be Deleted if Hit by Player's Bullet
        for shootAsteroid in bullets:
            if asteroid_x < shootAsteroid[0]+80 < asteroid_x+60 and asteroid_y < shootAsteroid[1]+30 < asteroid_y+90:
                bullets.remove(shootAsteroid)
                pygame.mixer.Sound.play(shootBullet)
                asteroid_x = 800-850
                score = score + 50
            elif asteroid_x < shootAsteroid[0]+80 < asteroid_x+60 and asteroid_y < shootAsteroid[1]+30 < asteroid_y+90:
                bullets.remove(shootAsteroid)
                pygame.mixer.Sound.play(shootBullet)
                asteroid_x = 800-850
                score = score + 50

        # Detecting Collision between Asteroid and Player
        if asteroid_x < player.x < asteroid_x+70 or asteroid_x < player.x+100 < asteroid_x+70:
            if asteroid_y < player.y < asteroid_y+80 or asteroid_y < player.y+80 < asteroid_y+80:
                player.damaged = True
                pygame.mixer.Sound.play(collision)
                player.health = player.health - 1
                asteroid_x = 800-850

        # Detecting Collision between Player and Rival Spaceship Bullets 
        for hitRivalSpaceship in bullets:
            if rivalSpaceship.x < hitRivalSpaceship[0]+80 < rivalSpaceship.x+90 or rivalSpaceship.x < hitRivalSpaceship[0]+90 < rivalSpaceship.x+90:
                if rivalSpaceship.y < hitRivalSpaceship[1]+30 < rivalSpaceship.y+70 or rivalSpaceship.y < hitRivalSpaceship[1]+40 < rivalSpaceship.y+70:
                    if not rivalSpaceship.x > 600:
                        pygame.mixer.Sound.play(crash)
                        score = score + 100
                        bullets.remove(hitRivalSpaceship)
                        rivalSpaceship.x = -200
                        rivalSpaceshipAlive = False

        # Detecting Collision between Rival Spaceship Bullets and Player        
        for hitPlayer in rivalSpaceship.bullets:
            if player.x < hitPlayer[0] < player.x+100 or player.x < hitPlayer[0]+40 < player.x+100:
                if player.y < hitPlayer[1]+40 < player.y+80 or player.y < hitPlayer[1]+40 < player.y+80:
                    player.damaged = True
                    pygame.mixer.Sound.play(collision)
                    player.health = player.health - 1
                    rivalSpaceship.bullets.remove(hitPlayer)

        # Detecting Collision between Player and Rival Shooter Bullets 
        for hitRivalShooter in bullets:
            if rivalShooter_x < hitRivalShooter[0]+80 < rivalShooter_x+90 or rivalShooter_x < hitRivalShooter[0]+80 < rivalShooter_x+90:
                if rivalShooter_y < hitRivalShooter[1]+30 < rivalShooter_y+70 or rivalShooter_y < hitRivalShooter[1]+30 < rivalShooter_y+70:
                    if not rivalShooter_x > 700:
                        pygame.mixer.Sound.play(crash)
                        bullets.remove(hitRivalShooter)
                        score = score + 200
                        rivalShooterHitPlayer = False
                        rivalShooterAlive = False
                        rivalShooter_x = -200
                        rivalShooter_y = random.randint(0, 400)

        # Detecting Collision between Rival Shooter Bullets and Player
        if rivalShooter_x < player.x < rivalShooter_x+100 or rivalShooter_x < player.x+100 < rivalShooter_x+100:
            if rivalShooter_y < player.y < rivalShooter_y+85 or rivalShooter_y < player.y+75 < rivalShooter_y+85:
                if not rivalShooterHitPlayer:
                    player.damaged = True
                    pygame.mixer.Sound.play(collision)
                    player.health = player.health - 1
                    rivalShooterHitPlayer = True

        pygame.display.update()
        clock.tick(FPS)
        
# Pause Menu
def pause():

    paused = True

    player.movingUp = False
    player.movingLeft = False
    player.movingDown = False
    player.movingRight = False

    # Displaying Text
    pausedText = messageDisplayed("PAUSED", font, 120, white)
    returnToGameText = messageDisplayed("Press Enter to return to game!", font, 20, white)
    pausedTextRect = pausedText.get_rect()
    returnToGameTextRect = returnToGameText.get_rect()

    gameDisplay.blit(pausedText, (displayWidth/2 - (pausedTextRect[2]/2), 50))
    gameDisplay.blit(returnToGameText, (displayWidth/2 - (returnToGameTextRect[2]/2), 200))

    pygame.display.update()
    clock.tick(15)

    # Saving New Highscore
    global highscoreFile
    global highscoreInt

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > highscoreInt:
                    highscoreFile = open('highscore.dat', "w")
                    highscoreFile.write(str(score))
                    highscoreFile.close()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(optionSelected)
                    paused = False

                    
main_menu()
main_game()
pygame.quit()
quit()

