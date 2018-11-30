import objects
import player

player1 = player.Player(250, 150)
player2 = player.Player(375, 150)
player1.start()
player2.start()
platform1 = objects.Platform(-50, -50, 2, 1.85)
platform2 = objects.Platform(500, -50, 2, 1.85)
platform3 = objects.Platform(225, -50, 1.98, 1.45)

hitboxes = []
#gameObjects.append(platform1)
#gameObjects.append(platform2)
#gameObjects.append(platform3)

def update():
    player1.update()
    player2.update()

#Does kirby's jump reset after getting hit
#How many times can kirby do each aerial attack in air
#Do they reset after he gets hit
#