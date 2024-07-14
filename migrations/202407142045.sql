-- migrate:up

ALTER TABLE papers ADD COLUMN translated_title VARCHAR(255);

-- migrate:down