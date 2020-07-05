DROP TABLE repostats;

CREATE TABLE repostats (
    repo varchar(255) NOT NULL,
    viewDate int NOT NULL,
    viewCount int NOT NULL,
    uniques int NOT NULL,
    CONSTRAINT REPO_DATE PRIMARY KEY (repo,viewDate)
);