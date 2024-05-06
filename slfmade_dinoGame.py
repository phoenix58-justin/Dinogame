from ursina import *
from random import randint
app = Ursina()
window.fullscreen = False
window.color = color.white

ground1 = Entity(model = 'quad', 
                texture = 'assets\ground', 
                scale = (50, 0.5, 0.25), 
                position = (0, -3, 0))
ground2 = duplicate(ground1, x = 50)
pair = [ground1, ground2]

starblast = Animation('assets\stq', model = 'sphere', collider = 'sphere', position = (-5.1, -2.4, 0), scale = (1.2, 1.2, 1), delay = 1, enabled = False)

dino = Animation('assets\dino', collider = 'box', position = (-5, -2.4, -0.5))

cactus = Entity(texture = 'assets\cactus', model = 'quad', position = (20, -2.4, -0.5), collider = 'sphere')

sword_for_dino = Entity(texture = 'assets\kenn', model = 'quad', position = (20, -2.4, -0.5), collider = 'sphere', enabled = False, scale = (0.5, 0.5, 1))

sword = Entity(texture = 'assets\kenn2', model = 'quad', position = (20, -2.4, -0.5), collider = 'sphere', enabled = True)

cacti = []
def newCactus():
    newC = duplicate(cactus, x = 12 + randint(0, 5))
    cacti.append(newC)
    invoke(newCactus, delay = randint(12, 20) / 10)
newCactus()

kirito = []
def newSword():
    newS = duplicate(sword, x = 30 + randint(0, 15), y = -2.4 + randint(0, 24) * 0.1)
    kirito.append(newS)
    invoke(newSword, delay = randint(40, 50) / 10)
newSword()

sound = Audio(
    'assets\\beep',
    autoplay = False
)

def bruh():
    red = randint(125, 255)
    blue = randint(150, 255)
    green = randint(150, 255)
    dino.color = color.rgb(red, green, blue)
    invoke(bruh, delay = 0.5)
bruh()

label = Text(
    text = f'Points: {0}',
    color = color.black,
    position = (-0.5, 0.4)
)
s = 1

muteki = False
doStarblast = False

dead = Text(
    text = f' ',
    color = color.red,
    position = (-0.85, -0.2),
    scale = (10),
    ignore = True,
    rotation = (0, 0, -15)
)

def update():
    global doStarblast
    global s, p
    starblast.x = dino.x
    starblast.y = dino.y
    sword_for_dino.x = dino.x + 0.4
    sword_for_dino.y = dino.y
    label.text = f'Points: {int(s * 100) - 100}'
    s += randint(1, 12) * 0.00005
    for ground in pair:
        ground.x -= 6 * s * time.dt
        if ground.x < -35:
            ground.x += 100
    for c in cacti:
        c.x -= 6 * s * time.dt
    for g in kirito:
        g.x -= 6 * s * time.dt
    if doStarblast == True:
        sword_for_dino.enabled = True
    else:
        sword_for_dino.enabled = False
    cut_info = starblast.intersects()
    if cut_info.hit:
        if cut_info.entity in cacti:
            cut_info.entity.texture = 'assets\cactus_broken'
    hit_info = dino.intersects()
    if hit_info.hit:
        if hit_info.entity in cacti and not muteki:
            hit_info.entity.texture = 'assets\cactus'
            dino.texture = 'assets\hit' 
            dead.text = f'YOU ARE DEAD'
            application.pause()
        elif hit_info.entity in kirito:
            doStarblast = True
            hit_info.entity.enabled = False
    object_intersect = cacti[-1].intersects()
    if object_intersect.hit:
        if object_intersect.entity in kirito:
            object_intersect.entity.enabled = False 

def input(key): 
    global muteki, doStarblast, s
    if key == 'space':
        sound.play()
        if dino.y < -2.4:
            dino.animate_y(0, duration = 0.4, curve = curve.out_sine)
        dino.animate_y(-2.4, duration = 0.4, delay = 0.35, curve = curve.in_sine)
    if key == 'z':
        if muteki == True:
            muteki = False
        else:
            muteki = True
    if key == 'x':
        if doStarblast == True:
            doStarblast = distinguish(doStarblast)
    if key == 'q':
        s *= 1.11
        

def distinguish(doStarblast):
    if doStarblast:
        starblast.enabled = True
        invoke(distinguish, False, delay = 3)
    else:
        starblast.enabled = False
        return False

camera.orthographic = True
camera.fov = 10

app.run()
