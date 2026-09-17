SELECT
    r.id, m.value,
    FIRST_VALUE(m.value) OVER (
        PARTITION BY r.experiment_id
        ORDER BY r.started_at
    ) AS baseline
FROM runs r
LEFT JOIN metrics m ON m.run_id = r.id AND m.name = 'accuracy'
ORDER BY r.started_at;