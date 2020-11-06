CREATE VIEW all_suspended_users
SELECT U.Username, U.Email
FROM users AS U
WHERE U.Status = 2
