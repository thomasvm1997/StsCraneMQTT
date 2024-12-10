import unittest
from trolley_object import Trolley

class TestTrolley(unittest.TestCase):

    #create new trolley
    def setUp(self):    
        self.trolley = Trolley(x=100, y=300, width=50, height=20, min_x=50, max_x=750)

    #test trolley position
    def test_initial_position(self):
        self.assertEqual(self.trolley.x, 100)
        self.assertEqual(self.trolley.y, 300)
        self.assertEqual(self.trolley.min_x, 50)
        self.assertEqual(self.trolley.max_x, 750)

    #test speed
    def test_set_speed(self):
        self.trolley.set_speed(2)
        self.assertEqual(self.trolley.speed, 2)

    #test emergency stop
    def test_emergency_stop(self):
        self.trolley.set_speed(2)
        self.trolley.emergency_stop_action()
        self.assertTrue(self.trolley.emergency_stop)
        self.assertEqual(self.trolley.speed, 0)


    #test if emergency stop releases correctly
    def test_release_emergency_stop(self):
        self.trolley.emergency_stop_action()
        self.trolley.release_emergency_stop()
        self.assertFalse(self.trolley.emergency_stop)

    #check if trolley moves within boundaries
    def test_movement_within_boundaries(self):
        self.trolley.set_speed(1)
        self.trolley.move(1, 1)  #move right for 1s
        self.assertEqual(self.trolley.x, 101)

        self.trolley.move(-1, 2)  #move left for 2s
        self.assertEqual(self.trolley.x, 99)

    #check if trolley doesnt move outside boundaries
    def test_movement_outside_boundaries(self):
        self.trolley.set_speed(1)
        self.trolley.move(-1, 100)  #attempt to move left beyond min_x
        self.assertEqual(self.trolley.x, self.trolley.min_x)

        self.trolley.move(1, 1000)  #attempt to move right beyond max_x
        self.assertEqual(self.trolley.x, self.trolley.max_x)

if __name__ == "__main__":
    unittest.main()
