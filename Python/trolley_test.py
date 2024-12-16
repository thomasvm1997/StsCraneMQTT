import unittest
from unittest.mock import MagicMock
from trolley import Trolley, handle_mqtt_message

class TestTrolley(unittest.TestCase):
    def setUp(self):
        self.trolley = Trolley()

    def test_initial_state(self):
        self.assertEqual(self.trolley.x, 0.0)
        self.assertEqual(self.trolley.speed, 0.2)
        self.assertEqual(self.trolley.direction, 0)
        self.assertFalse(self.trolley.emergency_stop)

    def test_move_command(self):
        self.trolley.move(1)  # Move right
        self.assertEqual(self.trolley.direction, 1)
        self.trolley.move(-1)  # Move left
        self.assertEqual(self.trolley.direction, -1)
        self.trolley.move(0)  # Invalid direction
        self.assertNotEqual(self.trolley.direction, 0)  # Should not change to 0

    def test_increment_speed(self):
        initial_speed = self.trolley.speed
        self.trolley.increment_speed()
        self.assertEqual(self.trolley.speed, initial_speed + 0.2)

        # Simulate hitting max speed
        for _ in range(10):  # Try increasing speed multiple times
            self.trolley.increment_speed()
        self.assertEqual(self.trolley.speed, self.trolley.max_speed)

    def test_emergency_stop(self):
        self.trolley.move(1)
        self.trolley.emergency_stop = True
        self.trolley.move(1)  # Should not move
        self.assertEqual(self.trolley.direction, 0)
        self.trolley.update_position(1)  # Position should not change
        self.assertEqual(self.trolley.x, 0.0)

    def test_release_emergency_stop(self):
        self.trolley.emergency_stop = True
        self.trolley.move(1)  # Should not move
        self.trolley.release_stop = False
        self.trolley.emergency_stop = False
        self.trolley.move(1)  # Should move now
        self.assertEqual(self.trolley.direction, 1)

    def test_handle_mqtt_message(self):
        # Mock a move command
        message = MagicMock()
        message.payload = b'{"command": "move", "direction": 1}'
        handle_mqtt_message(self.trolley, message)
        self.assertEqual(self.trolley.direction, 1)

        # Mock increment_speed command
        message.payload = b'{"command": "increment_speed"}'
        handle_mqtt_message(self.trolley, message)
        self.assertGreater(self.trolley.speed, 0.2)

        # Mock emergency stop command
        message.payload = b'{"command": "emergency_stop"}'
        handle_mqtt_message(self.trolley, message)
        self.assertTrue(self.trolley.emergency_stop)
        self.assertEqual(self.trolley.direction, 0)

        # Mock release emergency stop command
        message.payload = b'{"command": "release_stop"}'
        handle_mqtt_message(self.trolley, message)
        self.assertFalse(self.trolley.emergency_stop)
        self.assertEqual(self.trolley.speed, 0.2)  # Reset to minimum speed

if __name__ == '__main__':
    unittest.main()
