SELECT DATE(started_at) AS day, COUNT(*) AS runs
FROM runs
GROUP BY DATE(started_at)
ORDER BY day;
