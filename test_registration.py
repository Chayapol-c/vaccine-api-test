"""Test file for WCG api webservice."""
import unittest
import requests
from decouple import config
from datetime import datetime, timedelta


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
        self.endpoint = self.URL
        citizen_id = self.body.get("citizen_id")
        # remove this registration to avoid already registered case
        requests.delete(f"{self.URL}/{citizen_id}")

    def test_post_registration(self):
        """Send the POST request to create a registration."""
        response = requests.post(self.endpoint, params=self.body)
        content = response.json()
        self.assertEqual(201, response.status_code)
        self.assertEqual("registration success!", content["feedback"])
        self.assertEqual("text/html; charset=utf-8", response.headers["content-type"])

    def test_post_duplicate_registration(self):
        """Send the POST request with same data 2 times."""
        response = requests.post(self.endpoint, params=self.body)
        response = requests.post(self.endpoint, params=self.body)
        content = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            "registration failed: this person already registered", content["feedback"]
        )
        self.assertEqual("application/json", response.headers["content-type"])

    def test_post_with_missing_param_citizen_id(self):
        """Send the POST request with missing citizen_id."""
        self.body.pop("citizen_id")
        response = requests.post(self.endpoint, params=self.body)
        self.assertEqual(400, response.status_code)
        self.assertEqual("text/html; charset=utf-8", response.headers["content-type"])

    def test_post_with_more_than_13_digits_id(self):
        """Send the POST request with invalid citizen id."""
        self.body["citizen_id"] = "1234567890123123123"
        response = requests.post(self.endpoint, params=self.body)
        content = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual("registration failed: invalid citizen ID", content["feedback"])
        self.assertEqual("application/json", response.headers["content-type"])

    def test_post_with_invalid_birth_date(self):
        """Send the POST request with invalid birth date format."""
        self.body["birth_date"] = "abcaddd"
        response = requests.post(self.endpoint, params=self.body)
        content = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            "registration failed: invalid birth date format", content["feedback"]
        )
        self.assertEqual("application/json", response.headers["content-type"])

    def test_post_with_d_m_y_birth_date(self):
        """Send the POST request with dd/mm/yyyy birth date format."""
        self.body["birth_date"] = datetime(2000, 11, 5).strftime("%d/%m/%Y")
        response = requests.post(self.endpoint, params=self.body)
        content = response.json()
        self.assertEqual(201, response.status_code)
        self.assertEqual("registration success!", content["feedback"])
        self.assertEqual("text/html; charset=utf-8", response.headers["content-type"])

    def test_post_with_y_m_d_birth_date(self):
        """Send the POST request with yyyy/mm/dd birth date format."""
        self.body["birth_date"] = datetime(2000, 11, 5).strftime("%Y/%m/%d")
        response = requests.post(self.endpoint, params=self.body)
        content = response.json()
        self.assertEqual(201, response.status_code)
        self.assertEqual("registration success!", content["feedback"])
        self.assertEqual("text/html; charset=utf-8", response.headers["content-type"])

    def test_post_with_m_d_y_birth_date(self):
        """Send the POST request with mm/dd/yyyy birth date format."""
        self.body["birth_date"] = datetime(2000, 11, 5).strftime("%m/%d/%Y")
        response = requests.post(self.endpoint, params=self.body)
        content = response.json()
        self.assertEqual(201, response.status_code)
        self.assertEqual("registration success!", content["feedback"])
        self.assertEqual("text/html; charset=utf-8", response.headers["content-type"])

    def test_post_with_m_y_d_birth_date(self):
        """Send the POST request with mm/yyyy/dd birth date."""
        self.body["birth_date"] = datetime(2000, 11, 5).strftime("%m/%Y/%d")
        response = requests.post(self.endpoint, params=self.body)
        content = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            "registration failed: invalid birth date format", content["feedback"]
        )
        self.assertEqual("application/json", response.headers["content-type"])

    def test_post_with_d_y_m_birth_date(self):
        """Send the POST request with dd/yyyy/mm birth date."""
        self.body["birth_date"] = datetime(2000, 11, 5).strftime("%d/%Y/%m")
        response = requests.post(self.endpoint, params=self.body)
        content = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            "registration failed: invalid birth date format", content["feedback"]
        )
        self.assertEqual("application/json", response.headers["content-type"])

    def test_post_with_less_than_12_years_old(self):
        """Send the POST request with less than 12 years old data."""
        less_than_12_year_old = datetime.now() - timedelta(
            weeks=12 * 52
        )  # 12 years = 52 weeks * 12
        self.body["birth_date"] = less_than_12_year_old.strftime("%d/%m/%Y")
        response = requests.post(self.endpoint, params=self.body)
        content = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            "registration failed: not archived minimum age", content["feedback"]
        )
        self.assertEqual("application/json", response.headers["content-type"])

    def test_post_with_future_date(self):
        """Sent the POST request with future date."""
        future_date = datetime.now() + timedelta(days=2)
        self.body["birth_date"] = future_date.strftime("%d/%m/%Y")
        response = requests.post(self.endpoint, params=self.body)
        content = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            "registration failed: not archived minimum age", content["feedback"]
        )
        self.assertEqual("application/json", response.headers["content-type"])

    def test_remove_invalid_registration(self):
        """Send the DELETE request with invalid citizen id."""
        citizen_id = self.body.get("citizen_id")
        response = requests.delete(f"{self.endpoint}/{citizen_id}", params=self.body)
        self.assertEqual(404, response.status_code)
        self.assertEqual("text/html; charset=utf-8", response.headers["content-type"])

    def test_remove_registration(self):
        """Sent the DELETE request to remove a registration."""
        citizen_id = self.body.get("citizen_id")
        response = requests.post(self.endpoint, params=self.body)
        self.assertEqual(201, response.status_code)
        response = requests.delete(f"{self.endpoint}/{citizen_id}", params=self.body)
        self.assertEqual(200, response.status_code)
        self.assertEqual("text/html; charset=utf-8", response.headers["content-type"])

    def test_get_registration(self):
        """Send the GET request to retrive a registration."""
        citizen_id = self.body.get("citizen_id")
        response = requests.post(self.endpoint, params=self.body)
        response = requests.get(f"{self.endpoint}/{citizen_id}", params=self.body)
        self.assertEqual(200, response.status_code)
        content = response.json()
        self.body.update({"vaccine_taken": "[]"})
        self.assertEqual(self.body, content)
        self.assertEqual("text/html; charset=utf-8", response.headers["content-type"])

    def test_get_invalid_registration(self):
        """Send the GET request with invalid citizen id."""
        citizen_id = "123134567868"
        response = requests.get(f"{self.endpoint}/{citizen_id}", params=self.body)
        self.assertEqual(404, response.status_code)
        self.assertEqual("text/html; charset=utf-8", response.headers["content-type"])
