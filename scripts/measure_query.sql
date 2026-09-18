SELECT r.id, r.started_at
FROM runs r
WHERE r.experiment_id = 1
ORDER BY r.started_at DESC
LIMIT 10;