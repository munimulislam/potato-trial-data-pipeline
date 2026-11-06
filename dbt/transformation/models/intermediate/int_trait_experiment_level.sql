-- int_trait_experiment_level
-- One row = one variety in one experiment × one trait.
--
-- Purpose: averages the replicate plots of each variety in each experiment.
-- Varieties have 1–3 plots per trial; averaging first means every variety counts
-- once when the trial average is calculated later. Without this, varieties with
-- more plots would pull the trial average towards themselves.
--
-- Source:  int_trait_plot_level.
-- value_avg = mean of the variety's plots; n_plots = number of plots averaged.

WITH source AS (
    SELECT *
    FROM {{ ref('int_trait_plot_level') }}
),

experiment_level_value_avg AS (
    SELECT 
        variety, 
        experiment_name, 
        trait, 
        year, 
        env_type, 
        location, 
        AVG(value) AS value, 
        COUNT(plot) AS n_plots
    FROM source
    GROUP BY variety, experiment_name, trait, year, env_type, location
)

SELECT * FROM experiment_level_value_avg