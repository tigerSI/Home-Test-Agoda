import Server
from Server import app
from Rate_limiter import Rate_limiter

import unittest
import time

class rate_limited_test(unittest.TestCase):

    def setUp(self):
        Server.rate_limiter = Rate_limiter()
        app.testing = True 

    def tearDown(self):
        app.testing = False

    def test_index(self):
        with app.test_client(self) as tester:
            response = tester.get('/')
            self.assertEqual(response.status_code, 200)

    def test_output_from_city_endpoint(self):
        with app.test_client(self) as tester:
            response = tester.get('/city?city_name=Bangkok&ordering_type=DESC')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'[["Bangkok", "14", "Sweet Suite", 25000], ["Bangkok", "18", "Sweet Suite", 5300], ["Bangkok", "8", "Superior", 2400], ["Bangkok", "6", "Superior", 2000], ["Bangkok", "1", "Deluxe", 1000], ["Bangkok", "15", "Deluxe", 900], ["Bangkok", "11", "Deluxe", 60]]')
            
            response = tester.get('/city?city_name=Bangkok&ordering_type=ASC')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'[["Bangkok", "11", "Deluxe", 60], ["Bangkok", "15", "Deluxe", 900], ["Bangkok", "1", "Deluxe", 1000], ["Bangkok", "6", "Superior", 2000], ["Bangkok", "8", "Superior", 2400], ["Bangkok", "18", "Sweet Suite", 5300], ["Bangkok", "14", "Sweet Suite", 25000]]')
        
    def test_output_from_room_endpoint(self):
        with app.test_client(self) as tester:
            response = tester.get('/room?room_type=Deluxe&ordering_type=DESC')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'[["Ashburn", "21", "Deluxe", 7000], ["Amsterdam", "23", "Deluxe", 5000], ["Ashburn", "17", "Deluxe", 2800], ["Amsterdam", "26", "Deluxe", 2300], ["Amsterdam", "4", "Deluxe", 2200], ["Ashburn", "25", "Deluxe", 1900], ["Ashburn", "12", "Deluxe", 1800], ["Ashburn", "7", "Deluxe", 1600], ["Bangkok", "1", "Deluxe", 1000], ["Bangkok", "15", "Deluxe", 900], ["Bangkok", "11", "Deluxe", 60]]')
            
            response = tester.get('/room?room_type=Deluxe&ordering_type=ASC')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'[["Bangkok", "11", "Deluxe", 60], ["Bangkok", "15", "Deluxe", 900], ["Bangkok", "1", "Deluxe", 1000], ["Ashburn", "7", "Deluxe", 1600], ["Ashburn", "12", "Deluxe", 1800], ["Ashburn", "25", "Deluxe", 1900], ["Amsterdam", "4", "Deluxe", 2200], ["Amsterdam", "26", "Deluxe", 2300], ["Ashburn", "17", "Deluxe", 2800], ["Amsterdam", "23", "Deluxe", 5000], ["Ashburn", "21", "Deluxe", 7000]]')
    
    def test_bad_parameters_city_endpoint(self):
        with app.test_client(self) as tester:
            response = tester.get('/city?city_name=Bangkok&ordering_type=T')
            self.assertEqual(response.status_code, 400)

            response = tester.get('/city?city_name=A&ordering_type=ASC')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'[]')

    def test_bad_parameters_room_endpoint(self):
        with app.test_client(self) as tester:
            response = tester.get('/room?room_type=Deluxe&ordering_type=T')
            self.assertEqual(response.status_code, 400)

            response = tester.get('/room?room_type=D&ordering_type=ASC')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'[]')

    def test_rate_limiter(self):
        with app.test_client(self) as tester:
            for i in range(0, 10):
                response = tester.get('/city?city_name=Bangkok&ordering_type=ASC')
                self.assertEqual(response.status_code, 200)

            response = tester.get('/city?city_name=Bangkok&ordering_type=ASC')
            self.assertEqual(response.status_code, 429)

            time.sleep(5)

            response = tester.get('/city?city_name=Bangkok&ordering_type=ASC')
            self.assertEqual(response.status_code, 200)

    def test_configure_city_default(self):
        with app.test_client(self) as tester:
            tester.post('/city/configure')
            for i in range(50):
                response = tester.get('/city?city_name=Bangkok&ordering_type=ASC')
                self.assertEqual(response.status_code, 200)

            response = tester.get('/city?city_name=Bangkok&ordering_type=ASC')
            self.assertEqual(response.status_code, 429)

            time.sleep(5)

            response = tester.get('/city?city_name=Bangkok&ordering_type=ASC')
            self.assertEqual(response.status_code, 200)

    def test_configure_room_default(self):
        with app.test_client(self) as tester:
            tester.post('/room/configure')
            for i in range(50):
                response = tester.get('/room?room_type=Deluxe&ordering_type=ASC')
                self.assertEqual(response.status_code, 200)

            response = tester.get('/room?room_type=Deluxe&ordering_type=ASC')
            self.assertEqual(response.status_code, 429)

            time.sleep(5)

            response = tester.get('/room?room_type=Deluxe&ordering_type=ASC')
            self.assertEqual(response.status_code, 200)

    def test_configure_city_with_params(self):
        with app.test_client(self) as tester:
            tester.post('/city/configure?interval_time=10&number_requests=2')
            for i in range(2):
                response = tester.get('/city?city_name=Bangkok&ordering_type=ASC')
                self.assertEqual(response.status_code, 200)

            response = tester.get('/city?city_name=Bangkok&ordering_type=ASC')
            self.assertEqual(response.status_code, 429)

            time.sleep(5)

            response = tester.get('/city?city_name=Bangkok&ordering_type=ASC')
            self.assertEqual(response.status_code, 200)

            time.sleep(10)

            for i in range(2):
                response = tester.get('/city?city_name=Bangkok&ordering_type=ASC')
                self.assertEqual(response.status_code, 200)

    def test_configure_room_with_params(self):
        with app.test_client(self) as tester:
            tester.post('/room/configure?interval_time=10&number_requests=2')
            for i in range(2):
                response = tester.get('/room?room_type=Deluxe&ordering_type=ASC')
                self.assertEqual(response.status_code, 200)

            response = tester.get('/room?room_type=Deluxe&ordering_type=ASC')
            self.assertEqual(response.status_code, 429)

            time.sleep(5)

            response = tester.get('/room?room_type=Deluxe&ordering_type=ASC')
            self.assertEqual(response.status_code, 200)

            time.sleep(10)

            for i in range(2):
                response = tester.get('/room?room_type=Deluxe&ordering_type=ASC')
                self.assertEqual(response.status_code, 200)
                
if __name__ == '__main__':
    unittest.main()