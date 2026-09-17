WITH RECURSIVE days(d) AS (
    SELECT DATE('2026-01-01')
    UNION ALL
    SELECT date(d, '+1 day') FROM days WHERE d < DATE('2026-01-10')
)
SELECT days.d, COUNT(r.id) AS runs
FROM days
LEFT JOIN runs r ON DATE(r.started_at) = days.d
GROUP BY days.d
ORDER BY days.d;