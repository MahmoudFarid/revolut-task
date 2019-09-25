import json
import os
import unittest

from io import BytesIO

from api import app
from constants import FILE_NAME


class TestAPIs(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.url = '/api/v1/nest'

    def tearDown(self):
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)

    def test_get_nest_api(self):
        response = self.app.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json.get('message'), 'The method is not allowed for the requested URL.')

    def test_nest_without_authentication(self):
        response = self.app.post(self.url)
        self.assertEqual(response.status_code, 401)

    def test_nest_with_invalid_token(self):
        response = self.app.post(self.url, headers=dict(AUTHORIZATION="Token test"))
        self.assertEqual(response.status_code, 401)

    def test_nest_without_data(self):
        response = self.app.post(self.url, headers=dict(AUTHORIZATION="Token secret-token-1"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json.get('message').get('file'), 'This field is requied')
        self.assertEqual(response.json.get('message').get('levels'),
                         'You must add at least one key as a request parameter')

    def test_nest_with_invalid_key(self):
        data_json = [{"country": "FR"}]
        data = dict(
            file=(BytesIO(json.dumps(data_json).encode()), FILE_NAME)
        )
        response = self.app.post('/api/v1/nest?level=sdfsddsds',
                                 headers=dict(AUTHORIZATION="Token secret-token-1"),
                                 content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json.get('message').get('errors'),
                         "The file it not valid or you entered unknown level in query parameter")

    def test_nest_with_invalid_data_keys(self):
        data_json = [{"country": "FR"}, {"city": "Paris"}]
        data = dict(
            file=(BytesIO(json.dumps(data_json).encode()), FILE_NAME)
        )
        response = self.app.post('/api/v1/nest?level=country',
                                 headers=dict(AUTHORIZATION="Token secret-token-1"),
                                 content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json.get('message').get('errors'),
                         "The file it not valid or you entered unknown level in query parameter")

    def test_nest_with_data_with_one_level(self):
        data_jaon = [
            {
                "city": "Paris",
                "country": "FR",
                "currency": "EUR",
                "amount": 20
            },
            {
                "city": "Lyon",
                "country": "FR",
                "currency": "EUR",
                "amount": 11.4
            }
        ]
        expected_output = {
            'FR': [
                {'amount': 20, 'city': 'Paris', 'currency': 'EUR'},
                {'amount': 11.4, 'city': 'Lyon', 'currency': 'EUR'}
            ]}
        data = dict(
            file=(BytesIO(json.dumps(data_jaon).encode()), FILE_NAME)
        )
        response = self.app.post('/api/v1/nest?level=country',
                                 headers=dict(AUTHORIZATION="Token secret-token-1"),
                                 content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_output)

    def test_nest_with_data_with_two_levels(self):
        data_jaon = [
            {
                "city": "Paris",
                "country": "FR",
                "currency": "EUR",
                "amount": 20
            },
            {
                "city": "Lyon",
                "country": "FR",
                "currency": "EUR",
                "amount": 11.4
            }
        ]
        expected_output = {
            'EUR':
                {'FR':
                    [{'amount': 20, 'city': 'Paris'},
                     {'amount': 11.4, 'city': 'Lyon'}]
                 }
        }
        data = dict(
            file=(BytesIO(json.dumps(data_jaon).encode()), FILE_NAME)
        )
        response = self.app.post('/api/v1/nest?level=currency&level=country',
                                 headers=dict(AUTHORIZATION="Token secret-token-1"),
                                 content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_output)

    def test_nest_with_data_with_three_levels(self):
        data_jaon = [
            {
                "city": "Paris",
                "country": "FR",
                "currency": "EUR",
                "amount": 20
            },
            {
                "city": "Lyon",
                "country": "FR",
                "currency": "EUR",
                "amount": 11.4
            }
        ]
        expected_output = {
            'EUR':
                {'FR':
                    {'Lyon':
                        [{'amount': 11.4}],
                     'Paris':
                        [{'amount': 20}]
                     }
                 }
        }
        data = dict(
            file=(BytesIO(json.dumps(data_jaon).encode()), FILE_NAME)
        )
        response = self.app.post('/api/v1/nest?level=currency&level=country&level=city',
                                 headers=dict(AUTHORIZATION="Token secret-token-1"),
                                 content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_output)

    def test_nest_with_data_with_four_levels(self):
        data_jaon = [
            {
                "city": "Paris",
                "country": "FR",
                "currency": "EUR",
                "amount": 20
            },
            {
                "city": "Lyon",
                "country": "FR",
                "currency": "EUR",
                "amount": 11.4
            }
        ]
        expected_output = {
            'EUR':
                {'FR':
                    {'Lyon':
                        {'11.4': [{}]},
                     'Paris':
                        {'20': [{}]}
                     }
                 }
        }
        data = dict(
            file=(BytesIO(json.dumps(data_jaon).encode()), FILE_NAME)
        )
        response = self.app.post('/api/v1/nest?level=currency&level=country&level=city&level=amount',
                                 headers=dict(AUTHORIZATION="Token secret-token-1"),
                                 content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_output)
