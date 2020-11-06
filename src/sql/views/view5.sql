CREATE VIEW 
(SELECT U.Username
FROM users AS U
WHERE U.Username = ANY (
 SELECT C.Username
    FROM comments AS C
    GROUP BY C.Username
    HAVING Count(*) > 1
))
UNION
(
SELECT U.Username
FROM users AS U
WHERE U.Username = ANY (
 SELECT F.Username
    FROM favourites AS F
    GROUP BY F.Username
    HAVING Count(*) > 0
))
