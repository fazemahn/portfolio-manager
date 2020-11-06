CREATE VIEW users_info AS
SELECT U.Username, U.Email, U.FirstName, U.LastName, U.Role, U.Status
FROM users AS U
