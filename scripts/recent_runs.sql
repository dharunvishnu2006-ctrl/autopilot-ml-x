SELECT
    mt.name AS model,
    r.status,
    acc.value AS accuracy,
    dur.value AS duration,
    r.started_at AS started_at
FROM runs r
JOIN model_types mt ON mt.id = r.model_type_id
LEFT JOIN metrics acc ON acc.run_id = r.id AND acc.name = 'accuracy'
LEFT JOIN metrics dur ON dur.run_id = r.id AND dur.name = 'duration'
ORDER BY r.started_at DESC, r.id DESC
LIMIT ?;
