import pygame
import os
import math
import time


pygame.init()
music_on = True


if music_on:
    music = pygame.mixer.music.load("sounds/game_music.mp3")
    pygame.mixer.music.play(-1)

# SCREEN vars
WIDTH, HEIGHT = 900, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
CAPTION = pygame.display.set_caption("Too Late")

# CAR vars
car_x, car_y = WIDTH / 2, ((HEIGHT / 2) + 100)
max_vel = 0.1 * 240
vel = 0.1 * 20
accel = 0.005 * 5
org_handling = 0.1 * 50
handling = 0.1 * 50
decel = 0.05 * 5
car_drive = False
car_break = False
car_left = False
car_right = False
car_direction = 0
light = False
light_cooldown = 0
honk_cooldown = 0
drive_cooldown = 0
dark = False

# SOUNDS
HONK = pygame.mixer.Sound('sounds/car_horn.wav')
CAR_DRIVE = pygame.mixer.Sound('sounds/car_speeding.wav')


# VEHICLE IMGS
CAR_1 = pygame.image.load(os.path.join("images/car.png"))
CAR_2 = pygame.image.load(os.path.join("images/car_2.png"))
STEERING_WHEEL = pygame.image.load(os.path.join("images/steering-wheel.png"))
LIGHT = pygame.image.load(os.path.join("images/light.png"))
DARK = pygame.image.load(os.path.join("images/dark.png"))
DARK1 = pygame.image.load(os.path.join("images/dark1.png"))
BREAK_UP = pygame.image.load(os.path.join("images/brake_unpressed.png"))
PEDAL_UP = pygame.image.load(os.path.join("images/pedal_unpressed.png"))
BREAK_P = pygame.image.load(os.path.join("images/brake_pressed.png"))
PEDAL_P = pygame.image.load(os.path.join("images/pedal_pressed.png"))

PEDAL = PEDAL_UP
BREAK = BREAK_UP

# BG IMGS
bg_day = pygame.image.load(os.path.join("images/background_day.png")).convert()
bg_night = pygame.image.load(os.path.join("images/background_night.png")).convert()
bg = bg_day

bg_height = bg.get_height()

# GAME vars
tiles = (math.ceil(HEIGHT / bg_height)) + 2
scroll = 0
distance = 0


class Cars():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
    
    def draw(self):
        WIN.blit(self.img, (self.x, self.y))
    
    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()       
        
    def collision(self):
        rectangle = pygame.Rect((self.x, self.y), (self.img.get_width, self.img.get_height))
        




class PlayerCar():
    def __init__(self, img, vel, max_vel, org_handling, handling, car_x, car_y, car_right, car_left, car_direction, accel, decel):
        self.img = img
        self.vel = vel
        self.max_vel = max_vel
        self.org_handling = org_handling
        self.handling = handling
        self.car_x = car_x
        self.car_y = car_y
        self.car_right = car_right
        self.car_left = car_left
        self.car_direction = car_direction
        self.accel = accel
        self.decel = decel

    def collision(self):
        rect = pygame.Rect(car_x, car_y, self.img.get_width(), self.img.get_height())
        pygame.draw.rect(WIN, (255, 0, 0), rect, 2)
        if car_x >= (WIDTH - CAR_2.get_width()) - 210:
            print('crashed!')

        if car_x <= 210:
            print('crashed!')

# image = pygame.transform.rotate(image, 180)



start = time.time()


def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect


def light_detection():
    global light
    global light_cooldown

    if light_cooldown == 0:
        if light:
            light = False
        elif not light:
            light = True
        light_cooldown += 5
    elif light_cooldown > 0:
        light_cooldown -= 1



def day_night():
    global bg, bg_day, bg_night, dark
    if bg == bg_night:
        dark = True

    day_night_cooldown = 0
    if math.ceil(time.time() - start) % 60 == 0:
        if day_night_cooldown == 0:
            if bg == bg_day:
                bg = bg_night
                day_night_cooldown += 10
            elif bg == bg_night:
                bg = bg_day
                dark = False
                day_night_cooldown += 10
        if day_night_cooldown > 0:
            day_night_cooldown -= 1

def main():
    global car_x, car_y
    global vel, handling
    global scroll
    global car_drive, car_break
    global car_direction
    global car_left, car_right
    global honk_cooldown, drive_cooldown
    global CAR_2, STEERING_WHEEL, BREAK, PEDAL
    global  distance
    global bg, bg_day, bg_night

    


    player = PlayerCar(CAR_2, vel, max_vel, org_handling, handling, car_x, car_y, car_right, car_left,
                       car_direction, accel, decel)
    run = True



    FPS = 60
    clock = pygame.time.Clock()

    def draw_win():
        global CAR_2, STEERING_WHEEL, BREAK, PEDAL
        global scroll
        global tiles
        global distance
        global car_direction
        global light, dark, bg, bg_day, bg_night

        FontSize = 45
        font = pygame.font.SysFont('Comicsans', FontSize)

        for i in range(0, tiles):
            WIN.blit(bg, (0, (i * bg_height + scroll) - 400))

        distance += 0.0005 * vel

        if abs(scroll) > bg_height:
            scroll = 0

        WIN.blit(CAR_2, (car_x, car_y))

        if light:
            WIN.blit(LIGHT, (car_x - 20, car_y - 63))
            WIN.blit(LIGHT, (car_x + 15, car_y - 63))
            if dark:
                WIN.blit(DARK1, (0, 0))
        elif dark:
            WIN.blit(DARK, (0, 0))

        # player.collision()

        rotated_steering_wheel = rot_center(STEERING_WHEEL, (car_direction), (WIDTH - (STEERING_WHEEL.get_width())),
                                            (HEIGHT - (STEERING_WHEEL.get_height())))
        WIN.blit(rotated_steering_wheel[0], rotated_steering_wheel[1])
        WIN.blit(BREAK, (20, HEIGHT-(BREAK.get_height() + 20)))
        WIN.blit(PEDAL, (100, HEIGHT-(PEDAL.get_height() + 20)))
        if vel <= 100:
            speed_label = font.render(f"SPEED: {math.floor(vel * 10)}mph" , True, (0, 255, 0))
        if 100 < vel < max_vel - 30:
            speed_label = font.render(f"SPEED: {math.floor(vel * 10)}mph" , True, (255, 255, 0))
        if vel >= max_vel - 30:
            speed_label = font.render(f"SPEED: {math.floor(vel * 10)}mph" , True, (255, 0, 0))
        distance_label = font.render(f"DISTANCE: {round(distance/2, 2)}miles", True, (255, 255,0))
        WIN.blit(speed_label, (10, 10))
        WIN.blit(distance_label, (10, 45))

        pygame.display.update()

    print("Game starting...")
    while run:
        clock.tick(FPS)
        draw_win()
        if vel == max_vel:
            print("MAX SPEED")
#        print(vel)
#        print(light)
        day_night()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Game exited")
                end = time.time()
                print(str(end - start) + 'secs')
                print(str(round(distance, 2)) + ' miles')
                run = False

        # KEY INPUT
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] and car_x < (WIDTH - CAR_2.get_width()) - 210:
            car_x += handling
            car_right = True
            car_direction -= 5

        if keys[pygame.K_a] and car_x > 210:
            car_x -= handling
            car_left = True
            car_direction += 5

        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            car_left = False
            car_right = False
            if car_direction != 0:
                if car_direction > 0:
                    car_direction -= 5
                if car_direction < 0:
                    car_direction += 5

        if keys[pygame.K_w] and car_y > 0:
            car_drive = True
        if not keys[pygame.K_w]:
            car_drive = False

        if keys[pygame.K_s] and car_y < HEIGHT - CAR_2.get_height():
            car_break = True
        if not keys[pygame.K_s]:
            car_break = False

        if keys[pygame.K_l]:
            light_detection()

        if keys[pygame.K_h]:
            if honk_cooldown == 0:
                HONK.play()
                honk_cooldown += 1
            elif honk_cooldown > 0:
                honk_cooldown -= 0.5


        if car_drive:
            scroll += vel
            if vel <= max_vel:
                vel += accel
        if not car_drive:
            if vel >= decel/20:
                vel -= decel/20
            scroll += vel
        if car_break:
            if vel >= decel/3:
                vel -= decel/3

        if vel > 0.1 * 100:
            if handling > org_handling - 2:
                handling -= 2
        if vel < 0.1 * 100:
            if handling < org_handling:
                handling += (org_handling - handling)

        if car_drive:
            PEDAL = PEDAL_P
        elif not car_drive:
            PEDAL = PEDAL_UP
        if car_break:
            BREAK = BREAK_P
        elif not car_break:
            BREAK = BREAK_UP

#        print(drive_cooldown)
        if car_drive:
            if drive_cooldown == 0:
                CAR_DRIVE.play()
                drive_cooldown += 1600
        if drive_cooldown > 0:
            drive_cooldown -= 1



    pygame.quit()


if __name__ == "__main__":
    main()
