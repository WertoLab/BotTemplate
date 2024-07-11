-- migrate:up

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    username VARCHAR(255)
);

CREATE TABLE papers (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- migrate:down