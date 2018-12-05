import objects
import player
import pyglet
from threading import Timer

toDraw = []
toUpdate = []
levelSelectIcons = []
hitboxes = []
gameStarted = False
stage1icon = None
stage2icon = None
stage3icon = None
player1 = None
player2 = None
runTimer = True
camera = objects.Camera()

gameState = "MainMenu"

pyglet.font.add_file('smashfont.ttf')
smashfont = pyglet.font.load("Super Smash 4.1")

#Main Menu images
mainmenubg = pyglet.image.load("main_menu_bg.png", file=open("main_menu_bg.png", "rb"))
menubackground = pyglet.sprite.Sprite(mainmenubg)
menubackground.update(x=0, y=-5, scale_x=.95, scale_y=.95)
backgrounds = [pyglet.image.load('stage_1.png', file=open('stage_1.png', 'rb')),
               pyglet.image.load('stage_2.png', file=open('stage_2.png', 'rb')),
               pyglet.image.load('stage_3.png', file=open('stage_3.png', 'rb'))]
logo = pyglet.image.load('logo.png', file=open('logo.png', 'rb'))
logosprite = pyglet.sprite.Sprite(logo)

#Main menu and stats screen labels
statsDict = {"player1wins" : 0, "player2wins" : 0, "player1totalpoints" : 0, "player2totalpoints" :0}
levelText = pyglet.text.Label("Level Select", x=172, y=320, font_size=32, font_name="Super Smash 4.1")
statsText = pyglet.text.Label("Stats", x=280, y=70, font_size=20, font_name="Super Smash 4.1")

#Sounds to be used in game
pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent',)
bgm = pyglet.media.load("bgm.wav")
hurtsound = pyglet.media.load("hurt.wav")
deathsound = pyglet.media.load("explosion.wav")
canplayhurtsound = True
canplayexplosion = True

stage1 = objects.Stage(backgrounds[0], -50, 0, 1.09)
stage2 = objects.Stage(backgrounds[1], -210, -40, 1)
stage3 = objects.Stage(backgrounds[2], -50, 0, 1.90)

def loadStats():
    global statsDict
    config = open("stats.txt", "r")
    lines = config.readlines()
    for i in range(len(statsDict)):
        line = lines[i].split("=")
        statsDict[line[0]] = int(line[1].rstrip("\n"))

def saveStats():
    stats = open("stats.txt", "w")
    for stat in statsDict.keys():
        stats.write(stat + "=" + str(statsDict[stat]) + "\n")

#   Main menu
def endGame():
    global toDraw, toUpdate, gameStarted, stage1icon, stage2icon, stage3icon, gameState
    gameState = "MainMenu"
    toDraw = []
    toUpdate = []
    gameStarted = False
    logosprite.update(x=35, y=390, scale_x=.45, scale_y=.45)
    toDraw.append(menubackground)
    toDraw.append(logosprite)
    toDraw.append(levelText)
    toDraw.append(statsText)
    stage1icon = pyglet.sprite.Sprite(stage1.background)
    stage1icon.update(x=35, y=175, scale_x=.25, scale_y=.25)
    stage2icon = pyglet.sprite.Sprite(stage2.background)
    stage2icon.update(x=235, y=175, scale_x=.21, scale_y=.21)
    stage3icon = pyglet.sprite.Sprite(stage3.background)
    stage3icon.update(x=460, y=175, scale_x=.43, scale_y=.43)
    levelSelectIcons.append(stage1icon)
    levelSelectIcons.append(stage2icon)
    levelSelectIcons.append(stage3icon)
    toDraw.append(stage1icon)
    toDraw.append(stage2icon)
    toDraw.append(stage3icon)

loadStats()
saveStats()
endGame()

#S   tats screen
def showStatsScreen():
    global toDraw, toUpdate, gameState
    gameState = "StatsScreen"
    toDraw = []
    toUpdate = []

    label1 = pyglet.text.Label("Stats", x=250, y=440, font_size=32, font_name="Super Smash 4.1")
    label2 = pyglet.text.Label("<- Back", x=5, y=5, font_size=20, font_name="Super Smash 4.1")
    wins = pyglet.text.Label("Wins", x=50, y=300, font_size=20, font_name="Super Smash 4.1")
    totalpoints = pyglet.text.Label("Total Points", x=50, y=250, font_size=20, font_name="Super Smash 4.1")
    player1 = pyglet.text.Label("Player 1", x=260, y=350, font_size=22, font_name="Super Smash 4.1")
    player1wins = pyglet.text.Label(str(statsDict["player1wins"]), x=310, y=300, font_size=20, font_name="Super Smash 4.1")
    player1totalpoints = pyglet.text.Label(str(statsDict["player1totalpoints"]), x=310, y=250, font_size=20, font_name="Super Smash 4.1")
    player2 = pyglet.text.Label("Player 2", x=440, y=350, font_size=22, font_name="Super Smash 4.1")
    player2wins = pyglet.text.Label(str(statsDict["player2wins"]), x=490, y=300, font_size=20, font_name="Super Smash 4.1")
    player2totalpoints = pyglet.text.Label(str(statsDict["player2totalpoints"]), x=490, y=250, font_size=20, font_name="Super Smash 4.1")

    toDraw.append(menubackground)
    toDraw.append(label2)
    toDraw.append(label1)
    toDraw.append(wins)
    toDraw.append(totalpoints)
    toDraw.append(player1)
    toDraw.append(player1wins)
    toDraw.append(player1totalpoints)
    toDraw.append(player2)
    toDraw.append(player2wins)
    toDraw.append(player2totalpoints)

#   Determine level selected and assign platforms for the correct stage
def levelSelected(level):
    if level == stage1icon:
        platform1 = objects.Platform(-58, -48, 2, 2.70)
        platform2 = objects.Platform(526, -48, 2, 2.70)
        platform3 = objects.Platform(210, -80, 2.47, 2.50)
        startGame(250, 150, 375, 150, stage1)
    elif level == stage2icon:
        platform1 = objects.Platform(-45, -95, 1.5, 2.50)
        platform2 = objects.Platform(555, -45, 1.5, 2)
        platform3 = objects.Platform(155, -80, 3.48, 2.50)
        platform4 = objects.Platform(185, 260, .65, .1)
        platform5 = objects.Platform(407, 260, .65, .1)
        startGame(250, 150, 375, 150, stage2)
    elif level == stage3icon:
        platform1 = objects.Platform(70, -80, 4.83, 1.65)
        startGame(250, 150, 375, 150, stage3)

#   Start the game with given values
def startGame(xPos1, yPos1, xPos2, yPos2, stage):
    global player1, player2, gameStarted, camera, hitboxes, runTimer, gameState
    gameState = "InGame"
    runTimer = True
    gameStarted = True
    hitboxes = []
    #   Set proper background
    background = pyglet.sprite.Sprite(stage.background, x=stage.bgx, y=stage.bgy)
    background.update(x=stage.bgx, y=stage.bgy, scale_x=stage.scale, scale_y=stage.scale)
    toDraw.append(background)

    #   Set both player position and sprites
    player1 = player.Player(xPos1, yPos1)
    player2 = player.Player(xPos2, yPos2)
    player1.start()
    player2.start()
    toDraw.append(player1)
    toDraw.append(player2)
    toUpdate.append(player1)
    toUpdate.append(player2)

    #   Set the damage meters
    label1 = objects.DamageMeter(player1)
    label2 = objects.DamageMeter(player2)
    toDraw.append(label1)
    toDraw.append(label2)
    toUpdate.append(label1)
    toUpdate.append(label2)

    #   Set the timer and socres
    timer = objects.GameTimer(2)
    toDraw.append(timer)
    toUpdate.append(timer)
    score1 = objects.Scores(player1)
    score2 = objects.Scores(player2)
    toDraw.append(score1)
    toDraw.append(score2)
    toUpdate.append(score1)
    toUpdate.append(score2)

#   Runs each frame
def update():
    for object in toUpdate:
        object.update()

#   Control music and sounds
def playMusic():
    try:
        bgm.play()
    except:
        print("WARNING: " + str(deathsound) + " cannot be played.")
    Timer(210, playMusic).start()
playMusic()

def playhurtsound():
    global canplayhurtsound
    if canplayhurtsound:
        canplayhurtsound = False
        try:
            hurtsound.play()
        except:
            print("WARNING: " + str(hurtsound) + " cannot be played.")
        Timer(1, allowhurtsound).start()

def allowhurtsound():
    global canplayhurtsound
    canplayhurtsound = True

def playexplosion():
    global canplayexplosion
    if canplayexplosion:
        canplayexplosion = False
        try:
            deathsound.play()
        except:
            print("WARNING: " + str(deathsound) + " cannot be played.")
        Timer(5, allowexplosionsound).start()

def allowexplosionsound():
    global canplayexplosion
    canplayexplosion = True