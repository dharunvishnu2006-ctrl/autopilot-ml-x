CREATE VIRTUAL TABLE experiments_fts USING fts5(name, notes);

INSERT INTO experiments_fts (rowid, name, notes)
SELECT id, name, notes FROM experiments;