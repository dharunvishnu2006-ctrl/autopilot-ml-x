SELECT
    a.id AS run_a,
    b.id AS run_b,
    a.model_type_id
FROM runs a
JOIN runs b ON a.model_type_id = b.model_type_id
WHERE a.id < b.id;