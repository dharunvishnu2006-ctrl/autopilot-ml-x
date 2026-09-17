SELECT * FROM (
    SELECT
        r.id,
        r.experiment_id,
        m.value,
        RANK() OVER (
            PARTITION BY r.experiment_id
            ORDER BY m.value DESC
        ) AS rk
    FROM runs r
    JOIN metrics m ON m.run_id = r.id AND m.name = 'accuracy'
) t
WHERE t.rk = 1;