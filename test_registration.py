"""Test file for WCG api webservice."""
import unittest
import requests


class RegistrationTest(unittest.TestCase):
    """Tests registration endpoint of WCG api."""

    URL = "https://wcg-apis.herokuapp.com"

    def setUp(self):
        """Initialize testing variable."""
        self.name = "test name"
        self.surname = "test surname"
        self.birth_date = "2000-01-05"
        self.occupation = "tester"
        self.address = "bkk"

    def test_get_registration(self):
        """Send the GET request to fetch user's registration."""
        endpoint = f"{self.URL}/registration"
        response = requests.get(endpoint)
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers['content-type'])

    def test_post_registration(self):
        """Send the POST request to create a registration."""
        endpoint = f"""{self.URL}/registration?citizen_id="1234567890123"&name={self.name}&surname={self.surname}&birth_date={self.birth_date}&occupation={self.occupation}&address={self.address}"""
        response = requests.post(endpoint)
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers['content-type'])

    def test_post_with_missing_param_address(self):
        """Send the POST request with 5 query param exclude address."""
        endpoint = f"""{self.URL}/registration?citizen_id=13839573948374&name={self.name}&surname={self.surname}&birth_date={self.birth_date}&occupation={self.occupation}"""
        response = requests.post(endpoint)
        self.assertEqual(400, response.status_code)
        self.assertEqual("text/html; charset=utf-8",
                         response.headers['content-type'])

    def test_post_with_missing_param_occupation(self):
        """Send the POST request with 5 query param exclude occupation."""
        endpoint = f"""{self.URL}/registration?citizen_id=13839573948374&name={self.name}&surname={self.surname}&birth_date={self.birth_date}&address={self.address}"""
        response = requests.post(endpoint)
        self.assertEqual(400, response.status_code)
        self.assertEqual("text/html; charset=utf-8",
                         response.headers['content-type'])

    def test_post_with_missing_param_birth_date(self):
        """Send the POST request with 5 query param exclude birth date."""
        endpoint = f"""{self.URL}/registration?citizen_id=13839573948374&name={self.name}&surname={self.surname}&occupation={self.occupation}&address={self.address}"""
        response = requests.post(endpoint)
        self.assertEqual(400, response.status_code)
        self.assertEqual("text/html; charset=utf-8",
                         response.headers['content-type'])

    def test_post_with_missing_param_surname(self):
        """Send the POST request with 5 query param exclude surname."""
        endpoint = f"""{self.URL}/registration?citizen_id=13839573948374&name={self.name}&birth_date={self.birth_date}&occupation={self.occupation}&address={self.address}"""
        response = requests.post(endpoint)
        self.assertEqual(400, response.status_code)
        self.assertEqual("text/html; charset=utf-8",
                         response.headers['content-type'])

    def test_post_with_missing_param_name(self):
        """Send the POST request with 5 query param exclude name."""
        endpoint = f"""{self.URL}/registration?citizen_id=13839573948374&surname={self.surname}&birth_date={self.birth_date}&occupation={self.occupation}&address={self.address}"""
        response = requests.post(endpoint)
        self.assertEqual(400, response.status_code)
        self.assertEqual("text/html; charset=utf-8",
                         response.headers['content-type'])

    def test_post_with_missing_param_citizen_id(self):
        """Send the POST request with 5 query param exclude citizen id."""
        endpoint = f"""{self.URL}/registration?name={self.name}&surname={self.surname}&birth_date={self.birth_date}&occupation={self.occupation}&address={self.address}"""
        response = requests.post(endpoint)
        self.assertEqual(400, response.status_code)
        self.assertEqual("text/html; charset=utf-8",
                         response.headers['content-type'])

    def test_post_with_more_than_13_digits_id(self):
        """Send the POST request with invalid id."""
        invalid_id = "123456789"
        endpoint = f"""{self.URL}/registration?citizen_id={invalid_id}&name={self.name}&surname={self.surname}&birth_date={self.birth_date}&occupation={self.occupation}&address={self.address}"""
        response = requests.post(endpoint)
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers['content-type'])
        fb = response.json()["feedback"]
        self.assertNotEqual(-1, fb.find("failed"))

    def test_post_with_invalid_birth_date(self):
        """Send the POST request with invalid birth date format."""
        invalid_birth_date = "abcdefgh"
        endpoint = f"""{self.URL}/registration?citizen_id=1238193756392&name={self.name}&surname={self.surname}&birth_date={invalid_birth_date}&occupation={self.occupation}&address={self.address}"""
        response = requests.post(endpoint)
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers['content-type'])
        fb = response.json()["feedback"]
        self.assertNotEqual(-1, fb.find("failed"))

    def test_post_with_less_than_12_years_old(self):
        """Send the POST request with less than 12 years old data."""
        less_than_12_years_old_birth_date = "01-01-2020"
        endpoint = f"""{self.URL}/registration?citizen_id=1239562957394&name={self.name}&surname={self.surname}&birth_date={less_than_12_years_old_birth_date}&occupation={self.occupation}&address={self.address}"""
        response = requests.post(endpoint)
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers['content-type'])
        fb = response.json()["feedback"]
        self.assertNotEqual(-1, fb.find("failed"))

    def test_post_with_future_date(self):
        """Sent the POST request with future date."""
        future_date = "01-01-3000"
        endpoint = f"""{self.URL}/registration?citizen_id=8365937591831&name={self.name}&surname={self.surname}&birth_date={future_date}&occupation={self.occupation}&address={self.address}"""
        response = requests.post(endpoint)
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers['content-type'])
        fb = response.json()["feedback"]
        self.assertNotEqual(-1, fb.find("failed"))
