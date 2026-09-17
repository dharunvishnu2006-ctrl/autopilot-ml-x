CREATE TABLE datasets (
    id INTEGER PRIMARY KEY,
    sha256 TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    rows INTEGER,
    cols INTEGER,
    first_seen TEXT
);

CREATE TABLE model_types (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    family TEXT
);

CREATE TABLE experiments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    dataset_id INTEGER REFERENCES datasets(id),
    created_at TEXT,
    notes TEXT
);

CREATE TABLE runs (
    id INTEGER PRIMARY KEY,
    experiment_id INTEGER REFERENCES experiments(id),
    model_type_id INTEGER REFERENCES model_types(id),
    status TEXT,
    source TEXT,
    started_at TEXT,
    finished_at TEXT,
    hyperparams TEXT
    CHECK (finished_at IS NULL OR finished_at >= started_at)
);

CREATE TABLE metrics (
    id INTEGER PRIMARY KEY,
    run_id INTEGER REFERENCES runs(id),
    name TEXT NOT NULL,
    value REAL
);