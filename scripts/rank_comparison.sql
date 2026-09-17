SELECT
    r.id, m.value,
    ROW_NUMBER() OVER (ORDER BY m.value DESC) AS rn,
    RANK() OVER (ORDER BY m.value DESC) AS rk,
    DENSE_RANK() OVER (ORDER BY m.value DESC) AS drk
FROM runs r
JOIN metrics m ON m.run_id = r.id AND m.name = 'accuracy';