CREATE VIEW detect_inappropriate_comment AS
SELECT Username
FROM users 
WHERE  Username = ANY
(SELECT comments.Username FROM comments WHERE comments.Content LIKE ‘%bad_word%’)
GROUPBY Username
