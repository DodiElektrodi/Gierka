import pygame
import math
import random

# załączam pygame
pygame.init()
# ustawiam wielkość ekranu
screen_width, screen_height = 900, 600
screen = pygame.display.set_mode((screen_width, screen_height))
# ustawiam nazwę i miniature
pygame.display.set_caption("Blok Ekipa Drag Race Game")
icon = pygame.image.load("Grafiki/sport-car.png")
pygame.display.set_icon(icon)

# Gracz
playerImg = pygame.image.load("Grafiki/Player_car.png")
playerX = -200
playerY = 150
# Parametry fury
gear_box = {0: float('inf'), 1: 27.5, 2: 13.7, 3: 9.1, 4: 7.4, 5: 5.3, 6: 4.37}

# zegary
clock_img = pygame.image.load("Grafiki/Cloks.png")
pointer_img = pygame.image.load("Grafiki/Pointer.png")

# ekrany
start_screen_sup = pygame.image.load("Grafiki/Start_img_SUP.png")
false_start = pygame.image.load("Grafiki/False_start.png")
dead_engine = pygame.image.load("Grafiki/Dead_engine.png")
win_screen = pygame.image.load("Grafiki/Win.png")

pygame.display.set_caption('Show Text')
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('GeeksForGeeks', True, (0, 255, 0), (0, 0, 128))
textRect = text.get_rect()

# Otoczenie
background_img = pygame.image.load("Grafiki/Back_ground.png")
line = pygame.image.load("Grafiki/Line.png")

# Cyferki do odliczania
num_0 = pygame.image.load("Grafiki/num_0.png")
num_1 = pygame.image.load("Grafiki/num_1.png")
num_2 = pygame.image.load("Grafiki/num_2.png")
num_3 = pygame.image.load("Grafiki/num_3.png")


class wheel_class:
    def __init__(self, image):
        self.image = image
        self.angle = 0

    def show(self, pos_x, pos_y, speed):
        vibration = (random.random() * 2 - 1) * speed / 55
        img_copy = pygame.transform.rotate(self.image, self.angle)
        screen.blit(img_copy,
                    (pos_x - img_copy.get_width() // 2 + vibration,
                     pos_y - img_copy.get_height() // 2 + vibration))


player_wheel = pygame.image.load("Grafiki/wheel_template.png")
front_wheel = wheel_class(player_wheel)
back_wheel = wheel_class(player_wheel)


def draw_speed_pointer(x, y, v):
    pointer_copy = pygame.transform.rotate(pointer_img, 120 - v * 0.98)
    screen.blit(pointer_copy,
                (x - pointer_copy.get_width() // 2,
                 y - pointer_copy.get_height() // 2))


def draw_rpm_pointer(x_pos, y_pos, r):
    pointer_copy = pygame.transform.rotate(pointer_img, 120 - r * 0.029925)
    screen.blit(pointer_copy,
                (x_pos - pointer_copy.get_width() // 2,
                 y_pos - pointer_copy.get_height() // 2))


def gear_shift(num):
    global gear, gear_shifted
    if not clutch_pressed:
        print("Honk!!!")
    else:
        gear_shifted = num - gear
        gear = num


def clutch_release():
    global RPM, clutch_pressed, gear_shifted
    if gear_shifted:
        RPM -= 2500 * gear_shifted
        gear_shifted = 0
    clutch_pressed = False


def d_rpm(r, g):
    optima = math.floor(abs(7250 - r) / 400)
    return int((26 - optima) * (6 / g))


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
tick_time = 0
time = 0
start = 0
false_start_bool = False
engine_fail = False
win = False
# Start
while run:
    # Ustawienia zegara
    dt = clock.tick(30) / 1000  # w sekundach
    screen.fill((255, 255, 255))
    screen.blit(background_img, (start, 0))
    tick_time += 1

    # ___Ekran Początkowy
    if game_state == "EP":
        # pętla eventów
        screen.blit(start_screen_sup, (-40, 0))
        for event in pygame.event.get():
            # to umożliwia wyjście
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game_state = "GP"
                    tick_time = 0

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
            RPM += d_rpm(RPM, gear)
            velocity = rpm_to_speed()
        if clutch_pressed or gear == 0:
            RPM += 70
            if velocity > 0: velocity -= 0.2

        # tu jest zgrywanie ze sobą RPM, distance i velocity
        if velocity < 0: velocity = 0
        distance += velocity * dt / 3.6  # 3.6 daje nam metry na sekundę
        if RPM > 8000:
            RPM -= 155

        # Wyliczanie "skakania" gracza
        amp = 2 * (random.random() - 0.5)  # zwraca "losową" wartość [-1,1]
        dplayerY = playerY + amp * ((RPM / 4000) * (velocity / 100))
        # tu mamy wyjechanie na środek ekranu na start
        if distance < 8:
            playerX = distance * 50 - 200
        else:
            playerX = 200

        # Rysowanie linij startu/mety
        if distance < 8:
            screen.blit(line, (start + 100, 230))
        elif distance > 250:
            screen.blit(line, (int(900 - ((distance-250) * 25)), 230))

        # Rysowanie zegarów
        screen.blit(clock_img, (0, 0))
        draw_speed_pointer(342, 529, velocity)
        draw_rpm_pointer(562, 524, RPM)

        # Rysowanie gracza
        screen.blit(playerImg, (playerX, dplayerY))
        d_wheel_speed = velocity / 3
        front_wheel.angle -= d_wheel_speed
        back_wheel.angle -= d_wheel_speed
        front_wheel.show(playerX + 395, playerY + 130, velocity)
        back_wheel.show(playerX + 115, playerY + 130, velocity)
        # Wypisanie statystyk
        print(gear, clutch_pressed, RPM, velocity, distance, time)
        start -= velocity * dt * 10
        if start < -8000: start = 0

        # Rysowanie wejścia
        if tick_time <= 90:
            screen.blit(start_screen_sup, (-40, -tick_time * 12))
        elif 90 < tick_time <= 120:
            screen.blit(num_3,
                        ((screen_width - num_3.get_width()) // 2,
                         (screen_height - num_3.get_height()) // 2,))
        elif 120 < tick_time <= 150:
            screen.blit(num_2,
                        ((screen_width - num_2.get_width()) // 2,
                         (screen_height - num_2.get_height()) // 2,))
        elif 150 < tick_time <= 180:
            screen.blit(num_1,
                        ((screen_width - num_1.get_width()) // 2,
                         (screen_height - num_1.get_height()) // 2,))
        elif 180 < tick_time <= 210:
            screen.blit(num_0,
                        ((screen_width - num_0.get_width()) // 2,
                         (screen_height - num_0.get_height()) // 2,))

        # Pomiar czasu
        if tick_time == 180:
            time = 0
        if 0 < distance < 250:
            time += dt

        # Sprawdzam Falstart
        if tick_time < 180 and velocity > 0:
            false_start_bool = True
            tick_time = 1000
        if false_start_bool:
            screen.blit(false_start, (0, min(-1000 + (tick_time - 1000) * 12, -40)))

        # Sprawdzam obroty
        if (RPM < 1000 or RPM > 9000) and not engine_fail :
            engine_fail = True
            tick_time = 1000
        if engine_fail:
            RPM = 0
            if velocity > 0: velocity -= 5
            elif velocity < 0: velocity = 0
            screen.blit(dead_engine, (0, min(-1000 + (tick_time - 1000) * 12, -40)))

        # Wygrana
        if not win and distance > 260 and not (engine_fail or false_start_bool):
            win = True
            tick_time = 1000
            pygame.display.set_caption('Show Text')
            font = pygame.font.Font('freesansbold.ttf', 64)
            text = font.render(str(round(time, 2)), True, (255, 0, 0), (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (480, 430)
        if win:
            screen.blit(win_screen, (0, min(-1000 + (tick_time - 1000) * 12, -40)))
            if (tick_time-1000) > 85: screen.blit(text, textRect)




    # ___Ekran Końcowy___
    if game_state == "EK":
        pass
    # ta linijka robi odświeżenie ekranu
    pygame.display.update()
