# Query 1
# Write down a query that gives us a breakdown of spend in GBP by each user. Use the exchange rate with the largest timestamp

# Solution 1 >> equal the same in performance with solution 2
WITH er_with_pos AS (
  SELECT *, ROW_NUMBER() OVER(PARTITION BY from_currency ORDER BY ts DESC) AS n
  FROM exchange_rates
  WHERE to_currency = 'GBP'
)

SELECT f.user_id, SUM(f.total_gbp_amount)
FROM (
  SELECT t.user_id, t.amount*COALESCE(new_er.rate, 1) AS total_gbp_amount
  FROM transactions AS t
  LEFT JOIN er_with_pos AS new_er
  ON new_er.n = 1 AND t.currency = new_er.from_currency
) AS f

GROUP BY f.user_id
ORDER BY f.user_id
;


# Solution 2
WITH new_exchange_rate AS(
  SELECT er.from_currency, er.rate
    FROM exchange_rates AS er, (
    SELECT from_currency, MAX(ts) as ts
    FROM exchange_rates as new_er
    GROUP BY from_currency
  ) AS new_er
WHERE er.ts = new_er.ts AND er.to_currency = 'GBP'
)

SELECT t.user_id, SUM(t.amount*COALESCE(er.rate, 1))
FROM transactions as t
LEFT JOIN new_exchange_rate as er
ON t.currency = er.from_currency
GROUP BY t.user_id
ORDER BY t.user_id
;

# Solution 3 >> The worst one

SELECT f.user_id, SUM(f.amount*COALESCE(f.rate, 1))
FROM (
  SELECT DISTINCT ON (t.ts, t.amount, t.currency) t.ts, *
  FROM transactions AS t
  LEFT JOIN exchange_rates AS er
  ON t.currency = er.from_currency
  WHERE er.to_currency = 'GBP' OR t.currency = 'GBP'
  ORDER BY t.ts, t.amount, t.currency, er.ts DESC
) as f
GROUP BY f.user_id
ORDER BY f.user_id
;

# Query 2
# Write down the same query, but this time, use the latest exchange rate smaller or equal then the transaction timestamp. The solution should have the two columns: user_id, total_spent_gbp, ordered by user_id

# Solution 1 >> Better than solution 1
SELECT f.user_id, SUM(f.amount*COALESCE(f.rate, 1))
FROM (
  SELECT DISTINCT ON (t.ts, t.currency) t.ts, t.user_id, t.currency, t.amount, er.ts, er.rate
  FROM transactions as t
  LEFT JOIN exchange_rates as er
  ON t.ts >= er.ts AND t.currency = er.from_currency AND er.to_currency = 'GBP'
  ORDER BY t.ts, t.currency, t.user_id, t.amount, er.ts DESC
) As f
GROUP BY f.user_id
ORDER BY f.user_id
;


# Solution 2
SELECT ft.user_id, SUM(ft.gbp_amount)
FROM (
  SELECT final.user_id, final.amount*final.rate AS gbp_amount
  FROM(
    WITH temp AS (
      SELECT *, ROW_NUMBER() OVER(PARTITION BY t.user_id, t.currency, t.amount, t.ts ORDER BY er.ts DESC) AS n
      FROM transactions as t
      INNER JOIN exchange_rates as er
      ON t.ts >= er.ts AND t.currency = er.from_currency AND er.to_currency = 'GBP'
    )
    SELECT *
    FROM temp
    where n = 1
  ) AS final

  UNION ALL

  SELECT user_id, amount AS gbp_amount
  FROM transactions
  WHERE currency = 'GBP') as ft
GROUP BY ft.user_id
ORDER BY ft.user_id
;



# Query 3
# Bonus for Postgres superstars: Consider the same schema, but now let’s add some random data, to simulate real scale

# In the beginning, I change the schema by adding a unique id for each table then make a FK relation between
# transactions table with exchange_rates table and this by default will generate an index for pk
# so when filter with pk it will not take a lot of time and will execute in a short time.
# Also I implemented a trigger to add the er_id in a transaction with each insertion.

# This will work with new schema and it will run within 60 ms!
SELECT t.user_id, SUM(t.amount*COALESCE(er.rate, 1)) from transactions AS t
LEFT JOIN exchange_rates AS er
ON t.er_id=er.id
GROUP BY t.user_id
ORDER BY t.user_id
