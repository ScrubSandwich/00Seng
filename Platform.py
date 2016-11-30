'''
Created on June 20, 2015
Jacob Miecznikowski
Jason Choi
Luis Aguilar
Grant Knight
'''

import pygame
import sys
import time
import math
import random

pygame.init()

class Game():
    def __init__(self):
        self.screenSize = (0, 0)       
        self.screen = pygame.display.set_mode(self.screenSize, pygame.FULLSCREEN)
        pygame.display.set_caption("Platform")
        self.mainSurface = pygame.display.get_surface()
        self.backgroundImage = pygame.image.load("graphics//bg.jpg")
        self.backgroundColor = [0, 0, 0]
        self.continueGame = True
                 
        self.updateList = RemovableList()
        self.moveList = []
        self.enemyList = RemovableList()
        self.enemyProbability = 10
        
        self.terrain = Terrain(self.mainSurface, self)
        self.enemy = Enemy(self.mainSurface, self)
        self.enemyList.addToMainList(self.enemy)
        self.screenClock = pygame.time.Clock()
        self.player = Player(self.mainSurface, self)
        self.gun = Gun(self.mainSurface, self.player, self)
        self.background = Background(self.mainSurface, self.backgroundImage, self)
        self.scoreBoard = ScoreBoard(self.mainSurface, self.screenClock, self.gun, self)
        self.body = Body( self.mainSurface, self, self.enemy, self.enemyList)
        
        self.updateList.addToMainList(self.background)
        self.player.setGun(self.gun)
        self.player.setSword()
        self.updateList.addToMainList(self.terrain)
        self.updateList.addToMainList(self.body)
        self.updateList.addToMainList(self.player)
        self.updateList.addToMainList(self.enemy)
        self.updateList.addToMainList(self.scoreBoard)
        
        self.moveList.append(self.terrain)
        self.moveList.append(self.enemy)
        self.moveList.append(self.background)
        
        inputSurface = self.mainSurface
        inputPlayer = self.player
        powerUp = PowerUp(inputSurface, inputPlayer)
        self.updateList.addToMainList(powerUp)
        
        self.mixer = pygame.mixer.init()
        
        self.FPS = 40
        
        self.movingLeft = False
        self.movingRight = False        
        
        for x in self.moveList:
            x.movingLeft = False
            x.movingRight = False
            
        self.playerSpeed = 10 
    
    def addToUpdates(self, inputObj):     
        self.updateList.addToMainList(inputObj)
        
    def gameOver(self):
        self.continueGame = False
        
    def main(self):
        pygame.mixer.music.load("audio//jamesbond.ogg")
        pygame.mixer.music.play(-1)
        while self.continueGame == True:
            self.screenClock.tick(self.FPS)
            self.screen.fill(self.backgroundColor)
            #self.mainSurface.blit(self.backgroundImage, (0, 0))
            chanceForEnemy = random.randint(0, 100)
            if chanceForEnemy < self.enemyProbability:
                e = Enemy(self.mainSurface, self)
                self.enemyList.addToMainList(e)
                self.updateList.addToMainList(e)
                self.moveList.append(e)
                self.enemyProbability += 0.001
            self.enemyList.removeAll()
            self.updateList.removeAll()
            for x in self.updateList.getMainList():
                x.update()
            self.check_input()
            pygame.display.update()
            
        
        pygame.mixer.music.load("audio//airhorn.ogg")
        pygame.mixer.music.play(-1)
        
        self.backgroundImage = pygame.image.load("gameover/rekt.jpg")
        self.backgroundImage2 = pygame.image.load("gameover/noob.png")
        self.backgroundImage3 = pygame.image.load("gameover/fite.png")
        self.backgroundImage4 = pygame.image.load("gameover/noscope.png")
        self.backgroundImage5 = pygame.image.load("gameover/glasses.jpg")
        self.backgroundImage6 = pygame.image.load("gameover/fresh_meat.jpg")
        self.backgroundImage7 = pygame.image.load("gameover//drinkmonster.png")
        self.backgroundImage8 = pygame.image.load("gameover/stopcyberbullying.png")
        
        self.mainSurface.blit(self.backgroundImage, (0, 0))
        self.mainSurface.blit(self.backgroundImage2, (500, 0))
        self.mainSurface.blit(self.backgroundImage3, (1000, 0))
        self.mainSurface.blit(self.backgroundImage4, (0, 470))
        self.mainSurface.blit(self.backgroundImage5, (0, 900))
        self.mainSurface.blit(self.backgroundImage6, (800, 575))
        self.mainSurface.blit(self.backgroundImage7, (1250, 500))
        self.mainSurface.blit(self.backgroundImage8, (800, 525))
        
        pygame.font.init()
        
        scoreString = "Game Over. Your final score is " + str(self.scoreBoard.score)
        self.scoreString = scoreString

        self.thingy = pygame.font.Font(None, 50)

        self.finalScoreSurface = pygame.image.load("gameover/frame.png")
        self.finalScoreSurfaceText = self.thingy.render(self.scoreString, False, [150, 50, 100])
        self.finalScoreSurfaceText = pygame.transform.scale(self.finalScoreSurfaceText, (800, 100))
        
        self.finalScoreRect = self.finalScoreSurface.get_rect()    
        self.finalScoreSurfaceTextRect = self.finalScoreSurfaceText.get_rect()  
        
        self.finalScoreRect.x = 350
        self.finalScoreRect.y = (self.mainSurface.get_height() / 2.5) - 60
        
        self.finalScoreSurfaceTextRect.x = (self.mainSurface.get_width() // 2) - (self.mainSurface.get_height() / 4) - 120
        self.finalScoreSurfaceTextRect.y = (self.mainSurface.get_height() / 3) + 50
        
        self.mainSurface.blit(self.finalScoreSurface, self.finalScoreRect)
        self.mainSurface.blit(self.finalScoreSurfaceText, self.finalScoreSurfaceTextRect)        
        
        pygame.display.update()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONDOWN:
                break

    def getPlayerSpeed(self):
        return self.playerSpeed
            
    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    sys.exit()
                elif event.key == pygame.K_LSHIFT:
                    for i in self.moveList:
                        i.setSpeed(50)
                    self.playerSpeed = 50
                elif event.key == pygame.K_a:
                    for i in self.moveList:
                        i.movingRight = True
                        i.residual_direction = -1
                elif event.key == pygame.K_d:
                    for i in self.moveList:
                        i.movingLeft = True
                        i.residual_direction = 1
                elif event.key == pygame.K_RETURN:
                    self.player.attack()
                elif event.key == pygame.K_1:
                    self.player.toSword()
                elif event.key == pygame.K_2:
                    self.player.toGun()
    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    for i in self.moveList:
                        i.setSpeed(0)
                elif event.key == pygame.K_a:
                    for i in self.moveList:
                        i.movingRight = False
                elif event.key == pygame.K_d:
                    for i in self.moveList:
                        i.movingLeft = False
 
class ScoreBoard():
    def __init__(self, inputSurface, inputClock, gun, game):
        self.game = game
        self.mainSurface = inputSurface
        self.clock = inputClock
        self.curTime = self.clock.get_time()
        self.width = 10
        self.height = 10
        self.gun = gun
        self.lives = 3
        self.score = 0
        
        pygame.font.init()
        self.timeLabel = pygame.font.Font(None, 50)
        self.timeSurface = pygame.Surface([self.width, self.height])
        self.timeRect = self.timeSurface.get_rect()
        
        self.scoreLabel = pygame.font.Font(None, 50)
        self.scoreSurface = pygame.Surface([self.width, self.height])
        self.scoreRect = self.scoreSurface.get_rect()
        
        self.livesLabel = str("Health: ") + str("3")
        self.livesLabel = pygame.font.Font(None, 50)
        self.livesSurface = pygame.Surface([self.width, self.height])
        self.livesRect = self.livesSurface.get_rect()
        
        self.ammoLabel = str("Ammo: ") + str(self.gun.ammo)
        self.ammoLabel = pygame.font.Font(None, 50)
        self.ammoSurface = pygame.Surface([self.width, self.height])
        self.ammoRect = self.ammoSurface.get_rect()
        
    def update(self):
        lapsedTime = 60 - time.clock()
        timeString = "Time: " + str(int(lapsedTime))
        self.timeSurface = self.timeLabel.render(timeString, False, [200, 200, 0])
        self.timeRect.x = 0
        self.timeRect.y = 0
        self.mainSurface.blit(self.timeSurface, self.timeRect)
        
        scoreString = "Score: " + str(self.score)
        self.scoreSurface = self.scoreLabel.render(scoreString, False, [200, 200, 0])
        self.scoreRect.x = 0
        self.scoreRect.y = (self.mainSurface.get_height() / 20)
        self.mainSurface.blit(self.scoreSurface, self.scoreRect)
                
        livesCount = "Lives: " + str(self.lives)
        self.livesSurface = self.livesLabel.render(livesCount, False, [200, 200, 0])
        self.livesRect.x = 0
        self.livesRect.y = (self.mainSurface.get_height() / 10)
        self.mainSurface.blit(self.livesSurface, self.livesRect)
        
        livesCount = "Ammo: " + str(self.gun.ammo)
        self.ammoSurface = self.ammoLabel.render(livesCount, False, [200, 200, 0])
        self.ammoRect.x = 0
        self.ammoRect.y = (self.mainSurface.get_height() / 7)
        self.mainSurface.blit(self.ammoSurface, self.ammoRect)
        
        if lapsedTime <= 0:
            self.game.continueGame = False

class Background():
    def __init__(self, mainSurface, backgroundImage, game):
        self.game = game
        self.backgroundSurface = backgroundImage
        self.mainSurface = mainSurface
        self.height = (self.mainSurface.get_height() / 5)
        self.backgroundRect = self.backgroundSurface.get_rect()
        self.initialX = -6000
        self.initialY = 0
        self.backgroundRect.x = self.initialX
        self.backgroundRect.y = self.initialY
        
    def setSpeed(self, newSpeed):
        self.speed = newSpeed

    def update(self):
        if self.movingRight == True:
            self.backgroundRect.x += self.game.getPlayerSpeed() / 4
        if self.movingLeft == True:
            self.backgroundRect.x -= self.game.getPlayerSpeed() / 4
        self.mainSurface.blit(self.backgroundSurface, self.backgroundRect)

class RemovableList():
    def __init__(self):
        self.mainList = []
        self.removeList = []
    
    def removeAll(self):
        for toRemove in self.removeList:
            try:
                self.mainList.remove(toRemove)
            except:
                pass
        self.removeList = []
            
    def selectForRemoval(self, inputObj):
        self.removeList.append(inputObj)
        
    def addToMainList(self, inputObj):
        self.mainList.append(inputObj)
        
    def getMainList(self):
        return self.mainList
    
class Terrain():
    def __init__(self, inputSurface, game):
        self.game = game
        self.speed = 10
        self.width = inputSurface.get_width()
        self.mainSurface = inputSurface
        self.height = (self.mainSurface.get_height() / 5)
        self.terrainSurface = pygame.Surface([self.width, self.height])
        self.terrainRect = self.terrainSurface.get_rect()
        self.initialX = -5000
        self.initialY = (self.mainSurface.get_height() - (self.mainSurface.get_height() / 7))
        self.terrainRect.x = self.initialX
        self.terrainRect.y = self.initialY
        self.terrainSurface = pygame.image.load("graphics//terrain.png")
        self.residual_direction = 0
    
    def setSpeed(self, newSpeed):
        self.speed = newSpeed

    def update(self):
        if self.movingRight == True:
            self.terrainRect.x += self.speed + 2.5
        if self.movingLeft == True:
            self.terrainRect.x -= self.speed + 2.5
        self.mainSurface.blit(self.terrainSurface, self.terrainRect)

class PowerUp():
    def __init__(self, inputSurface, inputPlayer):
        self.width = 25
        self.height = 25
        self.mainSurface = inputSurface
        self.powerSurface = pygame.Surface([self.width, self.height])
        self.powerRect = self.powerSurface.get_rect()
        self.powerSurface = pygame.image.load("graphics//Powerup.jpeg")
        self.initialX = (self.mainSurface.get_width() / 20)
        self.initialY = (self.mainSurface.get_height() - (self.mainSurface.get_height() / 3)) + 60
        self.powerRect.x = self.initialX
        self.powerRect.y = self.initialY
        self.player = inputPlayer
        self.eaten = False
        
    def update(self):
        if not self.eaten:
            self.mainSurface.blit(self.powerSurface, self.powerRect)
        if self.player.playerRect.colliderect(self.powerRect):
            self.eaten = True
            
class Body():
    def __init__(self, inputSurface, game, enemy, enemyList):
        self.game = game
        self.terrain = self.game.terrain
        self.mainSurface = inputSurface
        self.bodySurface = pygame.image.load("graphics//1.png")
        self.bodySurface2 = pygame.image.load("graphics//2.png")
        self.bodySurface3 = pygame.image.load("graphics//3.png")
        self.bodySurface4 = pygame.image.load("graphics//4.png")
        self.bodySurface5 = pygame.image.load("graphics//5.png")
        
        self.bodyRect = self.bodySurface.get_rect()
        self.initialX = (self.mainSurface.get_width() / 2)
        self.initialY = (self.mainSurface.get_height() - (self.mainSurface.get_height() / 3))
        self.enemy = enemy
        self.enemyList = enemyList
        self.bodyRect.x = self.initialX
        self.bodyRect.y = self.initialY        
        self.counter = 0
        self.surfaceToDraw = self.bodySurface       
        self.game = game
        
    def update(self):
        listToRemove = []
        if self.terrain.movingLeft == True:
            self.counter += 1
            if self.counter < 5:
                self.surfaceToDraw = self.bodySurface
            elif self.counter >= 5 and self.counter < 10:
                self.surfaceToDraw = self.bodySurface2
            elif self.counter >= 10 and self.counter < 15:
                self.surfaceToDraw = self.bodySurface3
            elif self.counter >= 15 and self.counter < 20:
                self.surfaceToDraw = self.bodySurface4               
            elif self.counter >= 20 and self.counter < 25:
                self.counter = 0
                self.surfaceToDraw = self.bodySurface5
        self.mainSurface.blit(self.surfaceToDraw, self.bodyRect)
        
        for enemy in self.enemyList.getMainList():
                    if self.bodyRect.colliderect(enemy.enemyRect):
                        enemy.setDead()
                        listToRemove.append(enemy)
                        self.game.scoreBoard.lives -= 1
                        self.enemyList.selectForRemoval(enemy)
                    if self.game.scoreBoard.lives == 0:
                        self.game.gameOver()
        
        if self.terrain.movingRight == True:
            self.counter += 1
            if self.counter < 5:
                self.surfaceToDraw = pygame.transform.flip(self.bodySurface, True, False)
            elif self.counter >= 5 and self.counter < 10:
                self.surfaceToDraw = pygame.transform.flip(self.bodySurface2, True, False)
            elif self.counter >= 10 and self.counter < 15:
                self.surfaceToDraw = pygame.transform.flip(self.bodySurface3, True, False)
            elif self.counter >= 15 and self.counter < 20:
                self.surfaceToDraw = pygame.transform.flip(self.bodySurface4, True, False)               
            elif self.counter >= 20 and self.counter < 25:
                self.counter = 0
                self.surfaceToDraw = pygame.transform.flip(self.bodySurface5, True, False)
        self.mainSurface.blit(self.surfaceToDraw, self.bodyRect)
                                   
class Sword():
    def __init__(self, inputSurface, player, enemy, enemyList, updateList, game):
        self.game = game
        self.terrain = self.game.terrain
        self.width = 5
        self.height = 20
        self.mainSurface = inputSurface
        self.player = player
        self.enemy = enemy
        self.enemyList = enemyList
        self.swordSurface = pygame.image.load("graphics//sword.png")
        self.swordRect = self.swordSurface.get_rect()
        self.swordSurface = pygame.transform.rotate(self.swordSurface, 180)
        self.initialX = (self.mainSurface.get_width() / 2) - (self.swordSurface.get_width() / 5) + 60
        self.initialY = (self.mainSurface.get_height() - (self.mainSurface.get_height() / 3)) - 90
        self.swordRect.x = self.initialX
        self.swordRect.y = self.initialY
        self.movingUp = False
        self.movingDown = False
        self.movingRight = False
        self.movingLeft = False
        self.hasAttacked = False
        self.swordTimer = 0
        self.updateList = updateList
        self.surfaceToDraw =self.swordSurface
        self.residual_direction = 1
        self.rightSword = (self.mainSurface.get_width() / 2) - (self.swordSurface.get_width() / 5) + 60
        self.leftSword = (self.mainSurface.get_width() / 2) + 60
        self.hilt = 35

    def attack(self):
        self.hasAttacked = True

    def update(self): #this switches the sword image between attack and non attack
        if self.player.holdingSword:
            if self.hasAttacked == False:
                if self.terrain.residual_direction == -1:
                    self.surfaceToDraw = pygame.transform.flip(self.swordSurface, True, False)
                    self.swordRect.x = (self.mainSurface.get_width() / 2) + 60
                    self.swordRect.y = self.initialY
                elif self.terrain.residual_direction == 1:
                    self.surfaceToDraw = self.swordSurface
                    self.swordRect.x = (self.mainSurface.get_width() / 2) - (self.swordSurface.get_width() / 5) + 60
                    self.swordRect.y = self.initialY
                self.mainSurface.blit(self.surfaceToDraw, self.swordRect)
            listToRemove = []
            
            if self.hasAttacked == True:
                if self.terrain.residual_direction == 1:         
                    self.swordRect.y = self.initialY + self.swordSurface.get_height() - self.swordSurface.get_width()
                    self.swordRect.x = self.initialX + self.swordSurface.get_width() - 25
                    self.rotatedSwordSurface = pygame.transform.rotate(self.swordSurface, -90)
                    self.rotatedSwordRect = self.rotatedSwordSurface.get_rect()
                    self.mainSurface.blit(self.rotatedSwordSurface, self.swordRect)
                elif self.terrain.residual_direction == -1:
                    self.swordRect.y = self.initialY + self.swordSurface.get_height() - self.hilt
                    self.swordRect.x = self.initialX - math.ceil(self.swordSurface.get_height() / 2) - (self.hilt / 2)
                    self.rotatedSwordSurface = pygame.transform.rotate(self.swordSurface, 90)
                    self.rotatedSwordRect = self.rotatedSwordSurface.get_rect()
                    self.mainSurface.blit(self.rotatedSwordSurface, self.swordRect)  
                               
                for enemy in self.enemyList.getMainList():
                    if self.swordRect.colliderect(enemy.enemyRect):
                        self.game.scoreBoard.score += 10
                        enemy.setDead()
                        self.updateList.selectForRemoval(enemy)
                        self.enemyList.selectForRemoval(enemy)
                        
                if self.swordTimer == 5:
                    self.hasAttacked = False
                    self.swordTimer = 0
                else:
                    self.swordTimer += 1
                for enemyToDel in listToRemove:
                    self.enemyList.remove(enemyToDel)
                for enemyToDel2 in listToRemove:
                    self.updateList.remove(enemyToDel2)

class Gun():
    def __init__(self, inputSurface, player, game):
        self.game = game
        self.terrain = self.game.terrain
        self.mainSurface = inputSurface
        self.player = player
        self.gunSurface = pygame.image.load("graphics//gun.png")
        self.gunRect = self.gunSurface.get_rect()
        self.initialX = (self.mainSurface.get_width() / 2) + 160
        self.initialY = (self.mainSurface.get_height() - (self.mainSurface.get_height() / 3)) + 30
        self.gunRect.x = self.initialX
        self.gunRect.y = self.initialY
        self.hasFired = False
        self.gunTimer = 0
        self.ammo = 10
        self.game = game
        self.surfaceToDraw = self.gunSurface
        self.residual_direction = 1
        
    def attack(self):
        self.hasFired = True
        
    def update(self): #this switches the image between attack and non attack
        if self.terrain.residual_direction != 0:
            self.residual_direction = self.terrain.residual_direction
        if self.player.holdingGun:
            if self.terrain.movingRight == True:
                
                self.surfaceToDraw = pygame.transform.flip(self.gunSurface, True, False)
                self.gunRect.x = (self.mainSurface.get_width() / 2) + 36
            elif self.terrain.movingLeft == True:
                
                self.surfaceToDraw = self.gunSurface
                self.gunRect.x = (self.mainSurface.get_width() / 2) + 160
            self.mainSurface.blit(self.surfaceToDraw, self.gunRect)
            if self.ammo == 0:
                self.hasFired = False
            if self.hasFired == True:
                self.hasFired = False
                self.ammo -= 1
                if self.gunTimer == 0:
                    self.gunTimer = 0
                    bullet = Bullet(self.mainSurface, self, self.game.enemyList, self.game.updateList, self.game, self.residual_direction)
                    self.game.addToUpdates(bullet)
                else:
                    self.gunTimer += 1

class Bullet():
    def __init__(self, inputSurface, gun, enemyList, updateList, game, direction):
        self.game = game
        self.terrain = self.game.terrain
        self.mainSurface = inputSurface
        self.gun = gun
        self.Player = Player
        self.enemyList = enemyList
        self.updateList = updateList
        self.bulletSurface = pygame.image.load("graphics//Bullet.png")
        self.bulletRect = self.bulletSurface.get_rect()
        self.initialY = gun.initialY
        self.initialX = gun.gunRect.x
        if self.terrain.movingLeft:
            self.initialX = gun.gunRect.x + 50
            self.initialY = gun.initialY            
        self.bulletRect.x = self.initialX
        self.bulletRect.y = self.initialY
        self.dead = False
        self.direction = direction
        
    def setDead(self):
        self.dead = True
        
    def update(self):
        self.bulletRect.x += self.direction * 20
        if self.bulletRect.x > self.mainSurface.get_width() or self.bulletRect.x < 0 - self.bulletSurface.get_width():
            self.updateList.selectForRemoval(self)
        else:
            for enemy in self.enemyList.getMainList():
                if enemy.enemyRect.colliderect(self.bulletRect):
                    self.game.scoreBoard.score += 10
                    enemy.setDead()
                    self.setDead()
                    self.updateList.selectForRemoval(enemy)
                    self.enemyList.selectForRemoval(enemy)
                    self.updateList.selectForRemoval(self)
        self.mainSurface.blit(self.bulletSurface, self.bulletRect)
 
class Enemy():
    def __init__(self, inputSurface, game):
        global globalEnemyCount
        self.game = game
        self.mainSurface = inputSurface
        self.terrain = self.game.terrain
        self.originalSurface = pygame.image.load("graphics//karagoingleft.png")
        self.enemySurface = self.originalSurface
        self.enemyRect = self.enemySurface.get_rect()
        self.initialX = (self.mainSurface.get_width() - (self.mainSurface.get_width() / 6))
        self.initialY = (self.mainSurface.get_height() - (self.mainSurface.get_height() / 3))
        self.enemyRect.x = self.initialX
        self.enemyRect.y = self.initialY
        if self.terrain.residual_direction == -1:
            self.movingLeft = True
            self.movingRight = False
        elif self.terrain.residual_direction == 1:
            self.movingRight = True
            self.movingLeft = False
        else:
            self.movingRight = False
            self.movingLeft = False
        self.dead = False
        
        leftOrRight = random.randint(0, 1)
        placeRand = random.randint(0, 50)
        if leftOrRight == 0:
            self.initialX = 0 - placeRand
        else:
            self.initialX = self.mainSurface.get_width() + placeRand
        self.enemyRect.x = self.initialX
        self.enemyRect.y = self.initialY
        
    def setDead(self):
        self.dead = True

    def setSpeed(self, newSpeed):
        self.speed = newSpeed
        
    def update(self):        
        # to the left of us
        if self.enemyRect.x < self.game.player.playerRect.x:
            
            # player moving left
            if self.movingRight == True:
                self.enemyRect.x += (3 + self.game.player.speed)
            # player moving right
            elif self.movingLeft == True:
                self.enemyRect.x += (3 - self.game.player.speed)
            else:
                self.enemyRect.x += 3       
            
        # to the right of us
        if self.enemyRect.x > self.game.player.playerRect.x:
            
            # player moving left
            if self.movingRight == True:
                self.enemyRect.x += (self.game.player.speed - 3)
            # player moving right
            elif self.movingLeft == True:
                self.enemyRect.x += (-3 - self.game.player.speed)
            else:
                self.enemyRect.x -= 3 
    
        if not self.dead:
            self.mainSurface.blit(self.enemySurface, self.enemyRect)
            
class Player():
    def __init__(self, inputSurface, game):
        self.mainSurface = inputSurface
        self.game = game
        self.terrain = self.game.terrain
        self.originalSurface = pygame.image.load("graphics//Seng.png")
        self.originalSurface = pygame.transform.scale(self.originalSurface, (50, 50))
        self.playerSurface = self.originalSurface
        self.playerRect = self.playerSurface.get_rect()
        self.initialX = (self.mainSurface.get_width() / 2) + 100
        self.initialY = (self.mainSurface.get_height() - (self.mainSurface.get_height() / 3)) - 44
        self.playerRect.x = self.initialX
        self.playerRect.y = self.initialY
        self.speed = 10
        self.holdingSword = True
        self.holdingGun = False
        self.game = game
        self.gun = None
        self.sword = Sword(self.mainSurface, self, self.game.enemy, self.game.enemyList, game.updateList, self.game)
        self.game.addToUpdates(self.sword)
        
    def attack(self):
        if self.holdingSword:
            self.sword.attack()
        elif self.holdingGun:
            self.gun.attack()
    
    def setSword(self):
        self.game.updateList.addToMainList(self.sword)
    
    def setGun(self, gun):
        self.gun = gun
        self.game.addToUpdates(self.gun)
         
    def update(self):
        if self.terrain.movingRight == True:
            self.playerSurface = pygame.transform.flip(self.originalSurface, True, False)
        elif self.terrain.movingLeft == True:
            self.playerSurface = self.originalSurface
        self.mainSurface.blit(self.playerSurface, self.playerRect)
        
    def toSword(self):
        self.holdingSword = True
        self.holdingGun = False
        
    def toGun(self):
        self.holdingSword = False
        self.holdingGun = True
    
class Menu():
    def __init__(self):
        self.screenSize = (0, 0)       
        self.screen = pygame.display.set_mode(self.screenSize, pygame.FULLSCREEN)
        self.mainSurface = pygame.display.get_surface()
        
        self.backgroundSurface = pygame.image.load("Menu\\007.png").convert_alpha()
        self.titleSurface = pygame.image.load("Menu\\Title.png").convert_alpha()
        self.frameSurface = pygame.image.load("Menu\\frame.png").convert_alpha()
        self.playButtonSurface = pygame.image.load("Menu\\play.png").convert_alpha()
        self.quitSurface = pygame.image.load("Menu\\quit.png").convert_alpha()
        
        self.backgroundRect = self.backgroundSurface.get_rect()
        self.playButtonRect = self.playButtonSurface.get_rect()
        self.quitRect = self.quitSurface.get_rect()
        
        self.playGame = False
        self.mainSurface.blit(self.backgroundSurface, self.backgroundRect)
        self.frame = Frame(self.mainSurface, self.frameSurface, self.playButtonSurface, self.titleSurface, self.quitSurface)

        centerX = (self.mainSurface.get_width() // 2) - (self.mainSurface.get_height() / 4)

        self.playButtonRect.x = centerX + 55
        self.playButtonRect.y = 325
        
        self.quitRect.x = centerX + 55
        self.quitRect.y = 475
        
        pygame.display.update()
    
    def main(self):
        pygame.mixer.music.load("audio//Menu music.ogg")
        pygame.mixer.music.play(-1)
        while self.playGame == False:
            self.checkInputMenu()    
            if self.playGame == True:
                game = Game()
                game.main()
            pygame.display.update()
    
    def checkInputMenu(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.playButtonRect.collidepoint(mouse) == True:
                    self.playGame = True
                if self.quitRect.collidepoint(mouse) == True:
                    pygame.display.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        sys.exit()
    
class Frame():
    def __init__(self, mainSurface, frameSurface, playButtonSurface, titleSurface, quitSurface):
        self.titleSurface = titleSurface
        self.frameSurface = frameSurface
        self.playButtonSurface = playButtonSurface
        self.quitSurface = quitSurface
        self.mainSurface = mainSurface
        self.playButtonRect = self.playButtonSurface.get_rect()
        
        centerX = (self.mainSurface.get_width() // 2) - (self.mainSurface.get_height() / 4) - 40
        
        self.frameSurface.blit(self.playButtonSurface, (55, 40))
        self.frameSurface.blit(self.quitSurface, (55, 200))
        self.mainSurface.blit(self.frameSurface, (centerX, 275))
        self.mainSurface.blit(self.titleSurface, ((centerX - 100), 45))

if __name__ == "__main__":
    menu = Menu()
    menu.main()