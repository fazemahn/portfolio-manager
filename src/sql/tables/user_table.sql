CREATE TABLE `users` (
  `Username` varchar(255) NOT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `FirstName` varchar(45) DEFAULT NULL,
  `LastName` varchar(45) DEFAULT NULL,
  `Password` varchar(255) NOT NULL,
  `Role` int NOT NULL,
  `Status` int NOT NULL,
  PRIMARY KEY (`Username`)
);
