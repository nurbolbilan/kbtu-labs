CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
BEGIN
    SELECT user_id INTO v_contact_id
    FROM contacts
    WHERE user_name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Контакт "%" не найден', p_contact_name;
    END IF;

    INSERT INTO phones (contact_id, phone, phone_type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
    v_group_id   INT;
BEGIN
    SELECT user_id INTO v_contact_id
    FROM contacts
    WHERE user_name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Контакт "%" не найден', p_contact_name;
    END IF;

from connect import conn

sql_create = """
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    user_id   INT,
    user_name VARCHAR,
    email     VARCHAR,
    birthday  DATE,
    group_name VARCHAR,
    phones    TEXT
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.user_id,
        c.user_name,
        c.email,
        c.birthday,
        g.group_name,
        STRING_AGG(p.phone || ' (' || p.phone_type || ')', ', ')
            OVER (PARTITION BY c.user_id) AS phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.group_id
    LEFT JOIN phones p ON c.user_id = p.contact_id
    WHERE
        c.user_name ILIKE '%' || p_query || '%'
        OR c.email   ILIKE '%' || p_query || '%'
        OR p.phone   ILIKE '%' || p_query || '%'
    ORDER BY c.user_name;
END;
$$;