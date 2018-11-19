import engine
import objects
from pyglet.window import key
from pyglet.gl import *
window = pyglet.window.Window()
background_stream = pyglet.image.load('background.png', file=open('background.png', 'rb'))
background = pyglet.sprite.Sprite(background_stream, x=0, y=0)
camera = objects.Camera()

def update(dt):
    engine.update()
    camera.update()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, camera.width, 0, camera.height, -1, 1)
    glTranslatef(-camera.x, -camera.y, 0)
    glScalef(camera.toZoom, camera.toZoom, 1)
    glMatrixMode(GL_MODELVIEW)

@window.event
def on_draw():
    window.clear()
    background.draw()
    engine.player1.player.sprite.draw()
    engine.player2.sprite.draw()


@window.event
def on_key_press(symbol, modifier):
    if symbol == key.W:
        engine.player1.player.input.up = True
    if symbol == key.S:
        engine.player1.player.input.down = True
    if symbol == key.A:
        engine.player1.player.input.left = True
    if symbol == key.D:
        engine.player1.player.input.right = True
    if symbol == key.G:
        engine.player1.player.input.a = True
    if symbol == key.H:
        engine.player1.player.input.b = True

    if symbol == key.UP:
        engine.player2.input.up = True
    if symbol == key.DOWN:
        engine.player2.input.down = True
    if symbol == key.LEFT:
        engine.player2.input.left = True
    if symbol == key.RIGHT:
        engine.player2.input.right = True

@window.event
def on_key_release(symbol, modifier):
    if symbol == key.W:
        engine.player1.player.input.up = False
        engine.player1.player.releasedJump = True
    if symbol == key.S:
        engine.player1.player.input.down = False
    if symbol == key.A:
        engine.player1.player.input.left = False
    if symbol == key.D:
        engine.player1.player.input.right = False
    if symbol == key.G:
        engine.player1.player.input.a = False
    if symbol == key.H:
        engine.player1.player.input.b = False

    if symbol == key.UP:
        engine.player2.input.up = False
        engine.player2.releasedJump = True
    if symbol == key.DOWN:
        engine.player2.input.down = False
    if symbol == key.LEFT:
        engine.player2.input.left = False
    if symbol == key.RIGHT:
        engine.player2.input.right = False


pyglet.clock.schedule_interval(update, 1/120)
pyglet.app.run()
