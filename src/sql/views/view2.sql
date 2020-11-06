CREATE VIEW detect_inappropriate_comment AS
SELECT Username
FROM users 
WHERE  Username = ANY
(SELECT Username FROM C WHERE C.Content LIKE “%bad_word%”)
GROUPBY Username; 
