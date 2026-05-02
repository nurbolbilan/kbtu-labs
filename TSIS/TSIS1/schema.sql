-- PhoneBook database schema
-- ══════════════════════════════════════════════════════════

-- Drop existing tables (in correct order to respect FK constraints)
DROP TABLE IF EXISTS phones   CASCADE;
DROP TABLE IF EXISTS contacts CASCADE;
DROP TABLE IF EXISTS groups   CASCADE;

-- ── Groups ─────────────────────────────────────────────────
CREATE TABLE groups (
    group_id   SERIAL PRIMARY KEY,
    group_name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO groups (group_name) VALUES
    ('Family'),
    ('Work'),
    ('Friend'),
    ('Other');

-- ── Contacts ───────────────────────────────────────────────
CREATE TABLE contacts (
    user_id    SERIAL PRIMARY KEY,
    user_name  VARCHAR(50)  NOT NULL UNIQUE,
    email      VARCHAR(255),
    birthday   DATE,
    group_id   INT REFERENCES groups(group_id)
);

-- ── Phones ─────────────────────────────────────────────────
CREATE TABLE phones (
    phone_id   SERIAL        PRIMARY KEY,
    contact_id INT           NOT NULL REFERENCES contacts(user_id) ON DELETE CASCADE,
    phone      VARCHAR(30)   NOT NULL,
    phone_type VARCHAR(10)   NOT NULL CHECK (phone_type IN ('home', 'work', 'mobile'))
);