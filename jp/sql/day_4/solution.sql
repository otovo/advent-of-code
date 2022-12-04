SET client_min_messages TO WARNING;

DROP SCHEMA IF EXISTS day_4 CASCADE;
CREATE SCHEMA IF NOT EXISTS day_4;

CREATE TABLE day_4.input
(
    id          SERIAL PRIMARY KEY,
    first_pair  text NOT NULL,
    second_pair text NOT NULL
);

-- DATA LOAD
COPY day_4.input (first_pair, second_pair) FROM '/sql/day_4/input.csv' CSV;

-- SOLUTION
WITH df AS (
    SELECT
        id,
        split_part(first_pair, '-', 1) :: int AS first_start,
        split_part(first_pair, '-', 2) :: int AS first_stop,
        split_part(second_pair, '-', 1) :: int AS second_start,
        split_part(second_pair, '-', 2) :: int AS second_stop
    FROM day_4.input
           )

SELECT
    'Day 4 | Solution 1',
    sum(CASE
        WHEN first_start <= second_start AND first_stop >= second_stop THEN 1
        WHEN first_start >= second_start AND first_stop <= second_stop THEN 1 END)
FROM df

UNION ALL

SELECT
    'Day 4 | Solution 2',
    sum(CASE
        WHEN first_start BETWEEN second_start AND second_stop OR first_stop BETWEEN second_start AND second_stop THEN 1
        WHEN second_start BETWEEN first_start AND first_stop OR second_stop BETWEEN first_start AND first_stop THEN 1 END)
FROM df
