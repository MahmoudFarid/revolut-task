import json
import unittest

from unittest.mock import patch

from nest import is_valid_input, prepare_output, read_input


class TestNest(unittest.TestCase):

    def setUp(self):
        with open('input.json', 'r') as json_data:
            self.file = json.loads(json_data.read())

    def test_read_input_from_file(self):
        data = read_input(from_file=True, file='input.json')
        self.assertEqual(data, self.file)

    @patch('sys.stdin.readlines', return_value='{"x": "y"}')
    def test_read_input_from_stdin(self, stdin_mock):
        self.assertEqual(stdin_mock.call_count, 0)
        data = read_input()
        self.assertEqual(stdin_mock.call_count, 1)
        self.assertEqual(data, {"x": "y"})

    def test_is_valid_input(self):
        self.assertTrue(is_valid_input(self.file))

    def test_is_valid_input_with_not_correct_data(self):
        # import ipdb; ipdb.set_trace()
        self.assertTrue(is_valid_input(self.file))

    def test_prepare_output_with_one_key_with_multiple_value(self):
        output = prepare_output(self.file, ["currency"])
        actual_output = {
            "USD": [
                {
                    "country": "US",
                    "city": "Boston",
                    "amount": 100
                }
            ],
            "EUR": [
                {
                    "country": "FR",
                    "city": "Paris",
                    "amount": 20
                },
                {
                    "country": "FR",
                    "city": "Lyon",
                    "amount": 11.4
                },
                {
                    "country": "ES",
                    "city": "Madrid",
                    "amount": 8.9
                }
            ],
            "GBP": [
                {
                    "country": "UK",
                    "city": "London",
                    "amount": 12.2
                }
            ],
            "FBP": [
                {
                    "country": "UK",
                    "city": "London",
                    "amount": 10.9
                }
            ]
        }
        self.assertEqual(output, actual_output)

    def test_prepare_output_with_one_key_with_one_value(self):
        output = prepare_output(self.file, ["city"])
        actual_output = {
            "Boston": [
                {
                    "country": "US",
                    "currency": "USD",
                    "amount": 100
                }
            ],
            "Paris": [
                {
                    "country": "FR",
                    "currency": "EUR",
                    "amount": 20
                }
            ],
            "Lyon": [
                {
                    "country": "FR",
                    "currency": "EUR",
                    "amount": 11.4
                }
            ],
            "Madrid": [
                {
                    "country": "ES",
                    "currency": "EUR",
                    "amount": 8.9
                }
            ],
            "London": [
                {
                    "country": "UK",
                    "currency": "GBP",
                    "amount": 12.2
                },
                {
                    "country": "UK",
                    "currency": "FBP",
                    "amount": 10.9
                }
            ]
        }
        self.assertEqual(output, actual_output)

    def test_prepare_output_with_two_keys(self):
        output = prepare_output(self.file, ["currency", "country"])
        actual_output = {
            "USD": {
                "US": [
                    {
                        "city": "Boston",
                        "amount": 100
                    }
                ]
            },
            "EUR": {
                "FR": [
                    {
                        "city": "Paris",
                        "amount": 20
                    },
                    {
                        "city": "Lyon",
                        "amount": 11.4
                    }
                ],
                "ES": [
                    {
                        "city": "Madrid",
                        "amount": 8.9
                    }
                ]
            },
            "GBP": {
                "UK": [
                    {
                        "city": "London",
                        "amount": 12.2
                    }
                ]
            },
            "FBP": {
                "UK": [
                    {
                        "city": "London",
                        "amount": 10.9
                    }
                ]
            }
        }
        self.assertEqual(output, actual_output)

    def test_prepare_output_with_three_keys(self):
        output = prepare_output(self.file, ["currency", "country", "city"])
        actual_output = {
            "USD": {
                "US": {
                    "Boston": [
                        {
                            "amount": 100
                        }
                    ]
                }
            },
            "EUR": {
                "FR": {
                    "Paris": [
                        {
                            "amount": 20
                        }
                    ],
                    "Lyon": [
                        {
                            "amount": 11.4
                        }
                    ]
                },
                "ES": {
                    "Madrid": [
                        {
                            "amount": 8.9
                        }
                    ]
                }
            },
            "GBP": {
                "UK": {
                    "London": [
                        {
                            "amount": 12.2
                        }
                    ]
                }
            },
            "FBP": {
                "UK": {
                    "London": [
                        {
                            "amount": 10.9
                        }
                    ]
                }
            }
        }
        self.assertEqual(output, actual_output)

    def test_prepare_output_with_four_keys(self):
        output = prepare_output(self.file, ["currency", "country", "city", "amount"])
        actual_output = {
            "USD": {
                "US": {
                    "Boston": {
                        100: [
                            {}
                        ]
                    }
                }
            },
            "EUR": {
                "FR": {
                    "Paris": {
                        20: [
                            {}
                        ]
                    },
                    "Lyon": {
                        11.4: [
                            {}
                        ]
                    }
                },
                "ES": {
                    "Madrid": {
                        8.9: [
                            {}
                        ]
                    }
                }
            },
            "GBP": {
                "UK": {
                    "London": {
                        12.2: [
                            {}
                        ]
                    }
                }
            },
            "FBP": {
                "UK": {
                    "London": {
                        10.9: [
                            {}
                        ]
                    }
                }
            }
        }
        self.assertEqual(output, actual_output)
