WITH source AS (
    SELECT *
    FROM {{ ref('stg_trials')  }}
),

dictionary AS (
    SELECT 
        LOWER(TRIM(trait)) AS trait, 
    FROM {{ ref('trait_dictionary') }}
    WHERE LOWER(TRIM(data_type)) = 'float' AND agent_enabled = TRUE
),

narrowed AS (
    SELECT
        * EXCLUDE ( _dlt_load_id, 
                    source_file, 
                    source_row,
                    origin,
                    tubshape,
                    fleshcolou,
                    skincolour, 
                    cook_com,
                    comments)
    FROM source
),

trait_unpivoted AS (
    FROM narrowed
    UNPIVOT INCLUDE NULLS 
    (value FOR trait IN (COLUMNS(* EXCLUDE (_dlt_id, variety, location, env_type, experiment_name, plot, year))))
),

final_trait_long AS (
    SELECT * EXCLUDE (d.trait)
    FROM trait_unpivoted AS l
    INNER JOIN dictionary AS d ON l.trait = d.trait
    WHERE l.value IS NOT NULL
)

SELECT * FROM final_trait_long

