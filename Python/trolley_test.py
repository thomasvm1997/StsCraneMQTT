import unittest
from unittest.mock import Mock, patch
import json
from trolley_object import Trolley, TrolleyMovement
from trolley import TrolleyController


class TestTrolley(unittest.TestCase):

    def setUp(self):
        """Initialize a Trolley object before each test."""
        self.trolley = Trolley(x=100, width=50, height=20, min_x=0, max_x=500)

    def test_initial_state(self):
        """Test that the trolley initializes with default values."""
        self.assertEqual(self.trolley.speed, 0.2)
        self.assertFalse(self.trolley.emergency_stop)
        self.assertEqual(self.trolley.direction, TrolleyMovement.NEUTRAL)

    def test_increment_speed(self):
        """Test speed increment, ensuring it doesn't exceed max speed."""
        for _ in range(10):  # Increment multiple times
            self.trolley.increment_speed()

        self.assertEqual(self.trolley.speed, 2.0)  # Max speed
        self.trolley.increment_speed()  # Try exceeding max speed
        self.assertEqual(self.trolley.speed, 2.0)

    def test_emergency_stop(self):
        """Test that the emergency stop sets speed to 0."""
        self.trolley.increment_speed()
        self.trolley.stop()
        self.assertTrue(self.trolley.emergency_stop)
        self.assertEqual(self.trolley.speed, 0.0)

    def test_update_position_forward(self):
        """Test that the trolley updates position correctly when moving forward."""
        self.trolley.set_trolley_state(TrolleyMovement.FORWARD)
        initial_x = self.trolley.x
        self.trolley.update_position(1)  # Simulate 1 second of movement
        self.assertEqual(self.trolley.x, initial_x + self.trolley.speed)

    def test_update_position_backward(self):
        """Test that the trolley updates position correctly when moving backward."""
        self.trolley.set_trolley_state(TrolleyMovement.BACKWARD)
        initial_x = self.trolley.x
        self.trolley.update_position(1)  # Simulate 1 second of movement
        self.assertEqual(self.trolley.x, initial_x - self.trolley.speed)

    def test_update_position_no_movement(self):
        """Test that no movement occurs when the trolley is neutral."""
        self.trolley.set_trolley_state(TrolleyMovement.NEUTRAL)
        initial_x = self.trolley.x
        self.trolley.update_position(1)
        self.assertEqual(self.trolley.x, initial_x)


class TestTrolleyController(unittest.TestCase):

    @patch('paho.mqtt.client.Client')
    def setUp(self, MockMQTTClient):
        """Set up a TrolleyController with a mocked MQTT client."""
        self.mock_client = MockMQTTClient.return_value
        self.controller = TrolleyController()

    def test_on_message_forward(self):
        """Test that the trolley moves forward when receiving a forward command."""
        payload = json.dumps({"component": "trolley", "state": "forward"})
        msg = Mock()
        msg.payload = payload.encode()

        self.controller.on_message(self.mock_client, None, msg)
        self.assertEqual(self.controller.trolley.direction, TrolleyMovement.FORWARD)

    def test_on_message_backward(self):
        """Test that the trolley moves backward when receiving a backward command."""
        payload = json.dumps({"component": "trolley", "state": "backward"})
        msg = Mock()
        msg.payload = payload.encode()

        self.controller.on_message(self.mock_client, None, msg)
        self.assertEqual(self.controller.trolley.direction, TrolleyMovement.BACKWARD)

    def test_on_message_increment_speed(self):
        """Test that increment_speed increases trolley speed."""
        payload = json.dumps({"command": "increment_speed"})
        msg = Mock()
        msg.payload = payload.encode()

        self.controller.on_message(self.mock_client, None, msg)
        self.assertEqual(self.controller.trolley.speed, 0.4)  # Default increment is 0.2

    def test_on_message_emergency_stop(self):
        """Test that the trolley activates emergency stop."""
        payload = json.dumps({"command": "emergency_stop"})
        msg = Mock()
        msg.payload = payload.encode()

        self.controller.on_message(self.mock_client, None, msg)
        self.assertTrue(self.controller.trolley.emergency_stop)
        self.assertEqual(self.controller.trolley.speed, 0.0)

    def test_on_message_release_stop(self):
        """Test that the trolley releases emergency stop and resets speed."""
        self.controller.trolley.emergency_stop = True  # Simulate emergency stop active
        payload = json.dumps({"command": "release_stop"})
        msg = Mock()
        msg.payload = payload.encode()

        self.controller.on_message(self.mock_client, None, msg)
        self.assertFalse(self.controller.trolley.emergency_stop)
        self.assertEqual(self.controller.trolley.speed, 0.2)  # Reset to minimum speed


if __name__ == "__main__":
    unittest.main()
