import sqlite3
import unittest

from .queries import max_ts_query_1, max_ts_query_2, nearest_ts_query_2

# I have a syntex error in max_ts_query_3 and nearest_ts_query_1 in sqlite, so I didn't implement tests for them


class TestSQLQuery(unittest.TestCase):

    def setUp(self):
        conn = sqlite3.connect('example.db')
        self.c = conn.cursor()
        self.c.execute("drop table if exists exchange_rates;")
        self.c.execute(
            """
            create table exchange_rates(
            ts timestamp without time zone,
            from_currency varchar(3),
            to_currency varchar(3),
            rate numeric
            );
            """
        )
        data = [
            ('2018-04-01 00:00:00', 'USD', 'GBP', '0.71'),
            ('2018-04-01 00:00:05', 'USD', 'GBP', '0.82'),
            ('2018-04-01 00:01:00', 'USD', 'GBP', '0.92'),
            ('2018-04-01 01:02:00', 'USD', 'GBP', '0.62'),

            ('2018-04-01 02:00:00', 'USD', 'GBP', '0.71'),
            ('2018-04-01 03:00:05', 'USD', 'GBP', '0.82'),
            ('2018-04-01 04:01:00', 'USD', 'GBP', '0.92'),
            ('2018-04-01 04:22:00', 'USD', 'GBP', '0.62'),

            ('2018-04-01 00:00:00', 'EUR', 'GBP', '1.71'),
            ('2018-04-01 01:00:05', 'EUR', 'GBP', '1.82'),
            ('2018-04-01 01:01:00', 'EUR', 'GBP', '1.92'),
            ('2018-04-01 01:02:00', 'EUR', 'GBP', '1.62'),

            ('2018-04-01 02:00:00', 'EUR', 'GBP', '1.71'),
            ('2018-04-01 03:00:05', 'EUR', 'GBP', '1.82'),
            ('2018-04-01 04:01:00', 'EUR', 'GBP', '1.92'),
            ('2018-04-01 05:22:00', 'EUR', 'GBP', '1.62'),

            ('2018-04-01 05:22:00', 'EUR', 'HUF', '0.062')
        ]
        self.c.executemany('INSERT INTO exchange_rates VALUES (?,?,?,?)', data)

        self.c.execute("drop table if exists transactions;")
        self.c.execute(
            """
            create table transactions (
            ts timestamp without time zone,
            user_id int,
            currency varchar(3),
            amount numeric
            );
            """
        )
        data = [
            ('2018-04-01 00:00:00', 1, 'EUR', 2.45),
            ('2018-04-01 01:00:00', 1, 'EUR', 8.45),
            ('2018-04-01 01:30:00', 1, 'USD', 3.5),
            ('2018-04-01 20:00:00', 1, 'EUR', 2.45),

            ('2018-04-01 00:30:00', 2, 'USD', 2.45),
            ('2018-04-01 01:20:00', 2, 'USD', 0.45),
            ('2018-04-01 01:40:00', 2, 'USD', 33.5),
            ('2018-04-01 18:00:00', 2, 'EUR', 12.45),

            ('2018-04-01 18:01:00', 3, 'GBP', 2),

            ('2018-04-01 00:01:00', 4, 'USD', 2),
            ('2018-04-01 00:01:00', 4, 'GBP', 2)
        ]
        self.c.executemany('INSERT INTO transactions VALUES (?,?,?,?)', data)

    def test_get_user_GBP_spend_with_max_ts_soltuion_1(self):
        output = list()
        for row in self.c.execute(max_ts_query_1):
            output.append(row)
        output_dict = dict((str(x), y) for x, y in output)
        # USD rate = 0.62 & EUR rate = 1.62
        # User 1 >>> Total Spend: 2.45 * 1.62 + 8.45 * 1.62 + 3.5 * 0.62 + 2.45 * 1.62 = 23.797000000000004
        self.assertEqual(output_dict.get("1"), 23.797000000000004)
        # User 2 >>> Total Spend: 2.45 * 0.62 + 0.45 * 0.62 + 33.5 * 0.62 + 12.45 * 1.62 = 42.736999999999995
        self.assertEqual(output_dict.get("2"), 42.736999999999995)
        # User 3 >>> Total Spend: 3 * 1 = 3
        self.assertEqual(output_dict.get("3"), 2)
        # User 4 >>> Total Spend: 2 * 0.62 + 2 * 1 = 3.24
        self.assertEqual(output_dict.get("4"), 3.24)

    def test_get_user_GBP_spend_with_max_ts_soltuion_2(self):
        output = list()
        for row in self.c.execute(max_ts_query_2):
            output.append(row)
        output_dict = dict((str(x), y) for x, y in output)
        # USD rate = 0.62 & EUR rate = 1.62
        # User 1 >>> Total Spend: 2.45 * 1.62 + 8.45 * 1.62 + 3.5 * 0.62 + 2.45 * 1.62 = 23.797000000000004
        self.assertEqual(output_dict.get("1"), 23.797000000000004)
        # User 2 >>> Total Spend: 2.45 * 0.62 + 0.45 * 0.62 + 33.5 * 0.62 + 12.45 * 1.62 = 42.736999999999995
        self.assertEqual(output_dict.get("2"), 42.736999999999995)
        # User 3 >>> Total Spend: 3 * 1 = 3
        self.assertEqual(output_dict.get("3"), 2)
        # User 4 >>> Total Spend: 2 * 0.62 + 2 * 1 = 3.24
        self.assertEqual(output_dict.get("4"), 3.24)

    def test_get_user_GBP_spend_with_the_nearest_ts_solution_2(self):
        output = list()
        for row in self.c.execute(nearest_ts_query_2):
            output.append(row)
        output_dict = dict((str(x), y) for x, y in output)
        # User 1 >>> Total Spend: 2.45 * 1.71 + 8.45 * 1.71 + 3.5 * 0.62 + 2.45 * 1.62 = 24.778
        self.assertEqual(output_dict.get("1"), 24.778)
        # User 2 >>> Total Spend: 2.45 * 0.92 + 0.45 * 0.62 + 33.5 * 0.62 + 12.45 * 1.62 = 43.472
        self.assertEqual(output_dict.get("2"), 43.472)
        # User 3 >>> Total Spend: 3 * 1 = 3
        self.assertEqual(output_dict.get("3"), 2)
        # User 4 >>> Total Spend: 2 * 0.92 + 2 * 1 = 3.84
        self.assertEqual(output_dict.get("4"), 3.84)
