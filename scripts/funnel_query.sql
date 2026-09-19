SELECT
    COUNT(*) FILTER (WHERE status IS NOT NULL) AS submitted,
    COUNT(*) FILTER (WHERE status IN ('running','done')) AS started,
    COUNT(*) FILTER (WHERE status = 'done') AS completed,
    ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'done')
        / NULLIF(COUNT(*) FILTER (WHERE status IS NOT NULL), 0), 1
    ) AS pct_completed
FROM runs;