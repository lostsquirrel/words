CREATE TABLE `words`.`wordbook`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `guid` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `word_amount` int NOT NULL DEFAULT 0,
  `create_time` datetime NOT NULL,
  `modified_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `words`.`invite_code`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `code` char(32) NOT NULL,
  `create_time` datetime NOT NULL,
  `modified_time` datetime NOT NULL,
  `bind` 
  int UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
);

CREATE TABLE `words`.`user`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `device_type` tinyint NOT NULL,
  `create_time` datet-ime NOT NULL,
  `modified_time` datetime NOT NULL,
  `state` tinyint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
);

CREATE TABLE `words`.`token`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `token` char(32) NOT NULL,
  `user_id` int UNSIGNED NOT NULL,
  `create_time` datetime NOT NULL,
  `modified_time` datetime NOT NULL,
  `state` tinyint UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
);

CREATE TABLE `words`.`words`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `guid` int NOT NULL,
  `word` varchar(255) NOT NULL,
  `phonetic` varchar(1000) NOT NULL,
  `description` varchar(255) NOT NULL,
  `score` int UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `word_index`(`word`) USING BTREE
);

CREATE TABLE `words`.`plan`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` int UNSIGNED NOT NULL,
  `book_id` int UNSIGNED NOT NULL,
  `strategy` tinyint NOT NULL,
  `amount_per_day` int NOT NULL,
  `default` tinyint NOT NULL,
  `state` tinyint NOT NULL,
  `phonetic` tinyint NOT NULL DEFAULT 0,
  `create_time` datetime NOT NULL,
  `modified_time` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

CREATE TABLE `words`.`memorize`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `plan_id` int UNSIGNED NOT NULL,
  `word_id` int UNSIGNED NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
);