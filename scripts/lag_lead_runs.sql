SELECT
    r.id, r.started_at, m.value,
    LAG(m.value) OVER (ORDER BY r.started_at) AS prev_accuracy,
    LEAD(m.value) OVER (ORDER BY r.started_at) AS next_accuracy
FROM runs r
LEFT JOIN metrics m ON m.run_id = r.id AND m.name = 'accuracy'
ORDER BY r.started_at;