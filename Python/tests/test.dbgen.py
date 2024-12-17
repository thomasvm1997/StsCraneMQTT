import unittest
import sqlite3
import json
import time
import sys
from unittest.mock import MagicMock

# # Voeg het pad naar de module toe
# sys.path.append('/c:/Users/tjste/OneDrive/Bureaublad/Hogeschool Rotterdam/wp6/st-1-d-wx1-2425-1-t14-shark/Python')

# from db_generator import insert_message, log_emergency, on_connect, on_message, client, SUBSCRIPTIONS

class TestDBGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up a test database
        cls.conn = sqlite3.connect(':memory:')
        cls.cursor = cls.conn.cursor()
        cls.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Topics (
            id INTEGER PRIMARY KEY,
            topic_name TEXT UNIQUE,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        cls.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Messages (
            id INTEGER PRIMARY KEY,
            topic_id INTEGER,
            payload TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (topic_id) REFERENCES Topics (id)
        )
        ''')
        cls.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Emergencies (
            id INTEGER PRIMARY KEY,
            start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            end_time DATETIME
        )
        ''')
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_insert_message(self):
        insert_message('test/topic', '{"key": "value"}')
        self.cursor.execute('SELECT * FROM Topics WHERE topic_name = ?', ('test/topic',))
        topic = self.cursor.fetchone()
        self.assertIsNotNone(topic)
        self.cursor.execute('SELECT * FROM Messages WHERE topic_id = ?', (topic[0],))
        message = self.cursor.fetchone()
        self.assertIsNotNone(message)
        self.assertEqual(message[2], '{"key": "value"}')

    def test_log_emergency(self):
        start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        log_emergency(start_time)
        self.cursor.execute('SELECT * FROM Emergencies WHERE start_time = ?', (start_time,))
        emergency = self.cursor.fetchone()
        self.assertIsNotNone(emergency)
        self.assertEqual(emergency[1], start_time)

    def test_on_connect(self):
        mock_client = MagicMock()
        on_connect(mock_client, None, None, 0)
        for topic in SUBSCRIPTIONS:
            mock_client.subscribe.assert_any_call(topic, qos=1)

    def test_on_message(self):
        mock_client = MagicMock()
        msg = MagicMock()
        msg.topic = '/joysticks/gantry/left'
        msg.payload = json.dumps({"key": "value"}).encode('utf-8')
        on_message(mock_client, None, msg)
        self.cursor.execute('SELECT * FROM Topics WHERE topic_name = ?', (msg.topic,))
        topic = self.cursor.fetchone()
        self.assertIsNotNone(topic)
        self.cursor.execute('SELECT * FROM Messages WHERE topic_id = ?', (topic[0],))
        message = self.cursor.fetchone()
        self.assertIsNotNone(message)
        self.assertEqual(message[2], msg.payload.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()