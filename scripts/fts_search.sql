SELECT rowid, name, notes
FROM experiments_fts
WHERE experiments_fts MATCH 'first';