CREATE VIEW num_times_favourited
SELECT F.ticker, Count(*)
FROM favourites AS F
GROUP BY F.ticker
