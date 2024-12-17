import pygame
import time
from enum import Enum


class TrolleyMovement(Enum):
    FORWARD = "forward"
    BACKWARD = "backward"
    NEUTRAL = "neutral"


class Trolley:
    def __init__(self, x, width, height, min_x, max_x):
        self.x = x
        self.width = width
        self.height = height
        self.min_x = min_x
        self.max_x = max_x
        self.speed = 0.2  # Set the initial speed to the minimum speed
        self.max_speed = 2.0  # Maximum speed in m/s
        self.increment = 0.2  # Speed increment value
        self.direction = TrolleyMovement.NEUTRAL  # Current movement direction
        self.emergency_stop = False  # Emergency stop flag
        self.last_update = time.time()

    def move(self, movement):
        """Change the direction of the trolley."""
        if self.emergency_stop:
            print("Cannot move, emergency stop is active!")
            return

        if movement == TrolleyMovement.FORWARD:
            self.direction = TrolleyMovement.FORWARD
            print("Trolley moving forward")
        elif movement == TrolleyMovement.BACKWARD:
            self.direction = TrolleyMovement.BACKWARD
            print("Trolley moving backward")
        else:
            self.direction = TrolleyMovement.NEUTRAL
            self.speed = 0.0
            print("Trolley is in neutral")

    def set_trolley_state(self, state: TrolleyMovement):
        """Set the state (direction) of the trolley."""
        if self.emergency_stop:
            print("Cannot set state, emergency stop is active!")
            return
        self.direction = state
        print(f"Trolley state set to: {state.name}")

    def stop(self):
        """Immediately stop the trolley."""
        self.speed = 0.0
        self.direction = TrolleyMovement.NEUTRAL
        print("Trolley stopped.")

    def increment_speed(self):
        """Increment the speed of the trolley by 0.2 m/s, capped at max_speed."""
        if self.emergency_stop:
            print("Cannot increment speed, emergency stop is active!")
            return

        if self.speed < self.max_speed:
            self.speed = min(round(self.speed + self.min_increment, 2), self.max_speed)
            print(f"Speed increased to {self.speed:.2f} m/s")
        else:
            print("Maximum speed reached")

    def emergency_stop_action(self):
        """Activate the emergency stop, halting all movement."""
        self.emergency_stop = True
        self.stop()
        print("Emergency stop activated.")

    def release_emergency_stop(self):
        """Release the emergency stop and reset speed."""
        self.emergency_stop = False
        self.speed = self.min_increment  # Reset speed to minimum increment
        print("Emergency stop released. Speed reset to minimum (0.2 m/s).")

    def update_position(self, delta_time=0.1):
        """
        Update the trolley's position based on its direction and speed.
        delta_time: Simulates time elapsed since last update (default = 0.1s).
        """
        if self.emergency_stop:
            print("Cannot update position, emergency stop is active!")
            return

        if self.direction == TrolleyMovement.FORWARD:
            self.x = min(self.x + self.speed * delta_time, self.max_x)
        elif self.direction == TrolleyMovement.BACKWARD:
            self.x = max(self.x - self.speed * delta_time, self.min_x)
        else:
            self.speed = 0.0  # Trolley is neutral, no movement

        print(f"Position: {self.x:.2f} meters, Speed: {self.speed:.2f} m/s")

    def render(self, screen):
        """Render the trolley as a red rectangle on the screen."""
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.width, self.height))