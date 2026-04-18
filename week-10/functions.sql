CREATE OR REPLACE FUNCTION public.returns_all_records()
RETURNS TABLE(first_name text, last_name text, phone character varying)
LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY
    SELECT
        split_part(user_name, ' ', 1)::text,
        split_part(user_name, ' ', 2)::text,
        user_phone
    FROM data;
END;
$function$

CREATE OR REPLACE FUNCTION public.get_users_paged(p_limit integer, p_offset integer)
RETURNS TABLE(u_name text, u_phone character varying)
LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY
    SELECT
        user_name::text,
        user_phone::varchar
    FROM data
    ORDER BY user_name
    LIMIT p_limit
    OFFSET p_offset;
END;
$function$