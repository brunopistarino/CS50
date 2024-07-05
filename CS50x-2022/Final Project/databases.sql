CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    hash TEXT NOT NULL,
    PRIMARY KEY(id)
);

CREATE UNIQUE INDEX email ON users (email);

CREATE TABLE IF NOT EXISTS sections (
    id INTEGER NOT NULL,
    emoji TEXT NOT NULL,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS links (
    id INTEGER NOT NULL,
    name TEXT NOT NULL,
    link TEXT NOT NULL,
    section_id INTEGER NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(section_id) REFERENCES sections(id)
);