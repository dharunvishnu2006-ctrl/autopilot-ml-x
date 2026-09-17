SELECT
    COUNT(*) AS total_runs,
    COUNT(m.value) AS runs_with_accuracy,
    AVG(m.value) AS avg_accuracy,
    MAX(m.value) AS best_accuracy,
    MIN(m.value) AS worst_accuracy
FROM runs r
LEFT JOIN metrics m ON m.run_id = r.id AND m.name = 'accuracy';