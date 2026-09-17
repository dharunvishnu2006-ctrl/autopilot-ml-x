SELECT ex.id, ex.name
FROM experiments ex
LEFT JOIN runs r ON r.experiment_id = ex.id
WHERE r.id IS NULL;