import pyglet
import engine

yGravity = 1
platformBoxList = []
screenWidth = 640
screenHeight = 480

class Box:
    def __init__(self):
        self.xPosition = 0
        self.yPosition = 0
        self.height = 1
        self.width = 1

class Input:
    up = False
    down = False
    left = False
    right = False
    a = False
    b = False

class Camera:
    def __init__(self):
        self.box = Box()
        self.width = screenWidth
        self.height = screenHeight
        self.zoom = 1.75
        self.toZoom = 1.75
        self.x = screenWidth/2
        self.y = screenHeight/4

    def update(self):
        player1_xPosition = engine.player1.player.box.xPosition + engine.player1.player.box.width/2
        player2_xPosition = engine.player2.box.xPosition + engine.player2.box.width/2
        player1_yPosition = engine.player1.player.box.yPosition + engine.player1.player.box.height/2
        player2_yPosition = engine.player2.box.yPosition + engine.player2.box.height/2

        xDistance = screenWidth/(abs(player1_xPosition - player2_xPosition) + screenWidth/2)
        yDistance = screenHeight/(abs(player1_yPosition - player2_yPosition) + screenHeight/2)

        if player1_xPosition < player2_xPosition:
            self.box.xPosition = player1_xPosition - screenWidth/8
        else:
            self.box.xPosition = player2_xPosition - screenWidth/8

        if player1_yPosition < player2_yPosition:
            self.box.yPosition = player1_yPosition - screenHeight/4
        else:
            self.box.yPosition = player2_yPosition - screenHeight/4

        if xDistance < yDistance:
            self.zoom = xDistance
        else:
            self.zoom = yDistance

        if self.box.xPosition < 0:
            self.box.xPosition = 0

        if self.box.yPosition < 0:
            self.box.yPosition = 0
        if self.zoom < 1:
            self.zoom = 1
        elif self.zoom > 1.6:
            self.zoom = 1.6

        if screenHeight / self.zoom + self.box.yPosition - ((self.zoom - 1)**2) * 212 > screenHeight:
            self.box.yPosition = screenHeight - screenHeight/self.zoom + ((self.zoom - 1)**2)*212

        if screenWidth / self.zoom + self.box.xPosition - ((self.zoom - 1)**2) * 400 > screenWidth:
            self.box.xPosition = screenWidth - screenWidth/self.zoom + ((self.zoom - 1) ** 2) * 400

        self.x = self.x + (self.box.xPosition - self.x)/10
        self.y = self.y + (self.box.yPosition - self.y)/10
        self.toZoom = self.toZoom + (self.zoom - self.toZoom)/10

class Player:
    def __init__(self, xPosition, yPosition):
        self.input = Input()
        self.box = Box()
        self.xVelocity = 0
        self.yVelocity = 0
        self.xFriction = 2
        self.acceleration = 3
        self.grabTimer = 0
        self.isGrounded = False
        self.isGrabbing = False
        self.releasedGrab = False
        self.canGrab = True
        self.releasedJump = True
        self.canDoubleJump = True
        self.groundedPlatform = None

        player_stream = pyglet.image.load('box.png', file=open('test_platform.png', 'rb'))
        self.sprite = pyglet.sprite.Sprite(player_stream, x=self.box.xPosition, y=self.box.yPosition)

        self.xScale = .025
        self.yScale = .5
        self.box.width = self.sprite.width * self.xScale
        self.box.height = self.sprite.height * self.yScale
        self.box.xPosition = xPosition
        self.box.yPosition = yPosition

    def update(self):
        self.platformInteraction()

        if self.input.up:
            if self.releasedJump:
                self.jump()
                self.isGrounded = False
                if self.isGrabbing:
                    self.isGrabbing = False
                    self.canGrab = False
                    self.releasedGrab = True
                    self.grabTimer = 0
        if self.input.down:
            if self.isGrabbing:
                self.isGrounded = False
                self.isGrabbing = False
                self.canGrab = False
                self.releasedGrab = True
                self.grabTimer = 0

        if self.input.right:
            self.xVelocity += self.acceleration
        if self.input.left:
            self.xVelocity -= self.acceleration

        if self.isGrounded:
            self.yVelocity = 0
        else:
            self.yVelocity -= yGravity

        if not self.isGrabbing:
            self.box.xPosition += self.xVelocity
            self.box.yPosition += self.yVelocity

        if -1 > self.xVelocity or self.xVelocity > 1:
            self.xVelocity /= self.xFriction
        elif -1 <= self.xVelocity <= 1:
            self.xVelocity = 0

        self.sprite.update(x=self.box.xPosition, y=self.box.yPosition, scale_x=self.xScale, scale_y=self.yScale)

    def jump(self):
        self.releasedJump = False
        self.yVelocity = 10

    def platformInteraction(self):
        if self.releasedGrab:
            self.grabTimer += 1
            if self.grabTimer == 10:
                self.canGrab = True
                self.releasedGrab = False

        if self.isGrounded:
            if not (self.box.yPosition - 5 < self.groundedPlatform.box.yPosition + self.groundedPlatform.box.height < self.box.yPosition + 20 and
                    self.box.xPosition + self.box.width > self.groundedPlatform.box.xPosition and
                    self.box.xPosition < self.groundedPlatform.box.xPosition + self.groundedPlatform.box.width):
                self.isGrounded = False
        else:
            for platform in platformBoxList:
                if self.box.yPosition - 5 < platform.box.yPosition + platform.box.height < self.box.yPosition + 5 and \
                        self.box.xPosition + self.box.width > platform.box.xPosition and \
                        self.box.xPosition < platform.box.xPosition + platform.box.width:
                    self.isGrounded = True
                    self.box.yPosition = platform.box.yPosition + platform.box.height
                    self.groundedPlatform = platform
                elif self.box.yPosition + 5 < platform.box.yPosition + platform.box.height < self.box.yPosition + 50:
                    if platform.box.xPosition + 10 > self.box.xPosition + self.box.width > platform.box.xPosition:
                        if self.canGrab:
                            self.isGrounded = True
                            self.isGrabbing = True
                            self.box.xPosition = platform.box.xPosition - 20
                            self.box.yPosition = platform.box.yPosition + platform.box.height - 35

                    elif platform.box.xPosition + platform.box.width > self.box.xPosition > platform.box.xPosition + platform.box.width - 10:
                        if self.canGrab:
                            self.isGrounded = True
                            self.isGrabbing = True
                            self.box.xPosition = platform.box.xPosition + platform.box.width
                            self.box.yPosition = platform.box.yPosition + platform.box.height - 35

                    elif self.box.xPosition + self.box.width > platform.box.xPosition and \
                            self.box.xPosition < platform.box.xPosition + platform.box.width:
                        self.isGrounded = True
                        self.box.yPosition = platform.box.yPosition + platform.box.height
                        self.groundedPlatform = platform

                elif platform.box.yPosition < self.box.yPosition < platform.box.yPosition + platform.box.height:
                    if platform.box.xPosition + platform.box.width > self.box.xPosition > platform.box.xPosition + platform.box.width - 20:
                        self.box.xPosition = platform.box.xPosition + platform.box.width

                    elif platform.box.xPosition + 20 > self.box.xPosition + self.box.width > platform.box.xPosition:
                        self.box.xPosition = platform.box.xPosition - self.box.width

class Platform:
    def __init__(self, xPosition, yPosition, xScale, yScale):
        self.box = Box()

        self.box.xPosition = xPosition
        self.box.yPosition = yPosition

        self.platform_stream = pyglet.image.load('white_box.png', file=open('white_box.png', 'rb'))
        self.sprite = pyglet.sprite.Sprite(self.platform_stream, x=self.box.xPosition, y=self.box.yPosition)
        self.xScale = xScale
        self.yScale = yScale
        self.box.height = self.sprite.height * self.yScale
        self.box.width = self.sprite.width * self.xScale

        self.sprite.update(x=self.box.xPosition, y=self.box.yPosition, scale_x=self.xScale, scale_y=self.yScale)

        platformBoxList.append(self)

class Kirby:
    def __init__(self, xPosition, yPosition):
        self.player = Player(xPosition, yPosition)

    def update(self):
        self.player.update()

        #if self.player.input.right:


    #def run(self):

