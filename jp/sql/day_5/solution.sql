SET client_min_messages TO WARNING;

DROP SCHEMA IF EXISTS day_5 CASCADE;
CREATE SCHEMA IF NOT EXISTS day_5;

CREATE TABLE day_5.input
(
    id  SERIAL,
    raw TEXT
);

-- DATA LOAD
COPY day_5.input (raw) FROM '/sql/day_5/input.csv' CSV;

-- SOLUTION
DROP FUNCTION IF EXISTS day_5.arr_to_cols;
CREATE OR REPLACE FUNCTION day_5.arr_to_cols(arr text[])
    RETURNS TABLE
            (
                col1 varchar(1),
                col2 varchar(1),
                col3 varchar(1),
                col4 varchar(1),
                col5 varchar(1),
                col6 varchar(1),
                col7 varchar(1),
                col8 varchar(1),
                col9 varchar(1)
            )
AS
$$
DECLARE
    row text[];
BEGIN
    FOREACH row SLICE 1 IN ARRAY arr
        LOOP
            col1 := row[1];
            col2 := row[2];
            col3 := row[3];
            col4 := row[4];
            col5 := row[5];
            col6 := row[6];
            col7 := row[7];
            col8 := row[8];
            col9 := row[9];
            RETURN NEXT;
        END LOOP;
END
$$ LANGUAGE plpgsql;

WITH RECURSIVE
    stack AS (
        SELECT
            jsonb_build_array(
                    string_agg(boxes.col1, ''),
                    string_agg(boxes.col2, ''),
                    string_agg(boxes.col3, ''),
                    string_agg(boxes.col4, ''),
                    string_agg(boxes.col5, ''),
                    string_agg(boxes.col6, ''),
                    string_agg(boxes.col7, ''),
                    string_agg(boxes.col8, ''),
                    string_agg(boxes.col9, '')
                ) AS stack
        FROM day_5.input
            CROSS JOIN LATERAL day_5.arr_to_cols(string_to_array(regexp_replace(regexp_replace(raw, '(\s{4}|\s)', ',', 'g'), '[\[\]]', '', 'g'), ',')) boxes
        WHERE raw LIKE '%[%'
             ),

    moves AS (
        SELECT
            row_number() OVER (ORDER BY id)::int AS step,
            substring(raw, 'move (\d+)')::int AS moves,
            substring(raw, 'from (\d+)')::int AS "from",
            substring(raw, 'to (\d+)')::int AS "to"
        FROM day_5.input
            CROSS JOIN LATERAL regexp_matches(raw, 'move (\d+) from (\d+) to (\d+)') move_parts
    ),

    shuffle AS (
        SELECT
            0 AS step,
            0 AS moves,
            0 AS "from",
            0 AS "to",
            stack
        FROM stack

        UNION ALL

        SELECT
            m.step,
            m.moves,
            m.from,
            m.to,
            jsonb_set(
                    jsonb_set(
                            stack,
                            ARRAY [(m.to - 1)::text],
                            to_jsonb(reverse(substring(stack ->> (m.from - 1) FOR m.moves)) || (stack ->> (m.to - 1)))
                        ),
                    ARRAY [(m.from - 1)::text],
                    to_jsonb(substring(stack ->> (m.from - 1) FROM m.moves + 1))
                )
        FROM shuffle
            JOIN moves AS m ON m.step = shuffle.step + 1
    )

SELECT
    'Day 5 | Solution 1',
    string_agg(left(stacks, 1), '')
FROM shuffle
CROSS JOIN LATERAL jsonb_array_elements_text(stack) stacks
GROUP BY step
ORDER BY step DESC
LIMIT 1;

WITH RECURSIVE
    stack AS (
        SELECT
            jsonb_build_array(
                    string_agg(boxes.col1, ''),
                    string_agg(boxes.col2, ''),
                    string_agg(boxes.col3, ''),
                    string_agg(boxes.col4, ''),
                    string_agg(boxes.col5, ''),
                    string_agg(boxes.col6, ''),
                    string_agg(boxes.col7, ''),
                    string_agg(boxes.col8, ''),
                    string_agg(boxes.col9, '')
                ) AS stack
        FROM day_5.input
            CROSS JOIN LATERAL day_5.arr_to_cols(string_to_array(regexp_replace(regexp_replace(raw, '(\s{4}|\s)', ',', 'g'), '[\[\]]', '', 'g'), ',')) boxes
        WHERE raw LIKE '%[%'
             ),

    moves AS (
        SELECT
            row_number() OVER (ORDER BY id)::int AS step,
            substring(raw, 'move (\d+)')::int AS moves,
            substring(raw, 'from (\d+)')::int AS "from",
            substring(raw, 'to (\d+)')::int AS "to"
        FROM day_5.input
            CROSS JOIN LATERAL regexp_matches(raw, 'move (\d+) from (\d+) to (\d+)') move_parts
    ),

    shuffle AS (
        SELECT
            0 AS step,
            0 AS moves,
            0 AS "from",
            0 AS "to",
            stack
        FROM stack

        UNION ALL

        SELECT
            m.step,
            m.moves,
            m.from,
            m.to,
            jsonb_set(
                    jsonb_set(
                            stack,
                            ARRAY [(m.to - 1)::text],
                            to_jsonb(substring(stack ->> (m.from - 1) FOR m.moves) || (stack ->> (m.to - 1)))
                        ),
                    ARRAY [(m.from - 1)::text],
                    to_jsonb(substring(stack ->> (m.from - 1) FROM m.moves + 1))
                )
        FROM shuffle
            JOIN moves AS m ON m.step = shuffle.step + 1
    )

SELECT
    'Day 5 | Solution 2',
    string_agg(left(stacks, 1), '')
FROM shuffle
CROSS JOIN LATERAL jsonb_array_elements_text(stack) stacks
GROUP BY step
ORDER BY step DESC
LIMIT 1;
