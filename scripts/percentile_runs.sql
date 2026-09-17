SELECT
    r.id, m.value,
    RANK() OVER (ORDER BY m.value DESC) AS rk,
    PERCENT_RANK() OVER (ORDER BY m.value DESC) AS pct_rank
FROM runs r
JOIN metrics m ON m.run_id = r.id AND m.name = 'accuracy';