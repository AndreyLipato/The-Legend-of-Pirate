from random import choices
import pygame
from functions import rectPointIntersection
from game.animator import Animator, AnimatorData
from game.entity import Entity, EntityAlive, EntityGroups
from game.saveData import SaveData
from settings import Settings


animatorData = AnimatorData("pirate", [
    ("stayS.png", 0, (12, 24), (0, -0.8, 0.75, 1.5)),
    ("stayW.png", 0, (12, 24), (0, -0.8, 0.75, 1.5)),
    ("stayA.png", 0, (12, 18), (-0.15, -0.8, 1, 1.5)),
    ("stayD.png", 0, (12, 18), (-0.05, -0.8, 1, 1.5)),
    ("goingS.png", 150, (12, 24), (0, -0.8, 0.75, 1.5)),
    ("goingW.png", 150, (12, 24), (0, -0.8, 0.75, 1.5)),
    ("goingA.png", 150, (12, 18), (-0.15, -0.8, 1, 1.5)),
    ("goingD.png", 150, (12, 18), (-0.05, -0.8, 1, 1.5)),
    ("attackS.png", 100, (12, 32), (0, -0.8, 0.75, 2)),
    ("attackW.png", 100, (12, 29), (0, -1.1, 0.75, 1.8)),
    ("attackA.png", 100, (21, 18), (-0.9, -0.8, 1.75, 1.5)),
    ("attackD.png", 100, (21, 18), (0, -0.8, 1.75, 1.5)),
    ("attack_swimS.png", 100, (18, 32), (-0.17, -0.9, 1.125, 2)),
    ("attack_swimW.png", 100, (18, 29), (-0.17, -1.1, 1.125, 1.8)),
    ("attack_swimA.png", 100, (21, 20), (-0.67, -0.9, 1.743, 1.66)),
    ("attack_swimD.png", 100, (20, 20), (-0.27, -0.9, 1.66, 1.66)),
    ("dig.png", 200, (21, 18), (0, -0.8, 1.75, 1.5)),
    ("swimW.png", 0, (18, 24), (-0.17, -0.8, 1.125, 1.5)),
    ("swimS.png", 0, (18, 24), (-0.17, -0.8, 1.125, 1.5)),
    ("swimA.png", 0, (16, 18), (-0.27, -0.8, 1.33, 1.5)),
    ("swimD.png", 0, (16, 18), (-0.27, -0.8, 1.33, 1.5)),
    # ("swimingW.png", 150, (16, 24), (-0.1, -0.9, 1, 1.5)),
    # ("swimingS.png", 150, (16, 24), (-0.1, -0.9, 1, 1.5)),
    ("swimmingW.png", 150, (18, 24), (-0.17, -0.8, 1.125, 1.5)),
    ("swimmingS.png", 150, (18, 24), (-0.17, -0.8, 1.125, 1.5)),
    ("swimmingA.png", 150, (16, 18), (-0.27, -0.8, 1.33, 1.5)),
    ("swimmingD.png", 150, (16, 18), (-0.27, -0.8, 1.33, 1.5)),
])


class EntityPlayer(EntityAlive):
    def __init__(self, saveData: SaveData):
        super().__init__(None)
        self.saveData = saveData
        self.buttonPressed = []
        # нажаты ли кнопки движения в направлениях: вверх, вправо, вниз, влево (для корректного изменения направления движения)
        self.health = saveData.health
        self.healthMax = 6
        self.group = EntityGroups.playerSelf
        self.weapon: Entity = None
        self.message = ""
        self.speed = 0.07
        self.width = 0.75
        self.height = 0.7
        self.imagePos = (0, -0.5)
        self.x = saveData.checkPointX + (1 - self.width) / 2
        self.y = saveData.checkPointY + (1 - self.height) / 2
        self.animator = Animator(animatorData, "stayS")
        self.direction = "S"
        self.shovel = None
        self.state = "normal"
        self.action = None
        self.DamageDelay = Settings.damageDelayPlayer
        self.animator.DamageDelay = Settings.damageDelayPlayer
        self.animator.damageAnimCount = 4
        self.lastAttaker = ""

    def onKeyDown(self, key):
        if (key == pygame.K_w or key == pygame.K_UP):
            self.buttonPressed.append("up")
        if (key == pygame.K_s or key == pygame.K_DOWN):
            self.buttonPressed.append("down")
        if (key == pygame.K_d or key == pygame.K_RIGHT):
            self.buttonPressed.append("right")
        if (key == pygame.K_a or key == pygame.K_LEFT):
            self.buttonPressed.append("left")
        if (key == pygame.K_SPACE):
            self.attack()
        if (key == pygame.K_e):
            if (self.action):
                self.action()
            else:
                self.dig()

        if (Settings.moveScreenOnNumpad):
            if (key == pygame.K_KP_4):
                self.screen.tryGoTo("left")
            if (key == pygame.K_KP_8):
                self.screen.tryGoTo("up")
            if (key == pygame.K_KP_6):
                self.screen.tryGoTo("right")
            if (key == pygame.K_KP_2):
                self.screen.tryGoTo("down")

    def onKeyUp(self, key):
        if (key == pygame.K_w or key == pygame.K_UP):
            while "up" in self.buttonPressed:
                self.buttonPressed.remove("up")
        if (key == pygame.K_s or key == pygame.K_DOWN):
            while "down" in self.buttonPressed:
                self.buttonPressed.remove("down")
        if (key == pygame.K_d or key == pygame.K_RIGHT):
            while "right" in self.buttonPressed:
                self.buttonPressed.remove("right")
        if (key == pygame.K_a or key == pygame.K_LEFT):
            while "left" in self.buttonPressed:
                self.buttonPressed.remove("left")

    def onJoyHat(self, value):
        if (value[1] > 0):
            while "down" in self.buttonPressed:
                self.buttonPressed.remove("down")
            self.buttonPressed.append("up")
        elif (value[1] < 0):
            while "up" in self.buttonPressed:
                self.buttonPressed.remove("up")
            self.buttonPressed.append("down")
        else:
            while "up" in self.buttonPressed:
                self.buttonPressed.remove("up")
            while "down" in self.buttonPressed:
                self.buttonPressed.remove("down")
        if (value[0] > 0):
            while "left" in self.buttonPressed:
                self.buttonPressed.remove("left")
            self.buttonPressed.append("right")
        elif (value[0] < 0):
            while "right" in self.buttonPressed:
                self.buttonPressed.remove("right")
            self.buttonPressed.append("left")
        else:
            while "right" in self.buttonPressed:
                self.buttonPressed.remove("right")
            while "left" in self.buttonPressed:
                self.buttonPressed.remove("left")

    def onJoyAxis(self, axis, value):
        if (axis == 0):
            if (value > 0.5):
                while "left" in self.buttonPressed:
                    self.buttonPressed.remove("left")
                self.buttonPressed.append("right")
            elif (value < -0.5):
                while "right" in self.buttonPressed:
                    self.buttonPressed.remove("right")
                self.buttonPressed.append("left")
            else:
                while "right" in self.buttonPressed:
                    self.buttonPressed.remove("right")
                while "left" in self.buttonPressed:
                    self.buttonPressed.remove("left")
        elif (axis == 1):
            if (value > 0.5):
                while "up" in self.buttonPressed:
                    self.buttonPressed.remove("up")
                self.buttonPressed.append("down")
            elif (value < -0.5):
                while "down" in self.buttonPressed:
                    self.buttonPressed.remove("down")
                self.buttonPressed.append("up")
            else:
                while "up" in self.buttonPressed:
                    self.buttonPressed.remove("up")
                while "down" in self.buttonPressed:
                    self.buttonPressed.remove("down")
        elif (axis == 2):
            if (value > 0.5):
                self.attack("D")
            elif (value < -0.5):
                self.attack("A")
        elif (axis == 3):
            if (value > 0.5):
                self.attack("S")
            elif (value < -0.5):
                self.attack("W")

    def onJoyButonDown(self, button):
        if (button == 2):
            self.attack()
        if (button == 1):
            if (self.action):
                self.action()
            else:
                self.dig()

    def onJoyButonUp(self, button):
        pass

    def setSpeed(self):
        self.speedX = 0
        self.speedY = 0
        if (self.state != "normal" and self.state != "swim" and self.state != "dig"):
            return
        if (len(self.buttonPressed) > 0):
            if (self.state == "dig"):
                self.state = "normal"
            if (self.buttonPressed[-1] == "up"):
                self.speedY = -self.speed
                self.direction = "W"
            if (self.buttonPressed[-1] == "down"):
                self.speedY = self.speed
                self.direction = "S"
            if (self.buttonPressed[-1] == "right"):
                self.speedX = self.speed
                self.direction = "D"
            if (self.buttonPressed[-1] == "left"):
                self.speedX = -self.speed
                self.direction = "A"

    def attack(self, d=None):
        if (self.state != "normal" and self.state != "swim"):
            return
        if (d is not None):
            self.direction = d
        if (self.state == "swim"):
            self.state = "attack_swim"
        else:
            self.state = "attack"
        self.shovel = Entity.createById("shovel", self.screen)
        self.screen.addEntity(self.shovel)
        self.shovel.startX = self.x
        self.shovel.startY = self.y
        self.shovel.direction = self.direction
        self.shovel.nextStage()

    def dig(self):
        if (self.state != "normal"):
            return
        tile = self.get_tile(1, pos=(0.5, 0.7))
        if (tile.digable):
            self.state = "dig"

    def afterDig(self):
        entities = self.get_entitiesD((1.1, 0.4, 0.4, 0.3))
        dig_place = None
        for e in entities:
            if e.id == "dig_place":
                dig_place = e
                break
        if (dig_place and not dig_place.digged):
            dig_place.dig()
            found = choices(["coin", "heart", "crab"], [0.5, 0.4, 0.1])[0]
            if (found == "coin"):
                coin = Entity.createById("coin", self.screen)
                self.screen.addEntity(coin)
                coin.x = self.x + 1.25
                coin.y = self.y + 0.5
            elif (found == "heart"):
                heart = Entity.createById("heart", self.screen)
                self.screen.addEntity(heart)
                heart.x = self.x + 1.25
                heart.y = self.y + 0.2
            elif (found == "crab"):
                crab = Entity.createById("crab", self.screen)
                self.screen.addEntity(crab)
                crab.x = self.x + 1.25
                crab.y = self.y + 0.25

    def update(self):
        self.setSpeed()
        super().update()

        if (self.state == "dig"):
            self.animator.setAnimation("dig")
            if (self.animator.lastState[1]):
                self.afterDig()
                self.state = "normal"
        elif (self.state == "attack" or self.state == "attack_swim"):
            if (self.shovel is not None):
                self.animator.setAnimation(self.state + self.direction)
                if (self.animator.lastState[1]):
                    self.shovel.remove()
                    self.shovel = None
                    self.state = "normal"
                elif (self.animator.lastState[0]):
                    self.shovel.nextStage()
        else:
            tile = self.get_tile(pos=(0.5, 0.7))
            swim = False
            if (tile and "water" in tile.tags):
                x, y = self.x + self.width * 0.5, self.y + self.height * 0.7
                zone = [int(x), int(y), 1, 1]
                if ("water-t" in tile.tags):
                    zone[1] += 0.4
                    zone[3] -= 0.4
                if ("water-b" in tile.tags):
                    zone[3] -= 0.4
                if ("water-l" in tile.tags):
                    zone[0] += 0.4
                    zone[2] -= 0.4
                if ("water-r" in tile.tags):
                    zone[2] -= 0.4
                swim = rectPointIntersection(zone, (x, y))
            if (swim):
                self.state = "swim"
                anim = "swim" if self.speedX == 0 and self.speedY == 0 else "swimming"
                self.animator.setAnimation(anim + self.direction)
            else:
                self.state = "normal"
                anim = "stay" if self.speedX == 0 and self.speedY == 0 else "going"
                self.animator.setAnimation(anim + self.direction)

        if (self.x <= 0.05):
            if (self.screen.tryGoTo("left")):
                self.x = Settings.screen_width - self.width - 0.1
        elif (self.x + self.width >= Settings.screen_width - 0.05):
            if (self.screen.tryGoTo("right")):
                self.x = 0.1
        elif (self.y <= 0.05):
            if (self.screen.tryGoTo("up")):
                self.y = Settings.screen_height - self.height - 0.1
        elif (self.y + self.height >= Settings.screen_height - 0.05):
            if (self.screen.tryGoTo("down")):
                self.y = 0.1

        # self.animator.setAnimation("attack_swimS")

    def preUpdate(self):
        self.message = ""
        self.action = None

    def takeDamage(self, damage: int, attacker: Entity = None):
        if (super().takeDamage(damage, attacker)):
            self.lastAttaker = attacker.id
