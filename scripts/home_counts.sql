SELECT
    (SELECT COUNT(*) FROM experiments) AS experiments,
    (SELECT COUNT(*) FROM model_types) AS model_types;
