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
                self.opponent.isGrounded = False
                self.opponent.canMove = False
                self.opponent.canAttack = False
                self.opponent.canGrab = False
                self.opponent.isGrabbing = False
                self.opponent.damage += self.damage
                self.opponent.yVelocity = math.sin(math.radians(self.angle)) * self.knockback * (200 + self.opponent.damage)/200
                self.opponent.xVelocity = math.cos(math.radians(self.angle)) * self.knockback * (100 + self.opponent.damage)/100 * self.player.direction
                print(self.opponent.damage)
                self.opponent.xFriction = 1
                if self.damage / 20 < .15:
                    time = .15
                else:
                    time = self.damage / 20
                Timer(time, self.returnFriction).start()
                Timer(0.1, self.allowHit).start()
                self.opponent.goHurtSprite()
                self.opponent.canBeHit = False

    def returnFriction(self):
        self.opponent.xFriction = 1.75
        self.opponent.canMove = True
        self.opponent.canAttack = True
        self.opponent.canGrab = True

    def allowHit(self):
        self.opponent.canBeHit = True

    def update(self):
        #self.activate()
        if self.duration > 0:
            self.duration -= 1
        else:
            self.player.hitboxes.remove(self)
            engine.hitboxes.remove(self)

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

    def update(self):
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


class Platform:
    def __init__(self, xPosition, yPosition, xScale, yScale):
        self.platform_stream = pyglet.image.load('white_box.png', file=open('white_box.png', 'rb'))
        self.sprite = pyglet.sprite.Sprite(self.platform_stream, x=xPosition, y=yPosition)
        self.xScale = xScale
        self.yScale = yScale
        self.box = Box(xPosition, yPosition, self.sprite.width * self.xScale, self.sprite.height * self.yScale)

        self.sprite.update(x=self.box.xPosition, y=self.box.yPosition, scale_x=self.xScale, scale_y=self.yScale)

        platformBoxList.append(self)
