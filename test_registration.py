"""Test file for WCG api webservice."""
from typing import cast
import unittest
import requests
from decouple import config
from datetime import datetime


class RegistrationTest(unittest.TestCase):
    """Tests registration endpoint of WCG api."""

    URL = config("URL", cast=str)

    def setUp(self):
        """Initialize testing variable."""
        self.body = {
            "citizen_id": "1234567890123",
            "name": "Chayapol",
            "surname": "Chaipongsawalee",
            "birth_date": "2000-05-11",
            "occupation": "occupation",
            "phone_number": "0980000000",
            "is_risk": "False",
            "address": "address",
        }

        citizen_id = self.body.get("citizen_id")
        requests.delete(f"{self.URL}/registration/{citizen_id}")

    def test_post_registration(self):
        """Send the POST request to create a registration."""
        endpoint = f"{self.URL}/registration"
        citizen_id = self.body.get("citizen_id")
        response = requests.get(f"{self.URL}/registration/{citizen_id}")
        if response.status_code == 200:
            response = requests.delete(f"{self.URL}/registration/{citizen_id}")
        response = requests.post(endpoint, params=self.body)
        content = response.json()
        self.assertEqual(201, response.status_code)
        self.assertEqual("registration success!", content["feedback"])
        self.assertEqual("text/html; charset=utf-8", response.headers["content-type"])

    def test_post_duplicate_registration(self):
        """Send the POST request with same data 2 times."""
        endpoint = f"{self.URL}/registration"
        citizen_id = self.body.get("citizen_id")
        response = requests.get(f"{self.URL}/registration/{citizen_id}")
        if response.status_code == 200:
            response = requests.delete(f"{self.URL}/registration/{citizen_id}")
        response = requests.post(endpoint, params=self.body)
        response = requests.post(endpoint, params=self.body)
        content = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            "registration failed: this person already registered", content["feedback"]
        )
        self.assertEqual("application/json", response.headers["content-type"])

    def test_post_with_missing_param_address(self):
        """Send the POST request with 5 query param exclude address."""
        body = {
            "citizen_id": "1234567890123",
            "name": "Chayapol",
            "surname": "Chaipongsawalee",
            "birth_date": "2000-05-11",
            "occupation": "occupation",
            "phone_number": "0980000000",
            "is_rick": "False",
        }
        endpoint = f"""{self.URL}/registration"""
        citizen_id = self.body.get("citizen_id")
        response = requests.get(f"{self.URL}/registration/{citizen_id}")
        if response.status_code == 200:
            response = requests.delete(f"{self.URL}/registration/{citizen_id}")
        response = requests.delete(f"{endpoint}/{citizen_id}")
        response = requests.post(endpoint, params=body)
        self.assertEqual(400, response.status_code)
        self.assertEqual("text/html; charset=utf-8", response.headers["content-type"])

    def test_post_with_more_than_13_digits_id(self):
        """Send the POST request with invalid citizen id."""
        body = self.body
        body["citizen_id"] = "1234567890123123123"
        endpoint = f"""{self.URL}/registration"""
        response = requests.post(endpoint, params=self.body)
        content = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual("registration failed: invalid citizen ID", content["feedback"])
        self.assertEqual("application/json", response.headers["content-type"])

    def test_post_with_invalid_birth_date(self):
        """Send the POST request with invalid birth date format."""
        body = self.body
        body["birth_date"] = "abcaddd"
        endpoint = f"{self.URL}/registration"
        response = requests.post(endpoint, params=body)
        content = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            "registration failed: invalid birth date format", content["feedback"]
        )
        self.assertEqual("application/json", response.headers["content-type"])

    def test_post_with_d_m_y_birth_date(self):
        """Send the POST request with dd/mm/yyyy birth date format."""
        body = self.body
        body["birth_date"] = "05/11/2000"
        endpoint = f"{self.URL}/registration"
        response = requests.post(endpoint, params=body)
        content = response.json()
        self.assertEqual(201, response.status_code)
        self.assertEqual("registration success!", content["feedback"])
        self.assertEqual("text/html; charset=utf-8", response.headers["content-type"])

    def test_post_with_y_m_d_birth_date(self):
        """Send the POST request with mm/dd/yyyy birth date format."""
        body = self.body
        body["birth_date"] = "11/05/2000"
        endpoint = f"{self.URL}/registration"
        response = requests.post(endpoint, params=body)
        content = response.json()
        self.assertEqual(201, response.status_code)
        self.assertEqual("registration success!", content["feedback"])
        self.assertEqual("text/html; charset=utf-8", response.headers["content-type"])

    def test_post_with_m_y_d_birth_date(self):
        """Send the POST request with mm/yyyy/dd birth date."""
        body = self.body
        body["birth_date"] = "11/2000/05"
        endpoint = f"{self.URL}/registration"
        response = requests.post(endpoint, params=body)
        content = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            "registration failed: invalid birth date format", content["feedback"]
        )
        self.assertEqual("application/json", response.headers["content-type"])

    def test_post_with_less_than_12_years_old(self):
        """Send the POST request with less than 12 years old data."""
        body = self.body
        body["birth_date"] = "11/05/2020"
        endpoint = f"{self.URL}/registration"
        response = requests.post(endpoint, params=body)
        content = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            "registration failed: not archived minimum age", content["feedback"]
        )
        self.assertEqual("application/json", response.headers["content-type"])

    def test_post_with_future_date(self):
        """Sent the POST request with future date."""
        body = self.body
        body["birth_date"] = "11/05/3000"
        endpoint = f"{self.URL}/registration"
        response = requests.post(endpoint, params=body)
        content = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            "registration failed: not archived minimum age", content["feedback"]
        )
        self.assertEqual("application/json", response.headers["content-type"])

    def test_remove_invalid_registration(self):
        """Send the DELETE request with invalid citizen id"""
        citizen_id = self.body.get("citizen_id")
        endpoint = f"{self.URL}/registration{citizen_id}"
        response = requests.delete(endpoint, params=self.body)
        self.assertEqual(404, response.status_code)
        self.assertEqual("text/html; charset=utf-8", response.headers["content-type"])

    def test_remove_registration(self):
        """Sent the DELETE request."""
        citizen_id = self.body.get("citizen_id")
        endpoint = f"{self.URL}/registration"
        response = requests.post(endpoint, params=self.body)
        self.assertEqual(201, response.status_code)
        endpoint = f"{self.URL}/registration{citizen_id}"
        response = requests.delete(endpoint, params=self.body)
        self.assertEqual(404, response.status_code)
        self.assertEqual("text/html; charset=utf-8", response.headers["content-type"])
