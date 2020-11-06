CREATE VIEW online_by_role AS
SELECT Count(Username),
FROM users AS U
WHERE U.Status = 1
GROUP BY U.Role
