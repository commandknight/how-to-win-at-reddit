CREATE TABLE `ParentPostDetails` (
  `parentPost_id`    VARCHAR(20)  NOT NULL,
  `url`              VARCHAR(500) DEFAULT NULL,
  `timecreated_utc`  VARCHAR(100) NOT NULL,
  `subreddit_id`     VARCHAR(100) NOT NULL,
  `subreddit`        VARCHAR(100) NOT NULL,
  `title`            VARCHAR(800) NOT NULL,
  `selftext`         TEXT,
  `score`            INT(11)      DEFAULT NULL,
  `author`           VARCHAR(100) NOT NULL,
  `childrenComments` BLOB,
  PRIMARY KEY (`parentPost_id`)
)
  ENGINE = InnoDB;