CREATE OR REPLACE PROCEDURE public.add_new_user(IN new_name text, IN new_phone character varying)
LANGUAGE plpgsql
AS $procedure$
BEGIN
    INSERT INTO data (user_name, user_phone)
    VALUES (new_name, new_phone);

END;
$procedure$

CREATE OR REPLACE PROCEDURE public.add_many_new_users(IN names text[], IN phones character varying[])
LANGUAGE plpgsql
AS $procedure$
DECLARE
    i integer;
    tmp_name text;
    tmp_phone varchar;
begin
    for i IN 1 .. array_length(names, 1) loop
        tmp_name := names[i];
        tmp_phone := phones[i];
        if tmp_phone !~ '^\+?[0-9]{10,15}$' then
            CONTINUE;
        END IF;

        INSERT INTO data(user_name, user_phone)
        VALUES(tmp_name, tmp_phone)
        ON CONFLICT (user_name)
        DO UPDATE SET user_phone = EXCLUDED.user_phone;
    END LOOP;
END;
$procedure$

CREATE OR REPLACE PROCEDURE public.delete_users_data(IN search_data text)
LANGUAGE plpgsql
AS $procedure$
begin
DELETE FROM data where user_name = search_data or user_phone = search_data;
end;
$procedure$