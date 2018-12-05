import pyglet
import engine
import math
from threading import Timer
yGravity = .2
platformBoxList = []
screenWidth = 640
screenHeight = 480

class Box:
    """Contains the coordinates and dimensions of the sprite box"""
    def __init__(self,xPosition, yPosition, width, height):
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.height = height
        self.width = width
        self.xCenter = xPosition + (width/2)
        self.yCenter = yPosition + (height/2)

class Hitbox:
    """Box that causes damage"""
    def __init__(self, xRel, yRel, width, height, delay, damage, knockback, angle, player, opponent, duration):
        self.xRel = xRel
        self.yRel = yRel
        self.player = player
        self.opponent = opponent

        self.width = width
        self.height = height
        self.xPosition = (self.player.box.xCenter + self.xRel * self.player.direction) - self.width / 2
        self.yPosition = (self.player.box.yCenter + self.yRel) - self.height / 2
        self.platform_stream = pyglet.image.load('red_box.png', file=open('red_box.png', 'rb'))
        self.sprite = pyglet.sprite.Sprite(self.platform_stream, x=self.xPosition, y=self.yPosition)

        self.duration = duration
        self.damage = damage
        self.angle = angle
        self.knockback = knockback

        Timer(delay/30, self.awake).start()

    def awake(self):
        engine.hitboxes.append(self)
        self.player.hitboxes.append(self)
        self.activate()

    def activate(self):
        self.xPosition = (self.player.box.xCenter + self.xRel * self.player.direction) - self.width/2
        self.yPosition = (self.player.box.yCenter + self.yRel) - self.height/2
        self.sprite.update(x=self.xPosition, y=self.yPosition, scale_x=self.width/self.sprite.width, scale_y=self.height/self.sprite.height)

        if ((self.xPosition < self.opponent.box.xPosition < self.xPosition + self.width or self.xPosition < self.opponent.box.xPosition +
             self.opponent.box.width < self.xPosition + self.width) and (self.yPosition < self.opponent.box.yPosition < self.yPosition + self.height or
                self.yPosition < self.opponent.box.yPosition + self.opponent.box.height < self.yPosition + self.height)) or \
                ((self.opponent.box.xPosition < self.xPosition < self.opponent.box.xPosition + self.opponent.box.width or
                  self.opponent.box.xPosition < self.xPosition + self.width < self.opponent.box.xPosition + self.opponent.box.width) and
                 (self.opponent.box.yPosition < self.yPosition < self.opponent.box.yPosition + self.opponent.box.height or
                  self.opponent.box.yPosition < self.yPosition + self.height < self.opponent.box.yPosition + self.opponent.box.height)):
            if self.opponent.canBeHit:
                self.opponent.resetAerial()
                self.opponent.canBeHit = False
                self.opponent.isGrounded = False
                self.opponent.canMove = False
                self.opponent.canAttack = False
                self.opponent.canGrab = False
                self.opponent.isGrabbing = False
                self.opponent.jumpCounter = 0
                if self.opponent.isRock:
                    self.opponent.isRock = False
                self.opponent.damage += self.damage
                self.opponent.yVelocity = math.sin(math.radians(self.angle)) * self.knockback * (200 + self.opponent.damage)/200
                self.opponent.xVelocity = math.cos(math.radians(self.angle)) * self.knockback * (100 + self.opponent.damage)/100 * self.player.direction
                self.opponent.xFriction = 1
                if self.damage / 20 < .15:
                    time = .15
                else:
                    time = self.damage / 20
                Timer(time, self.returnFriction).start()
                engine.playhurtsound()
                #   self.opponent.goHurtSprite()
                #   ^Removed because it keeps crashing the game

    def returnFriction(self):
        self.opponent.xFriction = 1.75
        self.opponent.canMove = True
        self.opponent.canAttack = True
        self.opponent.canGrab = True
        self.opponent.canBeHit = True

    def update(self):
        self.activate()
        if self.duration > 0:
            self.duration -= 1
        else:
            self.player.hitboxes.remove(self)
            engine.hitboxes.remove(self)

class GameTimer:
    def __init__(self, minutes):
        self.minutes = minutes
        self.seconds = 0
        self.miliseconds = 0
        self.label = pyglet.text.Label(str(minutes) + ":00:000")
        self.label.font_size = 24
        self.label.x = 270
        self.label.y = 240
        self.label.color = (0, 0, 0, 195)

    def update(self):
        if engine.runTimer:
            self.miliseconds -= (100/35)
            if self.miliseconds < 0:
                self.miliseconds += 100
                self.seconds -= 1
            if self.seconds < 0 and self.minutes != 0:
                self.seconds += 60
                self.minutes -= 1
            if self.seconds < 10:
                seconds = "0" + str(self.seconds)
            else:
                seconds = self.seconds
            if self.miliseconds < 10:
                milliseconds = "0" + str(int(self.miliseconds))
            else:
                milliseconds = int(self.miliseconds)
            self.label.text = "%s:%s:%s" % (self.minutes, seconds, milliseconds)
            if self.seconds < 0 and self.minutes <= 0:
                if engine.player1.score == engine.player2.score:
                    self.label.text = "Draw!"
                    self.label.x += 13
                elif engine.player1.score > engine.player2.score:
                    self.label.text = "Player 1 Wins!!"
                    self.label.x -= 55
                    engine.statsDict["player1wins"] += 1
                else:
                    self.label.text = "Player 2 Wins!!"
                    self.label.x -= 55
                    engine.statsDict["player2wins"] += 1
                engine.statsDict["player1totalpoints"] += engine.player1.score
                engine.statsDict["player2totalpoints"] += engine.player2.score
                engine.saveStats()
                engine.runTimer = False
                engine.camera.reset()
                Timer(7, self.resetGame).start()

    def draw(self):
        self.label.draw()

    def resetGame(self):
        engine.endGame()

class Scores:
    def __init__(self, player):
        self.player = player
        self.label = pyglet.text.Label(str(self.player.score))
        self.label.font_size = 20
        if player == engine.player1:
            self.label.x = 273
            self.label.y = 200
            self.label.color = (255, 0, 0, 230)
        elif player == engine.player2:
            self.label.x = 360
            self.label.y = 200
            self.label.color = (0, 0, 255, 230)

    def update(self):
        self.label.text = str(self.player.score)

    def draw(self):
        self.label.draw()
class DamageMeter:
    def __init__(self, player):
        self.label = pyglet.text.Label(str(player.damage) + "%")
        self.label.text = "0%"
        self.player = player
        self.label.bold = True
        if player == engine.player1:
            self.label.color = (255, 0, 0, 255)
        elif player == engine.player2:
            self.label.color = (0, 0, 255, 255)

    def update(self):
        self.label.x = self.player.box.xPosition
        self.label.y = self.player.box.yPosition + self.player.box.height + 5
        self.label.text = "0%"
        self.label.text = str(int(self.player.damage)) + "%"

    def draw(self):
        self.label.draw()
class Input:
    """Contains booleans for each player command"""
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.a = False
        self.b = False
        self.j = False

        self.releaseUp = True
        self.releaseDown = True
        self.releaseLeft = True
        self.releaseRight = True
        self.releaseA = True
        self.releaseB = True
        self.releaseJ = True

class Camera:
    """Camera that follows both players"""
    def __init__(self):
        self.box = Box(screenWidth/2, screenHeight/4, screenWidth, screenHeight)
        self.zoom = 1.75
        self.toZoom = 1.75

        self.width = screenWidth
        self.height = screenHeight

        self.x = screenWidth/2
        self.y = screenHeight/4
        self.followPlayers = True

    def update(self):
        if self.followPlayers:
            #   Get the position on the center of each player
            player1_xPosition = engine.player1.box.xPosition + engine.player1.box.width/2
            player2_xPosition = engine.player2.box.xPosition + engine.player2.box.width/2
            player1_yPosition = engine.player1.box.yPosition + engine.player1.box.height/2
            player2_yPosition = engine.player2.box.yPosition + engine.player2.box.height/2

            #   Finds the position of the camera on the center of the two players
            #   and divides it to screen width and height to find the zoom value
            xDistance = screenWidth/(abs(player1_xPosition - player2_xPosition) + screenWidth/2)
            yDistance = screenHeight/(abs(player1_yPosition - player2_yPosition) + screenHeight/2)

            #   Use bottom and leftmost player as the camera position basis
            if player1_xPosition < player2_xPosition:
                self.box.xPosition = player1_xPosition - screenWidth/8
            else:
                self.box.xPosition = player2_xPosition - screenWidth/8
            if player1_yPosition < player2_yPosition:
                self.box.yPosition = player1_yPosition - screenHeight/4
            else:
                self.box.yPosition = player2_yPosition - screenHeight/4

            #   If the vertical difference is greater than horizontal, use that as the basis on how far the camera
            #   should zoom out and vice versa
            if xDistance < yDistance:
                self.zoom = xDistance
            else:
                self.zoom = yDistance

            #   The camera position cannot go lower than 0 on the x and y axis
            if self.box.xPosition < 0:
                self.box.xPosition = 0
            if self.box.yPosition < 0:
                self.box.yPosition = 0
            if self.zoom < 1:
                self.zoom = 1
            elif self.zoom > 1.6:
                self.zoom = 1.6

            #   If the camera will exceed the bounds of the background on the right or up, adjust the x and y positions
            #   so that the zoom is near perfect to the edge
            if screenHeight / self.zoom + self.box.yPosition - ((self.zoom - 1)**2) * 212 > screenHeight:
                self.box.yPosition = screenHeight - screenHeight/self.zoom + ((self.zoom - 1)**2)*212
            if screenWidth / self.zoom + self.box.xPosition - ((self.zoom - 1)**2) * 400 > screenWidth:
                self.box.xPosition = screenWidth - screenWidth/self.zoom + ((self.zoom - 1) ** 2) * 400

            #   Making the camera movement and zooming smoother
            self.x = self.x + (self.box.xPosition - self.x)/10
            self.y = self.y + (self.box.yPosition - self.y)/10
            self.toZoom = self.toZoom + (self.zoom - self.toZoom)/10

    def reset(self):
        self.followPlayers = False
        self.x = 0
        self.y = 0
        self.toZoom = 1

class Platform:
    def __init__(self, xPosition, yPosition, xScale, yScale):
        self.platform_stream = pyglet.image.load('white_box.png', file=open('white_box.png', 'rb'))
        self.sprite = pyglet.sprite.Sprite(self.platform_stream, x=xPosition, y=yPosition)
        self.xScale = xScale
        self.yScale = yScale
        self.box = Box(xPosition, yPosition, self.sprite.width * self.xScale, self.sprite.height * self.yScale)

        self.sprite.update(x=self.box.xPosition, y=self.box.yPosition, scale_x=self.xScale, scale_y=self.yScale)

        platformBoxList.append(self)

    def draw(self):
        self.sprite.draw()

class Stage:
    def __init__(self, background, bgx, bgy, scale):
        self.background = background
        self.bgsprite= pyglet.sprite.Sprite(background, x=0, y=0)
        self.bgx = bgx
        self.bgy = bgy
        self.scale = scale

    def draw(self):
        self.bgsprite.draw()