import engine
import objects
from pyglet.window import key
from pyglet.gl import *

#   Create window, background and camera
window = pyglet.window.Window()

#   Runs 120 times per second
def update(dt):
    engine.update()
    if engine.gameStarted:
        engine.camera.update()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, engine.camera.width, 0, engine.camera.height, -1, 1)
        glTranslatef(-engine.camera.x, -engine.camera.y, 0)
        glScalef(engine.camera.toZoom, engine.camera.toZoom, 1)
        glMatrixMode(GL_MODELVIEW)

#   The objects to be drawn on screen
@window.event
def on_draw():
    window.clear()
    for object in engine.toDraw:
        object.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    if engine.gameState == "MainMenu":
        for icon in engine.levelSelectIcons:
            if icon.x < x < icon.x + icon.width and icon.y < y < icon.y + icon.height:
                engine.levelSelected(icon)
        if 280 < x < 365 and 80 < y < 110:
            engine.showStatsScreen()
    elif engine.gameState == "StatsScreen":
        if 0 < x < 100 and 0 < y < 30:
            engine.endGame()
#   Detect on button press
@window.event
def on_key_press(symbol, modifier):
    if symbol == key.W:
        engine.player1.input.up = True
    if symbol == key.S:
        engine.player1.input.down = True
    if symbol == key.A:
        engine.player1.input.left = True
    if symbol == key.D:
        engine.player1.input.right = True
    if symbol == key.G:
        engine.player1.input.j = True
    if symbol == key.H:
        engine.player1.input.a = True
    if symbol == key.J:
        engine.player1.input.b = True

    if symbol == key.UP:
        engine.player2.input.up = True
    if symbol == key.DOWN:
        engine.player2.input.down = True
    if symbol == key.LEFT:
        engine.player2.input.left = True
    if symbol == key.RIGHT:
        engine.player2.input.right = True
    if symbol == key.NUM_2 or symbol == key.N:
        engine.player2.input.a = True
    if symbol == key.NUM_3 or symbol == key.M:
        engine.player2.input.b = True
    if symbol == key.NUM_1 or symbol == key.B:
        engine.player2.input.j = True

#   Detect on button release
@window.event
def on_key_release(symbol, modifier):
    if symbol == key.W:
        engine.player1.input.up = False
        engine.player1.input.releaseUp = True
    if symbol == key.S:
        engine.player1.input.down = False
        engine.player1.input.releaseDown = True
    if symbol == key.A:
        engine.player1.input.left = False
        engine.player1.input.releaseLeft = True
    if symbol == key.D:
        engine.player1.input.right = False
        engine.player1.input.releaseRight = True
    if symbol == key.G:
        engine.player1.input.j = False
        engine.player1.input.releaseJ = True
    if symbol == key.H:
        engine.player1.input.a = False
        engine.player1.input.releaseA = True
    if symbol == key.J:
        engine.player1.input.b = False
        engine.player1.input.releaseB = True

    if symbol == key.UP:
        engine.player2.input.up = False
        engine.player2.input.releaseUp = True
    if symbol == key.DOWN:
        engine.player2.input.down = False
        engine.player2.input.releaseDown = True
    if symbol == key.LEFT:
        engine.player2.input.left = False
        engine.player2.input.releaseLeft = True
    if symbol == key.RIGHT:
        engine.player2.input.right = False
        engine.player2.input.releaseRight = True
    if symbol == key.NUM_2 or symbol == key.N:
        engine.player2.input.a = False
        engine.player2.input.releaseA = True
    if symbol == key.NUM_3 or symbol == key.M:
        engine.player2.input.b = False
        engine.player2.input.releaseB = True
    if symbol == key.NUM_1 or symbol == key.B:
        engine.player2.input.j = False
        engine.player2.input.releaseJ = True

pyglet.clock.schedule_interval(update, 1/120)
pyglet.app.run()
