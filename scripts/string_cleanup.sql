SELECT
    ex.id,
    COALESCE(ex.notes, 'No notes') AS notes,
    SUBSTR(mt.name, 1, 3) AS model_prefix
FROM experiments ex
JOIN runs r ON r.experiment_id = ex.id
JOIN model_types mt ON mt.id = r.model_type_id;