WITH ranked AS (
    SELECT
        r.id, r.experiment_id, m.value,
        RANK() OVER (
            PARTITION BY r.experiment_id
            ORDER BY m.value DESC
        ) AS rk
    FROM runs r
    JOIN metrics m ON m.run_id = r.id AND m.name = 'accuracy'
),
best AS (
    SELECT * FROM ranked WHERE rk = 1
)
SELECT ex.name, mt.name, best.value
FROM best
JOIN experiments ex ON ex.id = best.experiment_id
JOIN runs r ON r.id = best.id
JOIN model_types mt ON mt.id = r.model_type_id;