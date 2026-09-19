SELECT model_type_id, COUNT(*) AS run_count
FROM runs
GROUP BY model_type_id
UNION ALL
SELECT NULL AS model_type_id, COUNT(*) AS run_count
FROM runs;