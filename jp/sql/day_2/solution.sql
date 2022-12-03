SET client_min_messages TO WARNING;

DROP SCHEMA IF EXISTS day_2 CASCADE;
CREATE SCHEMA IF NOT EXISTS day_2;

CREATE TABLE day_2.play_map
(
    my_play          VARCHAR(1) NOT NULL PRIMARY KEY,
    normalised_play  VARCHAR(1) NOT NULL,
    expected_outcome VARCHAR(4) NOT NULL,
    play_points      SMALLINT   NOT NULL
);

INSERT INTO day_2.play_map
VALUES ('Y', 'B', 'draw', 2),
       ('X', 'A', 'loss', 1),
       ('Z', 'C', 'win', 3);

CREATE TABLE day_2.outcome_map
(
    op_play        VARCHAR(1) NOT NULL,
    my_play        VARCHAR(1) NOT NULL,
    outcome        varchar(4) NOT NULL,
    outcome_points SMALLINT   NOT NULL,
    PRIMARY KEY (op_play, my_play)
);

INSERT INTO day_2.outcome_map
VALUES ('A', 'Y', 'win', 6),
       ('A', 'X', 'draw', 3),
       ('A', 'Z', 'loss', 0),
       ('B', 'Z', 'win', 6),
       ('B', 'Y', 'draw', 3),
       ('B', 'X', 'loss', 0),
       ('C', 'X', 'win', 6),
       ('C', 'Z', 'draw', 3),
       ('C', 'Y', 'loss', 0);

CREATE TABLE day_2.input
(
    op_play VARCHAR(1) NOT NULL,
    my_play VARCHAR(1) NOT NULL REFERENCES day_2.play_map (my_play)
);

-- DATA LOAD
COPY day_2.input FROM '/sql/day_2/input.csv' CSV DELIMITER ' ';

-- SOLUTION

SELECT
    'Day 1 | Solution 2',
    sum(play_points) + sum(outcome_points)
FROM day_2.input input
    JOIN day_2.play_map play ON play.my_play = input.my_play
    JOIN day_2.outcome_map map ON input.my_play = map.my_play AND input.op_play = map.op_play;

-- UNION ALL

SELECT
    'Day 1 | Solution 2',
    sum(map.outcome_points) + sum(play_points.play_points)
FROM day_2.input input
    JOIN day_2.play_map play ON input.my_play = play.my_play
    JOIN day_2.outcome_map map ON play.expected_outcome = map.outcome AND input.op_play = map.op_play
    JOIN day_2.play_map play_points ON map.my_play = play_points.my_play
