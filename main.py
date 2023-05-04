import pygame
import math

# załączam pygame
pygame.init()
# ustawiam wielkość ekranu
screen = pygame.display.set_mode((800, 600))
# ustawiam nazwę i miniature
pygame.display.set_caption("Blok Ekipa Drag Race Game")
icon = pygame.image.load("sport-car.png")
pygame.display.set_icon(icon)

# Gracz
playerImg = pygame.image.load("enemy_car.jpeg")
playerX = -200
playerY = 100
playerChange = 0
gas_lvl = 1
clutch_pressed = False
gear = 1
velocity = 0
d_velocity = 0
RPM = 3000
mass = 1800
power = 73550


def player():
    screen.blit(playerImg, (playerX, playerY))


def gear_shift():
    global gear
    if not clutch_pressed or gear == 6:
        print("Honk!!!")
    else:
        print("Click")
        gear += 1


def calc_drag():
    cross_sectio = 1.77
    drag_co = 0.3
    air_density = 1.225
    return 0.5 * air_density * velocity ** 2 * drag_co * cross_sectio


def calc_dv():
    x = RPM / 1000
    power_out = x * math.sqrt(11 - x) * 0.0712134 * power
    work = power_out * gas_lvl * dt
    dwork = work - calc_drag() * dt
    if dwork >= 0:
        dv = math.sqrt((2 * dwork) / mass)
    else:
        dv = math.sqrt(((-2) * dwork) / mass) * (-1)
    return dv


def speed_to_rpm():
    global RPM
    # stosunki przekładni
    sheet = {1: 15.466, 2: 9.082, 3: 6.845, 4: 4.052, 5: 2.892, 6: 2.310}
    shaft_rpm = velocity / (math.pi * 0.51)
    RPM = shaft_rpm * sheet[gear]
    if RPM > 8000: RPM = 8000


# tu śmiga pętla gry
run = True
while run:
    clock = pygame.time.Clock()
    dt = clock.tick(60) / 1000
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: gas_lvl = 1
            if event.key == pygame.K_2: gas_lvl = 2
            if event.key == pygame.K_3: gas_lvl = 3
            if event.key == pygame.K_4: gas_lvl = 4
            if event.key == pygame.K_5: gas_lvl = 5
            if event.key == pygame.K_i: gear_shift()
            if event.key == pygame.K_SPACE: clutch_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE: clutch_pressed = False

    if not clutch_pressed:
        velocity += calc_dv()
        speed_to_rpm()

    print(gas_lvl, clutch_pressed, gear, RPM, velocity)
    player()

    # ta linijka robi odświeżenie ekranu
    pygame.display.update()
