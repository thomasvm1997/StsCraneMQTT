import unittest
from unittest.mock import MagicMock, patch
import json
from mqtt_client import on_connect, on_message, data_dict

class TestMQTTSubscriptions(unittest.TestCase):

    @patch('paho.mqtt.client.Client')
    def test_subscription_gantry_handbrake_lock(self, mock_client):
        client = MagicMock()
        on_connect(client, None, None, 0)
        client.subscribe.assert_any_call("/hub/gantry/handbrake/lock", qos=1)

    @patch('paho.mqtt.client.Client')
    def test_subscription_gantry_handbrake_release(self, mock_client):
        client = MagicMock()
        on_connect(client, None, None, 0)
        client.subscribe.assert_any_call("/hub/gantry/handbrake/release", qos=1)

    @patch('paho.mqtt.client.Client')
    def test_subscription_gantry_location(self, mock_client):
        client = MagicMock()
        on_connect(client, None, None, 0)
        client.subscribe.assert_any_call("/hub/gantry/location", qos=1)

    @patch('paho.mqtt.client.Client')
    def test_subscription_hoist_location(self, mock_client):
        client = MagicMock()
        on_connect(client, None, None, 0)
        client.subscribe.assert_any_call("/hub/hoist/location", qos=1)

    @patch('paho.mqtt.client.Client')
    def test_subscription_trolley_location(self, mock_client):
        client = MagicMock()
        on_connect(client, None, None, 0)
        client.subscribe.assert_any_call("/hub/trolley/location", qos=1)

    @patch('paho.mqtt.client.Client')
    def test_subscription_spreader_widen(self, mock_client):
        client = MagicMock()
        on_connect(client, None, None, 0)
        client.subscribe.assert_any_call("/hub/spreader/widen", qos=1)

    @patch('paho.mqtt.client.Client')
    def test_subscription_spreader_narrow(self, mock_client):
        client = MagicMock()
        on_connect(client, None, None, 0)
        client.subscribe.assert_any_call("/hub/spreader/narrow", qos=1)

    @patch('paho.mqtt.client.Client')
    def test_subscription_spreader_lock(self, mock_client):
        client = MagicMock()
        on_connect(client, None, None, 0)
        client.subscribe.assert_any_call("/hub/spreader/lock", qos=1)

    @patch('paho.mqtt.client.Client')
    def test_subscription_spreader_unlock(self, mock_client):
        client = MagicMock()
        on_connect(client, None, None, 0)
        client.subscribe.assert_any_call("/hub/spreader/unlock", qos=1)

class TestMQTTMessages(unittest.TestCase):

    def test_on_message_gantry_location(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/gantry/location", payload=json.dumps({"x": 10, "y": 20}).encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertIn("/hub/gantry/location", data_dict)
        self.assertEqual(data_dict["/hub/gantry/location"], {"x": 10, "y": 20})

    def test_on_message_spreader_lock(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/spreader/lock", payload=json.dumps({"status": "locked"}).encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertIn("/hub/spreader/lock", data_dict)
        self.assertEqual(data_dict["/hub/spreader/lock"], {"status": "locked"})

    def test_on_message_invalid_topic(self):
        client = MagicMock()
        msg = MagicMock(topic="/unknown/topic", payload=json.dumps({"data": "ignored"}).encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertNotIn("/unknown/topic", data_dict)

    def test_on_message_empty_payload(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/gantry/location", payload=b'')
        
        on_message(client, None, msg)
        
        self.assertIn("/hub/gantry/location", data_dict)
        self.assertEqual(data_dict["/hub/gantry/location"], '')

if __name__ == '__main__':
    unittest.main()
