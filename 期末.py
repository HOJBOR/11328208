import pygame
import random

# 初始化 Pygame
pygame.init()

# 遊戲參數
WIDTH, HEIGHT = 800, 600
FPS = 60
BALL_SPEED = [4, -4]
PADDLE_SPEED = 6

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 初始化遊戲窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("打磚塊小遊戲")
clock = pygame.time.Clock()

# 遊戲物件
class Ball:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed

    def move(self):
        self.x += self.speed[0]
        self.y += self.speed[1]

        # 碰撞邊界檢測
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.speed[0] *= -1
        if self.y - self.radius <= 0:
            self.speed[1] *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and self.x + self.width < WIDTH:
            self.x += PADDLE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

class Brick:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.visible = True

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# 創建物件
ball = Ball(WIDTH // 2, HEIGHT // 2, 10, BALL_SPEED)
paddle = Paddle(WIDTH // 2 - 50, HEIGHT - 30, 100, 10)
bricks = [
    Brick(x * 100 + 10, y * 30 + 10, 80, 20, random.choice([RED, GREEN, BLUE]))
    for x in range(7) for y in range(5)
]

# 遊戲主循環
running = True
while running:
    screen.fill(BLACK)
    clock.tick(FPS)

    # 事件處理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    paddle.move(keys)

    # 移動小球
    ball.move()

    # 小球與滑板碰撞
    if (paddle.x < ball.x < paddle.x + paddle.width) and \
       (paddle.y < ball.y + ball.radius < paddle.y + paddle.height):
        ball.speed[1] *= -1

    # 小球與磚塊碰撞
    for brick in bricks:
        if brick.visible and brick.x < ball.x < brick.x + brick.width and \
           brick.y < ball.y < brick.y + brick.height:
            ball.speed[1] *= -1
            brick.visible = False

    # 判斷輸贏
    if ball.y > HEIGHT:
        print("遊戲結束！你輸了！")
        running = False

    if all(not brick.visible for brick in bricks):
        print("恭喜過關！")
        running = False

    # 繪製物件
    ball.draw(screen)
    paddle.draw(screen)
    for brick in bricks:
        brick.draw(screen)

    pygame.display.flip()

pygame.quit()
