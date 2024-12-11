import json
import paho.mqtt.client as paho
from unittest.mock import MagicMock
import pytest

@pytest.fixture
def mqtt_client():
    client = MagicMock(spec=paho.Client)
    return client

def test_neutral_state_forwarding(mqtt_client):
    from mqtt_hub import on_message, PUBLISH_TOPICS

    # Mock a neutral message for the hoist
    neutral_topic = "/joysticks/hoist/neutral"
    payload = json.dumps({"state": "neutral"})

    # Create a fake MQTT message
    msg = MagicMock()
    msg.topic = neutral_topic
    msg.payload = payload.encode("utf-8")

    # Call the message handler
    on_message(mqtt_client, None, msg)

    # Verify it forwards to the appropriate hub topic
    target_topic = PUBLISH_TOPICS[neutral_topic]
    mqtt_client.publish.assert_called_with(target_topic, payload, qos=1)

def test_non_neutral_forwarding(mqtt_client):
    from mqtt_hub import on_message, PUBLISH_TOPICS

    # Mock a "hoist up" message
    hoist_up_topic = "/joysticks/hoist/up"
    payload = json.dumps({"state": "up"})

    # Create a fake MQTT message
    msg = MagicMock()
    msg.topic = hoist_up_topic
    msg.payload = payload.encode("utf-8")

    # Call the message handler
    on_message(mqtt_client, None, msg)

    # Verify it forwards to the appropriate hub topic
    target_topic = PUBLISH_TOPICS[hoist_up_topic]
    mqtt_client.publish.assert_called_with(target_topic, payload, qos=1)
