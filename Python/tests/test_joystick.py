import time
import paho.mqtt.client as paho
from unittest.mock import patch, MagicMock
import pytest

# Mock keyboard inputs
def mock_keyboard_is_pressed(key):
    neutral_keys = {"a": False, "d": False, "w": False, "s": False, "i": False, "k": False, "1": False, "2": False, "z": False, "x": False}
    return neutral_keys.get(key, False)

@pytest.fixture
def mqtt_client():
    client = MagicMock(spec=paho.Client)
    return client

@patch("keyboard.is_pressed", side_effect=mock_keyboard_is_pressed)
def test_neutral_state(mock_keyboard, mqtt_client):
    from mqtt_joysticks import send_joystick_states

    # Call the function with the mocked client and keyboard
    send_joystick_states(mqtt_client)

    # Verify neutral states were sent
    mqtt_client.publish.assert_any_call("/joysticks/gantry/neutral", "gantry neutral", qos=1)
    mqtt_client.publish.assert_any_call("/joysticks/hoist/neutral", "hoist neutral", qos=1)
    mqtt_client.publish.assert_any_call("/joysticks/trolley/neutral", "trolley neutral", qos=1)
    mqtt_client.publish.assert_any_call("/joysticks/gantry/handbrake/release", "handbrake release", qos=1)
    mqtt_client.publish.assert_any_call("/joysticks/emergency/unlock", "emergency unlock", qos=1)

def test_non_neutral_state(mqtt_client):
    # Example to test if button 'w' is pressed for "hoist up"
    with patch("keyboard.is_pressed", side_effect=lambda key: key == "w"):
        from mqtt_joysticks import send_joystick_states
        send_joystick_states(mqtt_client)

    mqtt_client.publish.assert_any_call("/joysticks/hoist/up", "hoist up", qos=1)
