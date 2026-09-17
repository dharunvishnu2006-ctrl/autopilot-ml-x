SELECT
    r.id, m.value,
    AVG(m.value) OVER (
        ORDER BY r.started_at
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3
FROM runs r
JOIN metrics m ON m.run_id = r.id AND m.name = 'accuracy'
ORDER BY r.started_at;