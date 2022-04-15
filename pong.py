import pygame as pg
import random
pg.font.init()


WIDTH, HEIGHT = 900, 500
MIDDLE_X, MIDDLE_Y = WIDTH//2, HEIGHT//2

WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Pong!')

FPS = 165

VEL_CHOICES_X = [-3, 3]
VEL_CHOICES_Y_ANY = [-2, -1, 1, 2]
VEL_CHOICES_Y_MINUS = [-2, -1]
VEL_CHOICES_Y_PLUS = [1, 2]
VEL = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

HEALTH_FONT = pg.font.SysFont('arial', 40)
WINNER_FONT = pg.font.SysFont('arial', 100)

LEFT_RECT = pg.Rect(WIDTH//10, HEIGHT//2 - 75, 10, 150)
RIGHT_RECT = pg.Rect(int(WIDTH*0.9), HEIGHT//2 - 75, 10, 150)
PROJECTILE = pg.Rect(WIDTH//2 - 10, HEIGHT//2 - 10, 20, 20)

LEFT_HIT = pg.USEREVENT + 1
RIGHT_HIT = pg.USEREVENT + 2
TOP_HIT = pg.USEREVENT + 3
BOTTOM_HIT = pg.USEREVENT + 4
LEFT_WALL_HIT = pg.USEREVENT + 5
RIGHT_WALL_HIT = pg.USEREVENT + 6


def draw_window(left_health, right_health):
    WIN.fill(BLACK)
    pg.draw.rect(WIN, WHITE, LEFT_RECT)
    pg.draw.rect(WIN, WHITE, RIGHT_RECT)
    pg.draw.rect(WIN, WHITE, PROJECTILE)
    left_health_text = HEALTH_FONT.render(f'Health: {left_health}', True, WHITE)
    right_health_text = HEALTH_FONT.render(f'Health: {right_health}', True, WHITE)

    WIN.blit(left_health_text, (10, 10))
    WIN.blit(right_health_text, (WIDTH - right_health_text.get_width() - 10, 10))

    pg.display.update()


def handle_left_movement(keys_pressed, left):
    if keys_pressed[pg.K_s] and left.y + VEL + left.height < HEIGHT:
        left.y += VEL
    if keys_pressed[pg.K_w] and left.y - VEL > 0:
        left.y -= VEL


def handle_right_movement(keys_pressed, right):
    if keys_pressed[pg.K_DOWN] and right.y + VEL + right.height < HEIGHT:
        right.y += VEL
    if keys_pressed[pg.K_UP] and right.y - VEL > 0:
        right.y -= VEL


def handle_projectile(projectile, left_rect, right_rect, projectile_x_vel, projectile_y_vel):
    projectile.x += projectile_x_vel
    projectile.y += projectile_y_vel
    if left_rect.colliderect(projectile):
        pg.event.post(pg.event.Event(LEFT_HIT))
    elif right_rect.colliderect(projectile):
        pg.event.post(pg.event.Event(RIGHT_HIT))
    elif projectile.y + VEL + projectile.height > HEIGHT:
        pg.event.post(pg.event.Event(BOTTOM_HIT))
    elif projectile.y - VEL < 0:
        pg.event.post(pg.event.Event(TOP_HIT))
    elif projectile.x - VEL < 0:
        pg.event.post(pg.event.Event(LEFT_WALL_HIT))
    elif projectile.x + VEL > WIDTH:
        pg.event.post(pg.event.Event(RIGHT_WALL_HIT))


def draw_winner(winner_text):
    text = WINNER_FONT.render(winner_text, True, WHITE)
    WIN.blit(text, (MIDDLE_X - text.get_width()//2, MIDDLE_Y - text.get_height()//2))
    pg.display.update()
    pg.time.delay(5000)


def main():
    clock = pg.time.Clock()

    projectile_x_vel = random.choice(VEL_CHOICES_X)
    projectile_y_vel = random.choice(VEL_CHOICES_Y_ANY)

    winner_text = ''

    left_health = 3
    right_health = 3

    i = 1

    running = True
    while running:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print('Thanks for playing!')
                pg.quit()

            if event.type == LEFT_HIT or event.type == RIGHT_HIT:
                projectile_x_vel = -projectile_x_vel
                if projectile_y_vel < 0:
                    projectile_y_vel = random.choice(VEL_CHOICES_Y_MINUS)
                elif projectile_y_vel > 0:
                    projectile_y_vel = random.choice(VEL_CHOICES_Y_PLUS)
            if event.type == TOP_HIT or event.type == BOTTOM_HIT:
                projectile_y_vel = -projectile_y_vel

            if PROJECTILE.x - VEL < 0:
                left_health -= 1
                PROJECTILE.x = MIDDLE_X - PROJECTILE.width//2
                PROJECTILE.y = MIDDLE_Y - PROJECTILE.height//2
                projectile_x_vel = random.choice(VEL_CHOICES_X)
                projectile_y_vel = random.choice(VEL_CHOICES_Y_ANY)

            if PROJECTILE.x + VEL > WIDTH:
                right_health -= 1
                PROJECTILE.x = MIDDLE_X - PROJECTILE.width // 2
                PROJECTILE.y = MIDDLE_Y - PROJECTILE.height // 2
                projectile_x_vel = random.choice(VEL_CHOICES_X)
                projectile_y_vel = random.choice(VEL_CHOICES_Y_ANY)

        if left_health <= 0:
            winner_text = 'Right Wins!'
        if right_health <= 0:
            winner_text = 'Left Wins!'
        if winner_text != '':
            draw_winner(winner_text)
            break

        keys_pressed = pg.key.get_pressed()
        
        handle_left_movement(keys_pressed, LEFT_RECT)
        handle_right_movement(keys_pressed, RIGHT_RECT)

        # handle_projectile(PROJECTILE, LEFT_RECT, RIGHT_RECT, projectile_x_vel, projectile_y_vel)

        draw_window(left_health, right_health)

        if i == 1:
            pg.time.delay(1000)
            handle_projectile(PROJECTILE, LEFT_RECT, RIGHT_RECT, projectile_x_vel, projectile_y_vel)
        handle_projectile(PROJECTILE, LEFT_RECT, RIGHT_RECT, projectile_x_vel, projectile_y_vel)
        i += 1

    main()


if __name__ == '__main__':
    main()
