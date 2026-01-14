CREATE VIEW clean_3pt_shots AS 
SELECT PLAYER_ID, 
       PLAYER_NAME, 
       LOC_X, LOC_Y,
       SHOT_MADE, 
       SHOT_DISTANCE, 
       SHOT_TYPE 
FROM 
    NBA_Shots_2024 
WHERE 
    LOC_X IS NOT NULL  
    AND LOC_Y IS NOT NULL  
    AND SHOT_TYPE = '3PT Field Goal';

CREATE VIEW shots_with_distance2 AS
SELECT *,
       SQRT(
           LOC_X * LOC_X +
           (LOC_Y - 5.25) * (LOC_Y - 5.25)
       ) AS true_distance
FROM clean_3pt_shots;

SELECT
    AVG(true_distance - SHOT_DISTANCE) AS mean_diff,
    AVG(ABS(true_distance - SHOT_DISTANCE)) AS abs_diff
FROM shots_with_distance2;

CREATE VIEW analysis_shots AS
SELECT
    PLAYER_ID,
    PLAYER_NAME,
    LOC_X,
    LOC_Y,
    SHOT_MADE,
    true_distance,
    CASE
        WHEN true_distance >= 23.75 THEN 1
        ELSE 0
    END AS is_3pt_baseline
FROM shots_with_distance2
WHERE
    LOC_X IS NOT NULL
    AND LOC_Y IS NOT NULL;


