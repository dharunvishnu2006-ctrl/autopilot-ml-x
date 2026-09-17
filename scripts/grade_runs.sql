SELECT
    r.id,
    m.value AS accuracy,
    CASE
        WHEN m.value > 0.95 THEN 'A'
        WHEN m.value > 0.90 THEN 'B'
        WHEN m.value > 0.80 THEN 'C'
        ELSE 'D'
    END AS grade
FROM runs r
JOIN metrics m ON m.run_id = r.id AND m.name = 'accuracy';