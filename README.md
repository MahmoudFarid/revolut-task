Revolut - Python Developer (Data) Challenge

Programming Tasks
-----------------

In the beginning we need to create a virtual environment with python 3.6 or higher and install the requirements

    $ pip install -r equirements.txt

* Task 1
^^^^^^^^

All implementation in nest.py file, so we need to run this file.

We have 2 ways to run this file

    * from STDIN

        $ cat input.json | python nest.py nesting_level_1 nesting_level_2 ... nesting_level_n

    * from file

        $ python nest.py nesting_level_1 nesting_level_2 ... nesting_level_n -f input.json

To get more help, you can use

    $ python nest.py -h


* Task 2
^^^^^^^^

It's a simple API runs over Flask RESTful. All implementation in api.py file.
To run the server, please run

    $ python api.py

then you can post a request on `http://localhost:5000/api/v1/nest` with the file in the body of the request
Also, you must to add at least one level on the URL, i.e: `http://127.0.0.1:5000/api/v1/nest?level=city`
I implemented a very simple way to authenticate this API, all what you need to do is adding a header `Authorization`
to the request with value `Token secret-token-1`.


* Unit tests
^^^^^^^^^^^^

I added unit tests for the most of the application, all tests in the folder tests and splits into multiple files.
All tests related with python script will be in `test_nest.py`
All tests related with APIs will be in `test_apis.py`
All tests related with SQL Queries will be in `test_sql.py`

To run unit tests, just run:

    $ python -m unittest discover


SQL
---

All queries you can find it in query.sql file.
For the requirements 1 and 2, I added more than a solution to solve it, I tried to do my best to find the
most efficient way to solve the problem in a short time. So you can see multiple solutions for each one.

For the thid requirements, I can't find any way to solve it within 5s without editing on the schema,
so I edit on it by adding a PK for each table (transactions and exchange_rates) and FK between transactions
and exchange_rates, this helped me to solve the problem in ms not seconds!
You will find in `new_schema.sql`, the new tables after editing, and the new scripts for adding multiple data into it.
Also, I implemented a trigger function that will run after inserting any transaction to get the er_id
for this transaction, you will find this function in `new_schema.sql` also.
