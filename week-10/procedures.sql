CREATE OR REPLACE PROCEDURE upsert_user(new_name text, new_phone varchar(15))
AS $$
BEGIN
    INSERT INTO data (user_name, user_phone)
    VALUES (new_name, new_phone)
END;
$$;