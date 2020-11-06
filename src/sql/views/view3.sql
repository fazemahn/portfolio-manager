CREATE VIEW users_with_comments
SELECT U.Username
FROM users AS U
WHERE U.Username = ANY (
    SELECT C.Username
        FROM comments AS C
)
