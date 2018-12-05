import pyglet
import engine
import objects
import random
from threading import Timer
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

spriteDictionary = {"idle": [pyglet.resource.image("idle.png", flip_x=False)],
                    "idleF": [pyglet.resource.image("idle.png", flip_x=True)],
                    "walk": [(pyglet.resource.image("walk" + str(i) + ".png", flip_x=False)) for i in range(1, 13)],
                    "walkF": [(pyglet.resource.image("walk" + str(i) + ".png", flip_x=True)) for i in range(1, 13)],
                    "jump": [(pyglet.resource.image("jump" + str(i) + ".png", flip_x=False)) for i in range(1, 9)],
                    "jumpF": [(pyglet.resource.image("jump" + str(i) + ".png", flip_x=True)) for i in range(1, 9)],
                    "multiJump": [(pyglet.resource.image("multi-jump" + str(i) + ".png", flip_x=False)) for i in range(1, 5)],
                    "multiJumpF": [(pyglet.resource.image("multi-jump" + str(i) + ".png", flip_x=True)) for i in range(1, 5)],
                    "noJump": [pyglet.resource.image("multi-jump5.png", flip_x=False)],
                    "noJumpF": [pyglet.resource.image("multi-jump5.png", flip_x=True)],
                    "crouch": [(pyglet.resource.image("crouch" + str(i) + ".png", flip_x=False)) for i in range(1, 2)],
                    "crouchF": [(pyglet.resource.image("crouch" + str(i) + ".png", flip_x=True)) for i in range(1, 2)],
                    "basicAttack1": [(pyglet.resource.image("basicattack-single" + str(i) + ".png", flip_x=False)) for i in range(1, 4)],
                    "basicAttack1F": [(pyglet.resource.image("basicattack-single" + str(i) + ".png", flip_x=True)) for i in range(1, 4)],
                    "basicAttack2": [(pyglet.resource.image("basicattack-double" + str(i) + ".png", flip_x=False)) for i in range(1, 3)],
                    "basicAttack2F": [(pyglet.resource.image("basicattack-double" + str(i) + ".png", flip_x=True)) for i in range(1, 3)],
                    "basicAttack3": [(pyglet.resource.image("rapidpunch" + str(i) + ".png", flip_x=False)) for i in range(1, 6)],
                    "basicAttack3F": [(pyglet.resource.image("rapidpunch" + str(i) + ".png", flip_x=True)) for i in range(1, 6)],
                    "forwardAttack": [(pyglet.resource.image("forwardattack" + str(i) + ".png", flip_x=False)) for i in range(1, 9)],
                    "forwardAttackF": [(pyglet.resource.image("forwardattack" + str(i) + ".png", flip_x=True)) for i in range(1, 9)],
                    "forwardSmashCharge": [(pyglet.resource.image("forwardsmash" + str(i) + ".png", flip_x=False)) for i in range(1, 4)],
                    "forwardSmashChargeF": [(pyglet.resource.image("forwardsmash" + str(i) + ".png", flip_x=True)) for i in range(1, 4)],
                    "forwardSmash": [(pyglet.resource.image("forwardsmash" + str(i) + ".png", flip_x=False)) for i in range(4, 9)],
                    "forwardSmashF": [(pyglet.resource.image("forwardsmash" + str(i) + ".png", flip_x=True)) for i in range(4, 9)],
                    "upwardAttack": [(pyglet.resource.image("upwardattack" + str(i) + ".png", flip_x=False)) for i in range(1, 6)],
                    "upwardAttackF": [(pyglet.resource.image("upwardattack" + str(i) + ".png", flip_x=True)) for i in range(1, 6)],
                    "upwardSmashCharge": [(pyglet.resource.image("upwardsmash" + str(i) + ".png", flip_x=False)) for i in range(1, 4)],
                    "upwardSmashChargeF": [(pyglet.resource.image("upwardsmash" + str(i) + ".png", flip_x=True)) for i in range(1, 4)],
                    "upwardSmash": [(pyglet.resource.image("upwardsmash" + str(i) + ".png", flip_x=False)) for i in range(4, 9)],
                    "upwardSmashF": [(pyglet.resource.image("upwardsmash" + str(i) + ".png", flip_x=True)) for i in range(4, 9)],
                    "downwardAttack": [(pyglet.resource.image("downwardattack" + str(i) + ".png", flip_x=False)) for i in range(1, 5)],
                    "downwardAttackF": [(pyglet.resource.image("downwardattack" + str(i) + ".png", flip_x=True)) for i in range(1, 5)],
                    "downwardSmashCharge": [(pyglet.resource.image("downwardsmash" + str(i) + ".png", flip_x=False)) for i in range(1, 4)],
                    "downwardSmashChargeF": [(pyglet.resource.image("downwardsmash" + str(i) + ".png", flip_x=True)) for i in range(1, 4)],
                    "downwardSmash": [(pyglet.resource.image("downwardsmash" + str(i) + ".png", flip_x=False)) for i in range(4, 13)],
                    "downwardSmashF": [(pyglet.resource.image("downwardsmash" + str(i) + ".png", flip_x=True)) for i in range(4, 13)],
                    "basicAerial": [(pyglet.resource.image("basicaerial" + str(i) + ".png", flip_x=False)) for i in range(1, 9)],
                    "basicAerialF": [(pyglet.resource.image("basicaerial" + str(i) + ".png", flip_x=True)) for i in range(1, 9)],
                    "forwardAerial": [(pyglet.resource.image("forwardaerial" + str(i) + ".png", flip_x=False)) for i in range(1, 9)],
                    "forwardAerialF": [(pyglet.resource.image("forwardaerial" + str(i) + ".png", flip_x=True)) for i in range(1, 9)],
                    "backwardAerial": [(pyglet.resource.image("backwardaerial" + str(i) + ".png", flip_x=False)) for i in range(1, 10)],
                    "backwardAerialF": [(pyglet.resource.image("backwardaerial" + str(i) + ".png", flip_x=True)) for i in range(1, 10)],
                    "upwardAerial": [(pyglet.resource.image("upwardaerial" + str(i) + ".png", flip_x=False)) for i in range(1, 7)],
                    "upwardAerialF": [(pyglet.resource.image("upwardaerial" + str(i) + ".png", flip_x=True)) for i in range(1, 7)],
                    "downwardAerial": [(pyglet.resource.image("downwardaerial" + str(i) + ".png", flip_x=False)) for i in range(1, 12)],
                    "downwardAerialF": [(pyglet.resource.image("downwardaerial" + str(i) + ".png", flip_x=True)) for i in range(1, 12)],
                    "basicSpecial": [(pyglet.resource.image("basicspecial" + str(i) + ".png", flip_x=False)) for i in range(1, 11)],
                    "basicSpecialF": [(pyglet.resource.image("basicspecial" + str(i) + ".png", flip_x=True)) for i in range(1, 11)],
                    "forwardSpecial": [(pyglet.resource.image("forwardspecial" + str(i) + ".png", flip_x=False)) for i in range(1, 12)],
                    "forwardSpecialF": [(pyglet.resource.image("forwardspecial" + str(i) + ".png", flip_x=True)) for i in range(1, 12)],
                    "forwardAerialSpecial": [(pyglet.resource.image("forwardaerialspecial" + str(i) + ".png", flip_x=False)) for i in range(1, 9)],
                    "forwardAerialSpecialF": [(pyglet.resource.image("forwardaerialspecial" + str(i) + ".png", flip_x=True)) for i in range(1, 9)],
                    "upwardSpecial": [(pyglet.resource.image("upwardspecial" + str(i) + ".png", flip_x=False)) for i in range(3, 12)],
                    "upwardSpecialF": [(pyglet.resource.image("upwardspecial" + str(i) + ".png", flip_x=True)) for i in range(3, 12)],
                    "downwardSpecial1": [(pyglet.resource.image("downwardspecial" + str(i) + ".png", flip_x=False)) for i in range(2, 4)],
                    "downwardSpecial2": [(pyglet.resource.image("downwardspecial" + str(i) + ".png", flip_x=False)) for i in range(4, 6)],
                    "downwardSpecial3": [(pyglet.resource.image("downwardspecial" + str(i) + ".png", flip_x=False)) for i in range(6, 8)],
                    "downwardSpecial4": [(pyglet.resource.image("downwardspecial" + str(i) + ".png", flip_x=False)) for i in range(8, 10)],
                    "downwardSpecial5": [(pyglet.resource.image("downwardspecial" + str(i) + ".png", flip_x=False)) for i in range(10, 12)],
                    "downwardSpecial1F": [(pyglet.resource.image("downwardspecial" + str(i) + ".png", flip_x=True)) for i in range(2, 4)],
                    "downwardSpecial2F": [(pyglet.resource.image("downwardspecial" + str(i) + ".png", flip_x=True)) for i in range(4, 6)],
                    "downwardSpecial3F": [(pyglet.resource.image("downwardspecial" + str(i) + ".png", flip_x=True)) for i in range(6, 8)],
                    "downwardSpecial4F": [(pyglet.resource.image("downwardspecial" + str(i) + ".png", flip_x=True)) for i in range(8, 10)],
                    "downwardSpecial5F": [(pyglet.resource.image("downwardspecial" + str(i) + ".png", flip_x=True)) for i in range(10, 12)],
                    "hurt": [(pyglet.resource.image("hurt" + str(i) + ".png", flip_x=False)) for i in range(1, 9)],
                    "hurtF": [(pyglet.resource.image("hurt" + str(i) + ".png", flip_x=True)) for i in range(1, 9)],
                    "ledge": [(pyglet.resource.image("ledge.png", flip_x=False))],
                    "ledgeF": [(pyglet.resource.image("ledge.png", flip_x=True))]
                    }

class Player:
    """All player properties and methods same to all characters"""
    def __init__(self, xPosition, yPosition):
        self.input = objects.Input()
        self.damage = 0
        self.xVelocity = 0
        self.yVelocity = 0
        self.xFriction = 1.75
        self.acceleration = 1.2
        self.direction = 1
        self.jumpCounter = 0
        self.aerialAttacked = 0
        self.aerialSpecialed = 0
        self.isSmashing = False
        self.isGrounded = False
        self.isGrabbing = False
        self.canMove = True
        self.canGrab = True
        self.canAttack = True
        self.groundedPlatform = None
        self.startedCharge = False
        self.smashing = False
        self.attacking = False
        self.special = False
        self.aerial = False
        self.forward = False
        self.backward = False
        self.upward = False
        self.downward = False
        self.canBeHit = True
        self.isUpSpecial = True
        self.cancelUpSpecial = False
        self.isRock = False
        self.regainMomentum = False
        self.isDead = False
        self.basicAttackCounter = 0
        self.smashCounter = 0
        self.hitboxes = []
        self.spritePrefix = ""
        self.orientation = "right"
        self.anim = None
        self.spritexPosition = 0
        self.hurtSprite = pyglet.image.Animation.from_image_sequence(spriteDictionary["hurt"], 1 / 30, False)
        self.hurtSpriteF = pyglet.image.Animation.from_image_sequence(spriteDictionary["hurtF"], 1 / 30, False)
        self.sprites = spriteDictionary["idle"]
        self.anim = pyglet.image.Animation.from_image_sequence(self.sprites, 0.5, True)
        self.sprite = pyglet.sprite.Sprite(self.anim)
        self.xScale = 1
        self.yScale = 1
        self.score = 0

        self.box = objects.Box(xPosition, yPosition, self.sprite.width * self.xScale, self.sprite.height * self.yScale)

    def start(self):
        if self == engine.player1:
            self.opponent = engine.player2
        elif self == engine.player2:
            self.opponent = engine.player1

    def update(self):
        #   Interact with platforms (colliding, landing, grabbing, etc.)
        self.platformInteraction()
        if self.isRock:
            self.attack(0, 0, 25, 25, 0, 18, 10, 80, 1)
        #   Respawn
        if (self.box.xPosition < -50 or self.box.xPosition > 690 or  self.box.yPosition < -50 or self.box.yPosition > 530) and not self.isDead:
            self.box.xPosition = 1000
            self.opponent.score += 1
            self.isDead = True
            Timer(3, self.respawn).start()
            engine.playexplosion()

        for box in self.hitboxes:
            box.update()

        if self.direction == -1:
            self.spritePrefix = "F"
        else:
            self.spritePrefix = ""

        #   Controls
        if self.input.j:
            #   self.releasedJump makes sure the jumping only happens on a single frame
            if self.input.releaseJ:
                if self.isRock:
                    self.canMove = True
                    self.canAttack = True
                    self.isRock = False
                if self.canMove and self.canAttack:
                    if self.jumpCounter == 0:
                        self.changeSprites("jump" + self.spritePrefix, 30, False)
                        self.jumpCounter += 1
                    elif 0 < self.jumpCounter <= 5:
                        self.jumpCounter += 1
                        if 0 < self.jumpCounter <= 5:
                            self.changeSprites("multiJump" + self.spritePrefix, 30, False)
                    if self.jumpCounter <= 5:
                        self.yVelocity = 5 - self.jumpCounter/2
                        self.isGrounded = False
                        self.input.releaseJ = False
                #   If player is grabbing, remove isGrabbing status and not allow to grab for a short time
                if self.isGrabbing:
                    self.isGrounded = False
                    self.isGrabbing = False
                    self.canGrab = False
                    self.canMove = True
                    self.canAttack = True
                    Timer(.5, self.grabTimer).start()
        if self.jumpCounter >= 5 and self.yVelocity < 0:
            self.changeSprites("noJump" + self.spritePrefix, 30, False)
        if self.input.up:
            if self.input.releaseUp:
                self.isSmashing = True
                Timer(.10, self.smashTimer).start()
                self.input.releaseUp = False
        if self.input.down:
            if self.input.releaseDown:
                self.isSmashing = True
                Timer(.10, self.smashTimer).start()
                self.input.releaseDown = False
                if self.isGrounded:
                    self.changeSprites("crouch" + self.spritePrefix,30,False)

                #   If grabbing, release grab
                if self.isGrabbing:
                    self.isGrounded = False
                    self.isGrabbing = False
                    self.canGrab = False
                    self.canMove = True
                    Timer(.5, self.grabTimer).start()
        if self.input.right:
            if self.canMove and self.canAttack:
                self.xVelocity += self.acceleration
                if self.isGrounded:
                    self.direction = 1
                    if self.sprites != spriteDictionary["walk"]:
                        self.changeSprites("walk", 30, True)
            if self.input.releaseRight:
                self.isSmashing = True
                Timer(.10, self.smashTimer).start()
                self.input.releaseRight = False

        elif self.input.left:
            if self.canMove and self.canAttack:
                self.xVelocity -= self.acceleration
                if self.isGrounded:
                    self.direction = -1
                    if self.sprites != spriteDictionary["walkF"]:
                        self.changeSprites("walkF", 30, True)
            if self.input.releaseLeft:
                self.isSmashing = True
                Timer(.10, self.smashTimer).start()
                self.input.releaseLeft = False

        if self.canAttack:
            if self.input.a and not self.isGrabbing and self.input.releaseA:
                if self.isGrounded:
                    if self.isSmashing:
                        self.smashing = True
                        self.canAttack = False
                        self.canMove = False
                        if self.input.right or self.input.left:
                            self.forward = True
                        elif self.input.up:
                            self.upward = True
                        elif self.input.down:
                            self.downward = True
                        else:
                            self.smashing = False
                            self.canAttack = True
                            self.canMove = True
                    else:
                        self.canMove = False
                        if self.input.right or self.input.left:
                            Timer(10/30, self.attackRecover).start()
                            self.changeSprites("forwardAttack" + self.spritePrefix, 30, False)
                            self.attack(18, 0, 20, 13, 3, 8, 2, 10, 1)
                        elif self.input.up:
                            Timer(10/30, self.attackRecover).start()
                            self.changeSprites("upwardAttack" + self.spritePrefix, 30, False)
                            self.attack(-2, 25, 12, 20, 5, 5, 3, 80, 1)
                        elif self.input.down:
                            Timer(10/30, self.attackRecover).start()
                            self.changeSprites("downwardAttack" + self.spritePrefix, 30, False)
                            self.attack(12, -8, 25, 10, 4, 6, 4, 60, 1)
                        else:
                            if self.basicAttackCounter == 0:
                                self.attack(15, 0, 17, 12, 0, 2, 1, 60, 1)
                                self.changeSprites("basicAttack1" + self.spritePrefix, 30, False)
                                Timer(.2, self.attackRecover).start()
                            elif self.basicAttackCounter == 1:
                                self.attack(15, 0, 17, 12, 0, 3, 1, 60, 1)
                                self.changeSprites("basicAttack2" + self.spritePrefix, 30, False)
                                Timer(.2, self.attackRecover).start()
                            elif 2 <= self.basicAttackCounter <= 7:
                                if self.basicAttackCounter == 7:
                                    self.attack(20, 0, 35, 25, 0, 3, 5, 45, 1)
                                    self.anim = pyglet.image.Animation.from_image_sequence([spriteDictionary["basicAttack3" + self.spritePrefix][3]], 30, False)
                                else:
                                    self.attack(20, 0, 25, 20, 0, 1, 1, 60, 1)
                                    self.anim = pyglet.image.Animation.from_image_sequence([spriteDictionary["basicAttack3" + self.spritePrefix][random.randint(1, 4)]], 30, False)
                                self.sprite = pyglet.sprite.Sprite(self.anim)
                                Timer(.05, self.attackRecover).start()
                            else:
                                Timer(.05, self.attackRecover).start()
                            self.basicAttackCounter += 1
                            attackCounter = self.basicAttackCounter

                            Timer(.5, lambda: self.basicAttackReset(attackCounter)).start()
                        self.canAttack = False
                elif self.aerialAttacked < 2:
                    if (self.input.right and self.direction == 1) or (self.input.left and self.direction == -1):
                        self.canAttack = False
                        self.canMove = False
                        Timer(12 / 30, self.attackRecover).start()
                        Timer(12 / 30, self.frictionRecover).start()
                        self.changeSprites("forwardAerial" + self.spritePrefix, 30, False)
                        self.xVelocity = 5 * self.direction
                        self.xFriction = 1
                        self.yVelocity = 2
                        self.attack(15, 0, 20, 15, 3, 4, 3, 20, 10)
                        self.attack(15, 0, 25, 20, 15, 5, 7, 20, 1)
                    elif (self.input.right and self.direction == -1) or (self.input.left and self.direction == 1):
                        Timer(10 / 30, self.attackRecover).start()
                        self.changeSprites("backwardAerial" + self.spritePrefix, 30, False)
                        self.attack(-15, 0, 20, 12, 3, 13, 5, 155, 1)
                    elif self.input.up:
                        Timer(10 / 30, self.attackRecover).start()
                        self.changeSprites("upwardAerial" + self.spritePrefix, 30, False)
                        self.attack(0, 20, 30, 20, 4, 9, 5, 80, 2)
                    elif self.input.down:
                        Timer(10 / 30, self.attackRecover).start()
                        self.changeSprites("downwardAerial" + self.spritePrefix, 30, False)
                        self.attack(5, -10, 15, 25, 3, 2, 5, 275, 10)
                        self.cancelUpSpecial = False
                        self.upSpecial()
                        Timer(.5, self.upSpecial2).start()
                    else:
                        Timer(10 / 30, self.attackRecover).start()
                        self.changeSprites("basicAerial" + self.spritePrefix, 30, False)
                        self.attack(0, 0, 40, 40, 2, 10, 4, 45, 8)
                    self.aerialAttacked += 1
                self.input.releaseA = False

            if self.input.b and not self.isGrabbing and self.input.releaseB:
                if self.isGrounded:
                    self.canAttack = False
                    self.canMove = False
                    if self.input.right or self.input.left:
                        Timer(1, self.attackRecover).start()
                        self.changeSprites("forwardSpecial" + self.spritePrefix, 30, False)
                        self.attack(25, 0, 25, 25, 9, 19, 7, 35, 5)
                    elif self.input.up:
                        self.changeSprites("upwardSpecial" + self.spritePrefix, 30, False)
                        self.attack(25, 0, 25, 25, 0, 5, 3, 80, 8)
                        self.attack(25, 0, 25, 25, 15, 5, 3, 280, 8)
                        self.yVelocity = 10
                        self.isGrounded = False
                        self.isUpSpecial = True
                        self.cancelUpSpecial = False
                        Timer(.4, self.upSpecial).start()
                        Timer(2, self. upSpecial2).start()
                        Timer(1, self.attackRecover).start()
                    elif self.input.down:
                        self.changeSprites("downwardSpecial" + str(random.randint(1, 5)) + self.spritePrefix, 10, False)
                        self.isRock = True
                        self.cancelUpSpecial = False
                        self.isUpSpecial = True
                        Timer(.2, self.upSpecial).start()
                        Timer(2, self.upSpecial2).start()
                    else:
                        self.canAttack = True
                        self.canMove = True
                elif self.aerialSpecialed < 2:
                    if self.input.right or self.input.left:
                        Timer(30 / 30, self.attackRecover).start()
                        self.changeSprites("forwardAerialSpecial" + self.spritePrefix, 30, False)
                        self.canAttack = False
                        self.canMove = False
                        self.regainMomentum = True
                        self.attack(10, 10, 40, 40, 2, 15, 6, 40, 8)
                    elif self.input.up:
                        self.changeSprites("upwardSpecial" + self.spritePrefix, 30, False)
                        self.attack(25, 0, 25, 25, 0, 5, 3, 80, 8)
                        self.attack(25, 0, 25, 25, 15, 5, 3, 280, 8)
                        self.yVelocity = 10
                        self.isGrounded = False
                        self.isUpSpecial = True
                        self.canMove = False
                        self.canAttack = False
                        self.cancelUpSpecial = False
                        Timer(.4, self.upSpecial).start()
                        Timer(2, self.upSpecial2).start()
                        Timer(1, self.attackRecover).start()
                    elif self.input.down:
                        self.changeSprites("downwardSpecial" + str(random.randint(1,5)) + self.spritePrefix, 10, False)
                        Timer(.2, self.upSpecial).start()
                        self.isRock = True
                        self.canMove = False
                        self.canAttack = False
                        self.cancelUpSpecial = False
                        self.isUpSpecial = True
                        Timer(2, self.upSpecial2).start()
                    self.aerialSpecialed += 1
                self.input.releaseB = False
        if self.smashing:
            if self.forward:
                if self.smashCounter < 100:
                    self.smashCounter += 2.5
                    if not self.startedCharge:
                        self.changeSprites("forwardSmashCharge" + self.spritePrefix, 30, True)
                        self.startedCharge = True
                if not self.input.a or self.smashCounter == 100:
                    self.changeSprites("forwardSmash" + self.spritePrefix, 30, False)
                    self.attack(17, 0, 25, 13, 3, 10+6*self.smashCounter/100, 2 + 4*self.smashCounter/100, 20, 1)
                    self.xVelocity = 20 * self.direction * self.smashCounter/100
                    self.canMove = True
                    self.smashing = False
                    self.forward = False
                    self.startedCharge = False
                    Timer(.5, self.attackRecover).start()
                    self.smashCounter = 0
            if self.upward:
                if self.smashCounter < 100:
                    self.smashCounter += 2.5
                    if not self.startedCharge:
                        self.changeSprites("upwardSmashCharge" + self.spritePrefix, 30, True)
                        self.startedCharge = True
                if not self.input.a or self.smashCounter == 100:
                    self.changeSprites("upwardSmash" + self.spritePrefix, 30, False)
                    self.attack(0, 15, 30, 25, 3, 9+6*self.smashCounter/100, 2 + 6*self.smashCounter/100, 85, 2)
                    self.isGrounded = False
                    self.yVelocity += 1.5
                    self.startedCharge = False
                    self.smashing = False
                    self.upward = False
                    Timer(.5, self.attackRecover).start()
                    self.smashCounter = 0
            if self.downward:
                if self.smashCounter < 100:
                    self.smashCounter += 2.5
                    if not self.startedCharge:
                        self.changeSprites("downwardSmashCharge" + self.spritePrefix, 30, True)
                        self.startedCharge = True
                if not self.input.a or self.smashCounter == 100:
                    self.changeSprites("downwardSmash" + self.spritePrefix, 30, False)
                    self.attack(0, -10, 40, 12, 3, 8+6*self.smashCounter/100, 2 + 5*self.smashCounter/100, 80, 8)
                    self.xVelocity = 3 * -self.direction
                    self.canMove = True
                    self.startedCharge = False
                    self.smashing = False
                    self.downward = False
                    Timer(.5, self.attackRecover).start()
                    self.smashCounter = 0
        #   If player is touching ground remove gravity effects
        if self.isGrounded:
            self.jumpCounter = 0
            self.yVelocity = 0
            if self.xVelocity == 0 and self.canAttack and self.canMove and not self.input.down:
                if self.direction == 1 and not self.sprites == spriteDictionary["idle"]:
                    self.changeSprites("idle", 30, False)
                elif self.direction == -1 and not self.sprites == spriteDictionary["idleF"]:
                    self.changeSprites("idleF", 30, False)
        else:
            self.yVelocity -= objects.yGravity
            if self.yVelocity < -5 and not self.isUpSpecial:
                self.yVelocity = -5
        #   If not grabbing ledge, allow movement

        #   change position based on Velocity
        if not self.isGrabbing:
            self.box.xPosition += self.xVelocity
            self.box.yPosition += self.yVelocity
            self.box.xCenter = self.box.xPosition + self.box.width/2
            self.box.yCenter = self.box.yPosition + self.box.height/2

        #   If abs(velocity) is greater than 1, divide it by the friction and if less then one just make it 0
        if abs(self.xVelocity) > 1:
            if not self.regainMomentum or self.isGrounded:
                self.xVelocity /= self.xFriction
        else:
            self.xVelocity = 0

        if self.canMove and self.canAttack and self.isGrounded:
            if self.direction == 1 and self.orientation == "left":
                self.orientation = "right"
                self.spritexPosition = 0
            elif self.direction == -1 and self.orientation == "right":
                self.orientation = "left"
                self.spritexPosition = self.box.width
        #   Update the position and scale of the sprite
        self.sprite.update(x=self.box.xPosition + self.spritexPosition, y=self.box.yPosition, scale_x=self.xScale, scale_y=self.yScale)

    def attack(self, xRel, yRel, width, height, delay, damage, knockback, angle, duration):
        objects.Hitbox(xRel, yRel, width, height, delay, damage, knockback, angle, self, self.opponent, duration)
    def basicAttackReset(self, n):
        if self.basicAttackCounter == n or (self.basicAttackCounter > 7 and n > 7):
            self.basicAttackCounter = 0
    def goHurtSprite(self):
        if self.spritePrefix == "":
            self.sprite = pyglet.sprite.Sprite(self.hurtSprite)
        elif self.spritePrefix == "F":
            self.sprite = pyglet.sprite.Sprite(self.hurtSpriteF)
    def upSpecial(self):
        if not self.cancelUpSpecial:
            self.yVelocity = -10
    def upSpecial2(self):
        self.isUpSpecial = False
    def attackRecover(self):
        self.canAttack = True
        self.canMove = True
        self.regainMomentum = False
    def frictionRecover(self):
        self.xFriction = 1.75
    def platformInteraction(self):
        if self.isGrounded:
            #   If its state is touching the ground but it is not anywhere on top of a platform,
            #   then isGrounded should be false now
            if not (self.box.yPosition - 5 < self.groundedPlatform.box.yPosition + self.groundedPlatform.box.height < self.box.yPosition + 20 and
                    self.box.xPosition + self.box.width > self.groundedPlatform.box.xPosition and
                    self.box.xPosition < self.groundedPlatform.box.xPosition + self.groundedPlatform.box.width):
                self.isGrounded = False
        else:
            #   Check each platform for possible interactions
            for platform in objects.platformBoxList:
                #   If not isGrounded but on top of the platform, set the position of the player exactly on top of the
                #   platform and make isGrounded true
                if self.box.yPosition < platform.box.yPosition + platform.box.height < self.box.yPosition + 5 and \
                        self.box.xPosition + self.box.width > platform.box.xPosition and \
                        self.box.xPosition < platform.box.xPosition + platform.box.width:
                    self.isGrounded = True
                    self.box.yPosition = platform.box.yPosition + platform.box.height
                    self.groundedPlatform = platform
                    self.resetAerial()
                elif self.box.yPosition + 5 < platform.box.yPosition + platform.box.height < self.box.yPosition + 50:
                    #   If player touches the left ledge, grab it
                    if platform.box.xPosition + 10 > self.box.xPosition + self.box.width + 1 > platform.box.xPosition:
                        if self.canGrab:
                            self.isGrounded = True
                            self.isGrabbing = True
                            self.canMove = False
                            self.cancelUpSpecial = True
                            self.box.xPosition = platform.box.xPosition - 20
                            self.box.yPosition = platform.box.yPosition + platform.box.height - 30
                            self.changeSprites("ledge", 30, False)
                            self.direction = 1
                            self.spritexPosition = 0
                            self.resetAerial()
                    #   If player touches the right ledge, grab it
                    elif platform.box.xPosition + platform.box.width > self.box.xPosition - 1 > platform.box.xPosition + platform.box.width - 10:
                        if self.canGrab:
                            self.isGrounded = True
                            self.isGrabbing = True
                            self.canMove = False
                            self.cancelUpSpecial = True
                            self.box.xPosition = platform.box.xPosition + platform.box.width
                            self.box.yPosition = platform.box.yPosition + platform.box.height - 30
                            self.changeSprites("ledgeF", 30, False)
                            self.direction = -1
                            self.spritexPosition = self.box.width
                            self.resetAerial()
                    #   If player is on top of the box, make the player land on the box
                    elif self.box.xPosition + self.box.width > platform.box.xPosition and \
                            self.box.xPosition < platform.box.xPosition + platform.box.width:
                        self.isGrounded = True
                        self.box.yPosition = platform.box.yPosition + platform.box.height
                        self.groundedPlatform = platform
                        self.resetAerial()

                #   If player touches left or right side of platform don't allow to go any further
                elif platform.box.yPosition < self.box.yPosition < platform.box.yPosition + platform.box.height:
                    if platform.box.xPosition + platform.box.width > self.box.xPosition > platform.box.xPosition + platform.box.width - 20:
                        self.box.xPosition = platform.box.xPosition + platform.box.width

                    elif platform.box.xPosition + 20 > self.box.xPosition + self.box.width > platform.box.xPosition:
                        self.box.xPosition = platform.box.xPosition - self.box.width

    #   Function to call after temporarily disabling grab
    def grabTimer(self):
        self.canGrab = True
    #   Function to call to check if going to smash
    def smashTimer(self):
        self.isSmashing = False
    def changeSprites(self, name, fps, loop):
        self.sprites = spriteDictionary[name]
        self.anim = pyglet.image.Animation.from_image_sequence(self.sprites, 1 / fps, loop)
        self.sprite = pyglet.sprite.Sprite(self.anim)
    def draw(self):
        self.sprite.draw()
    def respawn(self):
        self.box.yPosition = 0
        self.box.xPosition = 320
        self.box.yPosition = 240
        self.damage = 0
        self.xVelocity = 0
        self.yVelocity = 0
        self.isDead = False
        self.resetAerial()
    def resetAerial(self):
        self.aerialSpecialed = 0
        self.aerialAttacked = 0