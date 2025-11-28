-- Use a schema to organize the tables
CREATE SCHEMA blog;

CREATE TABLE blog.users (
    id         BIGSERIAL PRIMARY KEY,
    username   TEXT NOT NULL UNIQUE,
    email      TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE blog.posts (
    id         BIGSERIAL PRIMARY KEY,
    user_id    BIGINT NOT NULL,
    title      TEXT NOT NULL,
    content    TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
        REFERENCES blog.users(id)
        ON DELETE CASCADE
);

-- Create an index on the foreign key for faster lookups
CREATE INDEX idx_posts_user_id ON blog.posts(user_id);
