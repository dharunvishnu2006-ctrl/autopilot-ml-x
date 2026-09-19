SELECT
    id,
    json_extract(hyperparams, '$.max_depth') AS depth,
    json_extract(hyperparams, '$.learning_rate') AS lr
FROM runs
WHERE id = 1;