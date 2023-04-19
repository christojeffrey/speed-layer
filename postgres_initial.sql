-- social_media: string, timestamp: 2023-01-01 00:00:00, count, unique_count, created_at, updated_at. primary key(social_media, timestamp)
CREATE TABLE IF NOT EXISTS social_media_stats (
    social_media VARCHAR(255) NOT NULL,
    media_timestamp TIMESTAMP NOT NULL,
    count INT NOT NULL,
    unique_count INT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (social_media, media_timestamp)
);