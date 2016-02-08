CREATE TABLE IF NOT EXISTS ParentPostDetails (
    parentPost_id TEXT PIMARY KEY NOT NULL,
    url TEXT,
    timecreated_utc INTEGER NOT NULL,
    subreddit_id TEXT NOT NULL,
    subreddit TEXT NOT NULL,
    title TEXT NOT NULL,
    score INTEGER,
    author TEXT NOT NULL,
    childrenComments BLOB
);



INSERT INTO ParentPostDetails (parentPost_id,url,timecreated_utc,subreddit_id,subreddit,title,score,author) 
VALUES ("t3_34fpen","www.google.com",1430438400,"t5_2qjvn","relationships","on whether you love someone?",26,"[deleted]");


INSERT INTO ParentPostDetails (parentPost_id,url,timecreated_utc,subreddit_id,subreddit,title,score,author) 
VALUES ("t3_34gmag","www.yahoo.com",1430438400,"t5_2sqho","GlobalOffensive","Who benefited the most from the NA roster shuffle? Who got screwed over the most?",12,"[deleted]");
t3_34gmag