import objects

player1 = objects.Kirby(250, 150)
player2 = objects.Player(375, 150)
platform1 = objects.Platform(-50, -50, 2, 1.85)
platform2 = objects.Platform(500, -50, 2, 1.85)
platform3 = objects.Platform(225, -50, 1.98, 1.45)

#gameObjects.append(platform1)
#gameObjects.append(platform2)
#gameObjects.append(platform3)

def update():
    player1.update()
    player2.update()
