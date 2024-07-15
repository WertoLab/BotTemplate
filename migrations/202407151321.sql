-- migrate:up

CREATE TABLE titles (
    id SERIAL PRIMARY KEY,
    original_title VARCHAR(255) NOT NULL,
    translated_title VARCHAR(255)
);

-- migrate:down
