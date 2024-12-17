import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Adjust the Python path to include the directory where mqtt_joysticks.py is located
sys.path.insert(0, r'C:\Users\tjste\OneDrive\Bureaublad\Hogeschool Rotterdam\wp6\st-1-d-wx1-2425-1-t14-shark\Python')

import mqtt_joysticks

class TestMQTTJoysticks(unittest.TestCase):

    @patch('mqtt_joysticks.paho.Client')
    def test_on_connect(self, MockClient):
        client = MockClient()
        mqtt_joysticks.on_connect(client, None, None, 0)
        client.on_connect.assert_called()

    @patch('mqtt_joysticks.paho.Client')
    def test_on_publish(self, MockClient):
        client = MockClient()
        mqtt_joysticks.on_publish(client, None, 1)
        client.on_publish.assert_called()

    @patch('mqtt_joysticks.paho.Client')
    def test_on_subscribe(self, MockClient):
        client = MockClient()
        mqtt_joysticks.on_subscribe(client, None, 1, 0)
        client.on_subscribe.assert_called()

    @patch('mqtt_joysticks.paho.Client')
    def test_on_message(self, MockClient):
        client = MockClient()
        msg = MagicMock()
        mqtt_joysticks.on_message(client, None, msg)
        client.on_message.assert_called()

    @patch('mqtt_joysticks.keyboard.is_pressed')
    @patch('mqtt_joysticks.paho.Client')
    def test_check_joysticks(self, MockClient, MockKeyboard):
        client = MockClient()
        MockKeyboard.side_effect = [True, False, False, False, False, False, False, False, False, False, KeyboardInterrupt]
        mqtt_joysticks.check_joysticks(client)
        client.publish.assert_called_with("/joystick/gantry", payload="joystick gantry forward", qos=1)

if __name__ == '__main__':
    unittest.main()