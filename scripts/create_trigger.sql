CREATE TRIGGER update_best_accuracy
AFTER INSERT ON metrics
WHEN NEW.name = 'accuracy'
BEGIN
    UPDATE experiments
    SET best_accuracy = NEW.value
    WHERE id = (
        SELECT experiment_id FROM runs WHERE id = NEW.run_id
    )
    AND (
        best_accuracy IS NULL OR NEW.value > best_accuracy
    );
END;