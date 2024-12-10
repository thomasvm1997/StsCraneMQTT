import unittest
from unittest.mock import MagicMock, patch
import json
from mqtt_client import on_connect, on_message, data_dict, topics

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

    @patch('paho.mqtt.client.Client')
    def test_on_connect_success(self, mock_client):
        client = MagicMock()
        on_connect(client, None, None, 0)
        for topic in topics:
            client.subscribe.assert_any_call(topic, qos=1)

    @patch('paho.mqtt.client.Client')
    def test_on_connect_failure(self, mock_client):
        client = MagicMock()
        on_connect(client, None, None, 1) 
        client.subscribe.assert_not_called()

    @patch('paho.mqtt.client.Client')
    def test_on_connect_subscribe_all_topics(self, mock_client):
        client = MagicMock()
        on_connect(client, None, None, 0)
        for topic in topics:
            client.subscribe.assert_any_call(topic, qos=1)

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

    def test_on_message_invalid_json(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/gantry/location", payload="invalid json".encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertIn("/hub/gantry/location", data_dict)
        self.assertEqual(data_dict["/hub/gantry/location"], "invalid json")

    def test_on_message_non_json_payload(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/spreader/lock", payload="status=locked".encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertIn("/hub/spreader/lock", data_dict)
        self.assertEqual(data_dict["/hub/spreader/lock"], "status=locked")

    def test_on_message_invalid_json_format(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/spreader/widen", payload="status=invalid".encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertIn("/hub/spreader/widen", data_dict)
        self.assertEqual(data_dict["/hub/spreader/widen"], "status=invalid")

    def test_on_message_non_dict_payload(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/trolley/location", payload="Trolley Location Data".encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertIn("/hub/trolley/location", data_dict)
        self.assertEqual(data_dict["/hub/trolley/location"], "Trolley Location Data")

    @patch('paho.mqtt.client.Client')
    def test_client_loop_start_stop(self, mock_client):
        client = MagicMock()
        
        client.loop_start()
        client.loop_start.assert_called_once()
        
        client.loop_stop()
        client.loop_stop.assert_called_once()

    def test_correct_topics_subscription(self):
        client = MagicMock()
        on_connect(client, None, None, 0)
        
        expected_topics = [
            "/hub/gantry/handbrake/lock",
            "/hub/gantry/handbrake/release",
            "/hub/gantry/location",
            "/hub/hoist/location",
            "/hub/trolley/location",
            "/hub/spreader/widen",
            "/hub/spreader/narrow",
            "/hub/spreader/lock",
            "/hub/spreader/unlock"
        ]
        for topic in expected_topics:
            client.subscribe.assert_any_call(topic, qos=1)

    def test_on_message_invalid_topic(self):
        client = MagicMock()
        msg = MagicMock(topic="/unknown/topic", payload=json.dumps({"data": "ignored"}).encode('utf-8'))
        on_message(client, None, msg)
    
        self.assertNotIn("/unknown/topic", data_dict)

    def test_on_message_non_utf8_payload(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/hoist/location", payload=b'\x80\x81\x82')  # Invalid UTF-8 data
        
        on_message(client, None, msg)
        self.assertIn("/hub/hoist/location", data_dict)
        self.assertEqual(data_dict["/hub/hoist/location"], b'\x80\x81\x82')

    def test_on_message_special_characters_in_payload(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/gantry/handbrake/lock", payload=json.dumps({"status": "locked$", "time": "2024-12-10"}).encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertIn("/hub/gantry/handbrake/lock", data_dict)
        self.assertEqual(data_dict["/hub/gantry/handbrake/lock"], {"status": "locked$", "time": "2024-12-10"})

    def test_on_message_numeric_payload(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/spreader/narrow", payload=json.dumps({"level": 5}).encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertIn("/hub/spreader/narrow", data_dict)
        self.assertEqual(data_dict["/hub/spreader/narrow"], {"level": 5})

    def test_on_message_special_characters_in_topic(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/spreader/narrow/lock_@#%!", payload=json.dumps({"status": "locked"}).encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertIn("/hub/spreader/narrow/lock_@#%!", data_dict)
        self.assertEqual(data_dict["/hub/spreader/narrow/lock_@#%!"], {"status": "locked"})

if __name__ == '__main__':
    unittest.main()
