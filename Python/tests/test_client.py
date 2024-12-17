import unittest
from unittest.mock import MagicMock, patch
import json
from mqtt_client import on_connect, on_message, data_dict, gantry_locked, spreader_locked, dot_x, dot_y, bottom_dot_x, bottom_dot_y, sts_back_image

GREEN = (0, 255, 0)  # RGB color for green
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
        self.assertTrue(spreader_locked)

    def test_on_message_spreader_unlock(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/spreader/unlock", payload=json.dumps({"status": "unlocked"}).encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertIn("/hub/spreader/unlock", data_dict)
        self.assertEqual(data_dict["/hub/spreader/unlock"], {"status": "unlocked"})
        self.assertFalse(spreader_locked)

    def test_on_message_gantry_handbrake_lock(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/gantry/handbrake/lock", payload=json.dumps({"status": "locked"}).encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertTrue(gantry_locked)

    def test_on_message_gantry_handbrake_release(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/gantry/handbrake/release", payload=json.dumps({"status": "released"}).encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertFalse(gantry_locked)

    def test_on_message_trolley_location(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/trolley/location", payload=json.dumps({"x": 100}).encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertEqual(dot_x, 100)
        self.assertEqual(dot_y, 200)  # Ensure y-position is unchanged
        self.assertEqual(bottom_dot_x, 400)  # Bottom dot does not move

    def test_on_message_gantry_location_locked(self):
        global gantry_locked, dot_x, bottom_dot_x
        gantry_locked = True
        client = MagicMock()
        msg = MagicMock(topic="/hub/gantry/location", payload=json.dumps({"x": 300}).encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertEqual(dot_x, 300)
        self.assertEqual(bottom_dot_x, 400)  # Bottom dot should not move due to the lock

    def test_on_message_hoist_location(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/hoist/location", payload=json.dumps({"y": 150}).encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertEqual(dot_y, 150)
        self.assertEqual(bottom_dot_y, 150)

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

    def test_on_spreader_lock_changes_color(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/spreader/lock", payload=json.dumps({"status": "locked"}).encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertEqual(sts_back_image.get_at((0, 0)), GREEN)  # Check the color change (top-left pixel)

    def test_on_spreader_unlock_resets_color(self):
        client = MagicMock()
        msg = MagicMock(topic="/hub/spreader/unlock", payload=json.dumps({"status": "unlocked"}).encode('utf-8'))
        
        on_message(client, None, msg)
        
        self.assertNotEqual(sts_back_image.get_at((0, 0)), GREEN)  # Check that the color is not green

if __name__ == '__main__':
    unittest.main()
