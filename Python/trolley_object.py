import pygame
import time

class Trolley:
    def __init__(self, x, y, width, height, min_x, max_x):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_x = min_x
        self.max_x = max_x
        self.speed = 1
        self.emergency_stop = False
        self.last_update = time.time()

    def move(self, direction, delta_time):
        if self.emergency_stop:
            return
        distance = self.speed * direction * delta_time
        new_x = self.x + distance
        self.x = max(self.min_x, min(self.max_x, new_x))
    
    def set_speed(self, speed):
        self.speed = max(speed, 1)
    
    def emergency_stop_action(self):
        self.emergency_stop = True
        self.speed = 0
    
    def release_emergency_stop(self):
        self.emergency_stop = False
    
    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
