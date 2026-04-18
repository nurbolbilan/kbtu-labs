CREATE OR REPLACE FUNCTION returns_all_records()
RETURNS TABLE(firstname text, lastname text, phone text) AS $$
BEGIN
    RETURN QUERY
    SELECT
        split_part(user_name, ' ', 1),
        split_part(user_name, ' ', 2),
        user_phone
    FROM data;
END;
$$ LANGUAGE plpgsql;