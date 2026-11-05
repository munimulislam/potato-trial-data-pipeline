WITH source AS (
    SELECT *
    FROM {{ source('raw_trial_data', 'trials') }}
),

dictionary AS (
    SELECT 
        LOWER(TRIM(trait)) AS trait, 
        valid_min, 
        valid_max
    FROM {{ ref('trait_dictionary') }}
    WHERE LOWER(TRIM(data_type)) = 'float'
),

loc_map AS (
    SELECT
        LOWER(TRIM(raw_location)) AS location_key,
        LOWER(TRIM(location))     AS location,
        LOWER(TRIM(env_type))     AS env_type
    FROM {{ ref('location_map') }}
),

exclusions AS (
    SELECT DISTINCT
        LOWER(TRIM(experiment_name))    AS experiment_name,
        LOWER(TRIM(name))               AS trait
    FROM {{ ref('trait_exclusions') }}
),

renamed AS (
    SELECT
        * EXCLUDE (name1, experiment_name, location, plot, year),
        LOWER(TRIM(name1))              AS variety,
        LOWER(TRIM(experiment_name))    AS experiment_name,
        LOWER(TRIM(location))           AS location,
        CAST(plot AS BIGINT)            AS plot,
        CAST(year AS INTEGER)           AS year
    FROM source
),

-- Non-trait columns: identifiers, text traits, lineage. Keep this list in sync with the
-- source; any text column missing here makes the UNPIVOT below fail with a type error.
row_attributes AS (
    SELECT
        _dlt_id, 
        _dlt_load_id,
        source_file, 
        source_row,
        origin,
        variety, 
        experiment_name, 
        plot, 
        year,
        location,
        tubshape,
        fleshcolou,
        skincolour,
        cook_com, 
        comments
    FROM renamed
),

-- Only the plot id, the experiment key and the numeric trait columns
trait_input AS (
    SELECT 
        * EXCLUDE (_dlt_load_id, 
                    source_file, 
                    source_row,
                    origin,
                    variety, 
                    location, 
                    plot, 
                    year,
                    tubshape,
                    fleshcolou,
                    skincolour, 
                    cook_com,
                    comments)
    FROM renamed
),

-- Every numeric trait column -> one row per (plot, trait)
trait_long AS (
    SELECT *
    FROM trait_input
    UNPIVOT INCLUDE NULLS (
        raw_value FOR trait IN (COLUMNS(* EXCLUDE (_dlt_id, experiment_name)))
    )
),

trait_rules AS (
    SELECT
        long._dlt_id,
        long.trait,
        long.raw_value,
        x.trait IS NOT NULL                                                 AS is_excluded,
        long.raw_value < dict.valid_min OR long.raw_value > dict.valid_max  AS is_out_of_range,
        dict.trait IS NOT NULL
            AND MAX(ABS(long.raw_value)) OVER (PARTITION BY long.experiment_name, long.trait) = 0
                                                                        AS is_all_zero_experiment
    FROM trait_long         AS long
    LEFT JOIN dictionary    AS dict    ON LOWER(long.trait) = dict.trait
    LEFT JOIN exclusions    AS x       ON long.experiment_name = x.experiment_name AND LOWER(long.trait) = x.trait
),

trait_cleaned AS (
    SELECT
        _dlt_id,
        trait,
        CASE
            WHEN is_excluded OR is_out_of_range OR is_all_zero_experiment THEN NULL
            ELSE raw_value
        END AS value
    FROM trait_rules
),

-- Back to wide: one column per trait, same names as the source
traits_wide AS (
    PIVOT trait_cleaned
    ON trait
    USING FIRST(value)
    GROUP BY _dlt_id
),

joined AS (
    SELECT
        a.* EXCLUDE (location),
        m.location,
        m.env_type,
        w.* EXCLUDE (_dlt_id)
    FROM row_attributes AS a
    JOIN traits_wide    AS w  ON a._dlt_id = w._dlt_id
    LEFT JOIN loc_map   AS m  ON LOWER(a.location) = m.location_key
),

yield_merged AS (
    SELECT
        *,
        COALESCE(finalyield, yield_total_t_ha) AS yield,
    FROM joined
)

SELECT * FROM yield_merged