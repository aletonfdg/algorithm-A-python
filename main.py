import pygame
import random
import math
import heapq


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Размеры сетки для алгоритма поиска пути
GRID_SIZE = 20


class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 2
        self.path = []

    def update(self):
        if self.path:
            target_x, target_y = self.path[0]
            self.move_towards(target_x, target_y)
            if math.hypot(target_x - self.x, target_y - self.y) < self.speed:
                self.x, self.y = self.path.pop(0)

    def draw(self, screen):
        car_rect = pygame.Rect(self.x, self.y, 50, 30)
        pygame.draw.rect(screen, RED, car_rect)
        return car_rect

    def set_speed(self, speed):
        self.speed = speed

    def set_angle(self, angle):
        self.angle = angle

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        self.angle = math.degrees(math.atan2(-dy, dx))
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))


class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)


car_spawn_x = random.randint(0, SCREEN_WIDTH - 50)
car_spawn_y = random.randint(0, SCREEN_HEIGHT - 50)
destination_x = random.randint(0, SCREEN_WIDTH)
destination_y = random.randint(0, SCREEN_HEIGHT)


car = Car(car_spawn_x, car_spawn_y)

# Создадим список препятствий
obstacles = []

for _ in range(10):
    x = random.randint(0, SCREEN_WIDTH - 50)
    y = random.randint(0, SCREEN_HEIGHT - 50)
    obstacles.append(Obstacle(x, y, 50, 50))

# Функция для поиска пути с использованием A*
def a_star(start, goal, obstacles):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    grid_width = SCREEN_WIDTH // GRID_SIZE
    grid_height = SCREEN_HEIGHT // GRID_SIZE
    start = (start[0] // GRID_SIZE, start[1] // GRID_SIZE)
    goal = (goal[0] // GRID_SIZE, goal[1] // GRID_SIZE)

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append((current[0] * GRID_SIZE + GRID_SIZE // 2, current[1] * GRID_SIZE + GRID_SIZE // 2))
                current = came_from[current]
            path.reverse()
            return path

        neighbors = [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1)
        ]

        for neighbor in neighbors:
            if 0 <= neighbor[0] < grid_width and 0 <= neighbor[1] < grid_height:
                # Проверяем, что соседняя клетка не занята препятствием
                neighbor_rect = pygame.Rect(neighbor[0] * GRID_SIZE, neighbor[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                if any(obstacle.rect.colliderect(neighbor_rect) for obstacle in obstacles):
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []


running = True
clock = pygame.time.Clock()

# Найдем путь с использованием A*
car.path = a_star((car_spawn_x, car_spawn_y), (destination_x, destination_y), obstacles)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

   
    car.update()

    
    screen.fill(WHITE)

   
    pygame.draw.circle(screen, BLACK, (car_spawn_x, car_spawn_y), 10)

   
    pygame.draw.circle(screen, BLUE, (destination_x, destination_y), 10)

    # Нарисуем путь, если он содержит 2 или более точек
    if len(car.path) > 1:
        pygame.draw.lines(screen, BLACK, False, [(int(x), int(y)) for x, y in car.path], 2)

    # Нарисуем препятствия
    for obstacle in obstacles:
        obstacle.draw(screen)

  
    car_rect = car.draw(screen)


    pygame.display.flip()

    # Ограничим FPS
    clock.tick(60)

pygame.quit()
