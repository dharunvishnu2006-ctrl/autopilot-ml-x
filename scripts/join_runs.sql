SELECT
    r.id AS run_id,
    ex.name AS experiment_name,
    mt.name AS model_name
FROM runs r
JOIN experiments ex ON ex.id = r.experiment_id
JOIN model_types mt ON mt.id = r.model_type_id;