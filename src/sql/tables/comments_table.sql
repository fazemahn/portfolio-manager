CREATE TABLE `comments` (
  `Username` VARCHAR(255) NOT NULL,
  `Ticker` VARCHAR(10) NOT NULL,
  `DateCreated` DATETIME NOT NULL,
  `Content` MEDIUMTEXT NULL,
  INDEX `USER_FKEY_idx` (`Username` ASC) VISIBLE,
  INDEX `STOCK_FKEY_idx` (`Ticker` ASC) VISIBLE,
  CONSTRAINT `USER_FKEY`
    FOREIGN KEY (`Username`)
    REFERENCES `monte_carlo`.`users` (`Username`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT `STOCK_FKEY`
    FOREIGN KEY (`Ticker`)
    REFERENCES `monte_carlo`.`stocks` (`Ticker`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION);
