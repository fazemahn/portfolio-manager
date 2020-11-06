CREATE TABLE `favourites` (
  `Username` varchar(255) NOT NULL,
  `Ticker` varchar(10) NOT NULL,
  PRIMARY KEY (`Username`,`Ticker`),
  KEY `STOCK_FKEY_idx` (`Ticker`),
  CONSTRAINT `FAV_STOCK_FKEY` FOREIGN KEY (`Ticker`) REFERENCES `stocks` (`Ticker`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FAV_USER_FKEY` FOREIGN KEY (`Username`) REFERENCES `users` (`Username`) ON DELETE CASCADE ON UPDATE CASCADE
);
