WITH source AS (
    SELECT *
    FROM {{ ref('int_trait_plot_level') }}
),

experiment_level_avg AS (
    SELECT 
        variety, 
        experiment_name, 
        trait, 
        year, 
        env_type, 
        location, 
        AVG(value) AS value_avg, 
        COUNT(plot) AS n_plots
    FROM source
    GROUP BY variety, experiment_name, trait, year, env_type, location
)

SELECT * FROM experiment_level_avg