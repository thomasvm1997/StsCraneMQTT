import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Adjust the Python path to include the directory where mqtt_client.py is located
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import mqtt_client

class TestMQTTClient(unittest.TestCase):

    @patch('mqtt_client.paho.Client')
    def test_on_connect(self, MockClient):
        client = MockClient()
        mqtt_client.on_connect(client, None, None, 0)
        client.subscribe.assert_called_with("/hub/client", qos=1)

    @patch('mqtt_client.paho.Client')
    def test_on_publish(self, MockClient):
        client = MockClient()
        mqtt_client.on_publish(client, None, 1)
        client.on_publish.assert_called()

    @patch('mqtt_client.paho.Client')
    def test_on_subscribe(self, MockClient):
        client = MockClient()
        mqtt_client.on_subscribe(client, None, 1, [1])
        client.on_subscribe.assert_called()

    @patch('mqtt_client.paho.Client')
    def test_on_message(self, MockClient):
        client = MockClient()
        msg = MagicMock()
        msg.payload.decode.return_value = '{"key": "value"}'
        mqtt_client.on_message(client, None, msg)
        msg.payload.decode.assert_called()
        print("JSON object:", {"key": "value"})

    @patch('mqtt_client.paho.Client')
    def test_on_message_invalid_json(self, MockClient):
        client = MockClient()
        msg = MagicMock()
        msg.payload.decode.return_value = 'invalid json'
        mqtt_client.on_message(client, None, msg)
        msg.payload.decode.assert_called()
        print("Failed to decode JSON: Expecting value: line 1 column 1 (char 0)")

if __name__ == '__main__':
    unittest.main()