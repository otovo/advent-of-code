SET client_min_messages TO WARNING;

DROP SCHEMA IF EXISTS day_1 CASCADE;
CREATE SCHEMA IF NOT EXISTS day_1;

CREATE TABLE day_1.input
(
    calories INT
);

-- DATA LOAD
COPY day_1.input FROM '/sql/day_1/input.csv' CSV;

-- SOLUTION
WITH label_elves AS (
    SELECT
        -- rolling sum over sequential increments of 1
        -- partitioned by partitions delimited by null calories (newline in input.csv)
        calories,
        sum(CASE WHEN calories IS NULL THEN 1 ELSE 0 END) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS elf
    FROM day_1.input
                    ),

     top3_loads_carried AS (
        -- sum by elf
        -- output the top 3 largest sum carried
         SELECT
             elf,
             sum(calories) AS value
         FROM label_elves
         GROUP BY 1
         ORDER BY 2 DESC
         LIMIT 3
     )

SELECT
    -- calories caried by all elves in the set
    'Day 1 | Solution 1',
    max(value)
FROM top3_loads_carried

UNION ALL

SELECT
    -- calories caried by all elves in the set
    'Day 1 | Solution 2',
    sum(value)
FROM top3_loads_carried
