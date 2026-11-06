
WITH source AS (
    SELECT *
    FROM {{ ref('int_trait_experiment_level') }}
),

trait_exp_avg AS (
    SELECT 
        trait, 
        experiment_name, 
        AVG(value) AS value, 
        COUNT(variety) AS n_varieties
    FROM source
    GROUP BY trait, experiment_name
),

fct_variety_trial_relative_performance AS (
    SELECT
        s.variety,
        s.experiment_name,
        s.year,
        s.location,
        s.env_type,
        s.trait,
        s.n_plots,
        s.value AS plot_mean,
        trial_avg.value AS experiment_mean,
        100.0 * s.value / NULLIF(trial_avg.value, 0) AS experiment_mean_pct,
        trial_avg.n_varieties
    FROM source AS s
    LEFT JOIN trait_exp_avg AS trial_avg 
        ON s.trait = trial_avg.trait AND s.experiment_name = trial_avg.experiment_name
    WHERE trial_avg.n_varieties >= {{ var('min_varieties_per_trial') }}
)

SELECT * FROM fct_variety_trial_relative_performance
