CREATE TABLE `words`.`wordbook`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `guid` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `word_amount` int NOT NULL DEFAULT 0,
  `create_time` datetime NOT NULL,
  `modified_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
);