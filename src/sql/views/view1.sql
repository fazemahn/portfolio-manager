CREATE VIEW comments_on_favourites AS
SELECT U.Username, C.Content, C.DateCreated, C.Ticker
FROM users AS U
JOIN comments AS C 
JOIN favourites AS F 
ON U.Username = F.Username 
    AND U.Username = C.Username
    AND C.Ticker = F.Ticker
