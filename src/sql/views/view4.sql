CREATE VIEW user_comments AS
SELECT U.Username, C.Content
FROM U
FULL JOIN C ON U.Username = C.Username
ORDER BY C.Content;