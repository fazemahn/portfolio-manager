CREATE VIEW all_registered_emails
SELECT U.Username, U.Email
FROM users AS U
WHERE U.Email IS NOT NULL
