DROP TABLE ParentPostDetails;
CREATE TABLE IF NOT EXISTS ParentPostDetails (
	parentPost_id VARCHAR(20) PRIMARY KEY NOT NULL,
    url VARCHAR(300),
    timecreated_utc VARCHAR(100) NOT NULL,
    subreddit_id VARCHAR(100) NOT NULL,
    subreddit VARCHAR(100) NOT NULL,
    title VARCHAR(400) NOT NULL,
    selftext TEXT(),
    score INTEGER,
    author VARCHAR(100) NOT NULL,
    childrenComments BLOB
);