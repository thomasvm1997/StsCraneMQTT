import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Adjust the Python path to include the directory where mqtt_hub.py is located
sys.path.insert(0, r'C:\Users\tjste\OneDrive\Bureaublad\Hogeschool Rotterdam\wp6\st-1-d-wx1-2425-1-t14-shark\Python')

import mqtt_hub

class TestMQTTHub(unittest.TestCase):

    @patch('mqtt_hub.paho.Client')
    def test_on_connect(self, MockClient):
        client = MockClient()
        mqtt_hub.on_connect(client, None, None, 0)
        for topic in mqtt_hub.TOPIC_MAPPING.keys():
            client.subscribe.assert_any_call(topic, qos=1)

    @patch('mqtt_hub.paho.Client')
    def test_on_publish(self, MockClient):
        client = MockClient()
        mqtt_hub.on_publish(client, None, 1)
        client.on_publish.assert_called()

    @patch('mqtt_hub.paho.Client')
    def test_on_subscribe(self, MockClient):
        client = MockClient()
        mqtt_hub.on_subscribe(client, None, 1, [1])
        client.on_subscribe.assert_called()

    @patch('mqtt_hub.paho.Client')
    def test_on_message(self, MockClient):
        client = MockClient()
        msg = MagicMock()
        msg.topic = "/joystick/gantry"
        msg.payload.decode.return_value = '{"action": "move gantry forward"}'
        mqtt_hub.on_message(client, None, msg)
        msg.payload.decode.assert_called()
        client.publish.assert_any_call("/hub/joystick/gantry", payload='{"action": "move gantry forward"}', qos=1)
        client.publish.assert_any_call("/hub/client", payload='{"action": "move gantry forward"}', qos=1)

    @patch('mqtt_hub.paho.Client')
    def test_on_message_invalid_json(self, MockClient):
        client = MockClient()
        msg = MagicMock()
        msg.topic = "/joystick/gantry"
        msg.payload.decode.return_value = 'invalid json'
        mqtt_hub.on_message(client, None, msg)
        msg.payload.decode.assert_called()
        client.publish.assert_not_called()

if __name__ == '__main__':
    unittest.main()