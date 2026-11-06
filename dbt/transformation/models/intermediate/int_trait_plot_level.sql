-- int_trait_plot_level
-- One row = one plot × one trait (cleaned value).
--
-- Purpose: turns the wide staging table (one column per trait) into a long table
-- (one row per trait), so every trait can be processed with the same SQL.
--
-- Source:  stg_trials (already cleaned: exclusions, valid ranges, all-zero trials removed).
-- Traits:  only numeric traits in trait_dictionary with agent_enabled = TRUE.
-- Rows:    empty values are dropped.
-- Rules:   none. All cleaning happens in stg_trials, so wide and long always agree.

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
    UNPIVOT
    (value FOR trait IN (COLUMNS(* EXCLUDE (_dlt_id, variety, location, env_type, experiment_name, plot, year))))
),

final_trait_long AS (
    SELECT * EXCLUDE (d.trait)
    FROM trait_unpivoted AS l
    INNER JOIN dictionary AS d ON l.trait = d.trait
)

SELECT * FROM final_trait_long

