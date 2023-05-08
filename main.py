import pygame
import math
import random

# załączam pygame
pygame.init()
# ustawiam wielkość ekranu
screen = pygame.display.set_mode((900, 600))
# ustawiam nazwę i miniature
pygame.display.set_caption("Blok Ekipa Drag Race Game")
icon = pygame.image.load("sport-car.png")
pygame.display.set_icon(icon)

# Gracz
playerImg = pygame.image.load("Player_car_template.png")
playerX = -200
playerY = 100
# Parametry fury
gear_box = {0: float('inf'), 1: 27.5, 2: 13.7, 3: 9.1, 4: 7.4, 5: 5.3, 6: 4.37}


class wheel_class:
    def __init__(self, image):
        self.image = image
        self.angle = 0

    def show(self, pos_x, pos_y, speed):
        vibration = (random.random() * 2 - 1) * (speed / 55)
        img_copy = pygame.transform.rotate(self.image, self.angle)
        screen.blit(img_copy, (pos_x - img_copy.get_width() // 2, pos_y - img_copy.get_height() // 2))

player_wheel = pygame.image.load("wheel_template.png")
front_wheel = wheel_class(player_wheel)
back_wheel = wheel_class(player_wheel)


def gear_shift(num):
    global gear, gear_shifted
    if not clutch_pressed:
        print("Honk!!!")
    else:
        gear_shifted = num - gear
        gear = num


def game_over():
    print("Game over")


def clutch_release():
    global RPM, clutch_pressed, gear_shifted
    if gear_shifted:
        RPM -= 2500 * gear_shifted
        gear_shifted = 0
    clutch_pressed = False


def d_rpm():
    amp = math.floor(abs(7250 - RPM) / 400)
    return int((26 - amp) * math.sqrt(6 / gear))


def rpm_to_speed():
    shaft_rpm = RPM / gear_box[gear]
    # 2 jest od 2 m obwodu koła
    speed = shaft_rpm * 2 * 60 / 1000
    return speed


# Starting stats
game_state = "EP"
clock = pygame.time.Clock()
gear = 0
clutch_pressed = False
velocity = 0
RPM = 1000
gear_shifted = 0
distance = 0
wait = True
run = True
tick = 0
# Start
while run:
    dt = clock.tick(30) / 1000  # w sekundach
    screen.fill((255, 255, 255))
    if tick == 10:
        game_state = "GP"

    # ___Ekran Początkowy
    if game_state == "EP":
        # pętla eventów
        tick += 1
        for event in pygame.event.get():
            # to umożliwia wyjście
            if event.type == pygame.QUIT:
                run = False

    # ___Rozgrywka___
    if game_state == "GP":
        # pętla eventów
        for event in pygame.event.get():
            # to umożliwia wyjście
            if event.type == pygame.QUIT:
                run = False
            # tu mamy całe sterowanie
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: gear_shift(1)
                if event.key == pygame.K_2: gear_shift(2)
                if event.key == pygame.K_3: gear_shift(3)
                if event.key == pygame.K_4: gear_shift(4)
                if event.key == pygame.K_5: gear_shift(5)
                if event.key == pygame.K_6: gear_shift(6)
                if event.key == pygame.K_SPACE: clutch_pressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE: clutch_release()

        # tu są wszystkie akcje w zależności od trzymania sprzęgła
        if not clutch_pressed and gear != 0:
            RPM += d_rpm()
            velocity = rpm_to_speed()
        if clutch_pressed or gear == 0:
            RPM += 70
            if velocity > 0: velocity -= 0.2

        # tu jest zgrywanie ze sobą RPM, distance i velocity
        if velocity < 0: velocity = 0
        distance += velocity * dt / 3.6  # 3.6 daje nam metry na sekundę
        if RPM > 8000:
            RPM -= 85
        if RPM < 1000:
            game_over()
            break

        # tu mamy animowanie naszego pojazdu
        # zacznijmy od ruchów góra dół
        amp = 2 * (random.random() - 0.5)  # zwraca "losową" wartość [-1,1]
        dplayerY = playerY + amp * ((RPM / 4000) * (velocity / 100))
        # tu mamy wyjechanie na środek ekranu na start
        if distance < 8:
            playerX = distance * 50 - 200
        else:
            playerX = 200
        screen.blit(playerImg, (playerX, dplayerY))
        dplayerY = dplayerY
        d_wheel_speed = velocity / 3
        front_wheel.angle -= d_wheel_speed
        back_wheel.angle -= d_wheel_speed
        front_wheel.show(playerX + 395, playerY + 130, velocity)
        back_wheel.show(playerX + 115, playerY + 130, velocity)
        print(gear, clutch_pressed, RPM, velocity, distance)

    # ___Ekran Końcowy___
    if game_state == "EK":
        pass
    # ta linijka robi odświeżenie ekranu
    pygame.display.update()
