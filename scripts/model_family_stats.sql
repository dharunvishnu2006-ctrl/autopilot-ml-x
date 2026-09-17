SELECT
    r.model_type_id,
    COUNT(*) AS run_count,
    AVG(m.value) AS avg_accuracy
FROM runs r
JOIN metrics m ON m.run_id = r.id AND m.name = 'accuracy'
WHERE r.status = 'done'
GROUP BY r.model_type_id
HAVING COUNT(*) >= 1;