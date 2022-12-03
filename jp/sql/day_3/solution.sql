SET client_min_messages TO WARNING;

DROP SCHEMA IF EXISTS day_3 CASCADE;
CREATE SCHEMA IF NOT EXISTS day_3;

CREATE TABLE day_3.input
(
    id       SERIAL PRIMARY KEY,
    contents TEXT NOT NULL
);

-- DATA LOAD
COPY day_3.input (contents) FROM '/sql/day_3/input.csv' CSV;

-- SOLUTION
WITH df AS (
    SELECT
        id,
        split_part(left(contents, char_length(contents) / 2) || '|' || right(contents, char_length(contents) / 2), '|', 1) AS compartment_1,
        split_part(left(contents, char_length(contents) / 2) || '|' || right(contents, char_length(contents) / 2), '|', 2) AS compartment_2
    FROM day_3.input
           ),

     priorities AS (
         SELECT DISTINCT
             id,
             compartment_1,
             compartment_2,
             CASE WHEN lower(expld.chr) = expld.chr THEN ascii(expld.chr) - 96 ELSE ascii(expld.chr) - 38 END AS priority
         FROM df
             CROSS JOIN LATERAL (
                            SELECT
                                c1.chr
                            FROM regexp_split_to_table(df.compartment_1, '') c1(chr)
                                JOIN regexp_split_to_table(df.compartment_2, '') c2(chr) ON c1.chr = c2.chr
                            ) expld
     )

SELECT
    'Day 3 | Solution 1',
    sum(priority)
FROM priorities;

WITH df AS (
    SELECT
        (id - 1) / 3 AS content_group,
        array_agg(contents) AS contents
    FROM day_3.input
    GROUP BY 1
           ),
     transpose AS (
         SELECT
             content_group,
             regexp_split_to_array(contents[1], '') AS contents_1,
             regexp_split_to_array(contents[2], '') AS contents_2,
             regexp_split_to_array(contents[3], '') AS contents_3
         FROM df
     )

SELECT
    'Day 3 | Solution 2',
    sum(CASE WHEN lower(common_chr.chr) = common_chr.chr THEN ascii(common_chr.chr) - 96 ELSE ascii(common_chr.chr) - 38 END)
FROM transpose
    CROSS JOIN LATERAL (SELECT DISTINCT
                            c1.chr
                        FROM unnest(contents_1) c1(chr)
                            CROSS JOIN unnest(contents_2) c2(chr)
                            CROSS JOIN unnest(contents_3) c3(chr)
                        WHERE c1.chr = c2.chr
                          AND c2.chr = c3.chr
                   ) AS common_chr;
