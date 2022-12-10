SET client_min_messages TO WARNING;

DROP SCHEMA IF EXISTS day_6 CASCADE;
CREATE SCHEMA IF NOT EXISTS day_6;

CREATE TABLE day_6.input
(
    datastream text
);

-- DATA LOAD
COPY day_6.input (datastream) FROM '/sql/day_6/input.csv' CSV;

-- SOLUTION
WITH enums AS (SELECT len from (VALUES (4)) AS enum (len)),
    df AS (
    SELECT
        row_number() OVER () AS pos,
        array_agg(chrs) OVER (ORDER BY id ROWS (SELECT len-1 FROM enums) PRECEDING) AS packet
    FROM day_6.input
        CROSS JOIN LATERAL unnest(regexp_split_to_array(datastream, '')) chrs
           )

SELECT
    'Day 6 | Solution 1',
    df.pos
FROM df
    CROSS JOIN LATERAL (
                   SELECT
                       array_agg(DISTINCT chrs) AS packet
                   FROM unnest(df.packet) chrs
                   ) packet__set
WHERE cardinality(packet__set.packet) = (SELECT len FROM enums)
LIMIT 1;


WITH enums AS (SELECT len from (VALUES (14)) AS enum (len)),
    df AS (
    SELECT
        row_number() OVER () AS pos,
        array_agg(chrs) OVER (ORDER BY id ROWS (SELECT len-1 FROM enums) PRECEDING) AS packet
    FROM day_6.input
        CROSS JOIN LATERAL unnest(regexp_split_to_array(datastream, '')) chrs
           )

SELECT
    'Day 6 | Solution 2',
    df.pos
FROM df
    CROSS JOIN LATERAL (
                   SELECT
                       array_agg(DISTINCT chrs) AS packet
                   FROM unnest(df.packet) chrs
                   ) packet__set
WHERE cardinality(packet__set.packet) = (SELECT len FROM enums)
LIMIT 1;
