-- Deployment creation sql script for codebits
-- Scott Kemperman
-- Nov 24, 2018


DROP TABLE if EXISTS codebit_topic_jnc;
DROP TABLE if EXISTS chunk;
DROP TABLE if EXISTS codebits;
DROP TABLE if EXISTS topics;
DROP TABLE if EXISTS chunk_types;
DROP TABLE if EXISTS codebit_types;

CREATE TABLE topics (
    id INTEGER auto_increment,
    name VARCHAR(32),
    PRIMARY KEY(id)
);
insert into topics (name) values
    ('Health'), ('Productivity'), ('Python'), ('Cloud'), ('Infiniti');

CREATE TABLE chunk_types (
    id INTEGER auto_increment,
    name VARCHAR(32),
    PRIMARY KEY(id)
);
insert into chunk_types (name) values
    ('Plain Text'), ('Quote'), ('Phone Number'), ('Code'), ('CLI'),
    ('Credentials'), ('Link'), ('Date'), ('Time'), ('Address');

CREATE TABLE codebit_types (
    id INTEGER auto_increment,
    name VARCHAR(32),
    PRIMARY KEY(id)
);
insert into codebit_types (name) values
    ('Reminder'), ('Chill'), ('Important');

CREATE TABLE codebits (
    id INTEGER auto_increment,
    codebitType_id INTEGER,
    PRIMARY KEY(id),
    FOREIGN KEY(codebitType_id) REFERENCES codebit_types(id)
);

CREATE TABLE chunks (
    id INTEGER auto_increment,
    content TEXT,
    chunkType_id INTEGER,
    codebit_id INTEGER,
    PRIMARY KEY(id),
    FOREIGN KEY(chunkType_id) REFERENCES chunk_types(id),
    FOREIGN KEY(codebit_id) REFERENCES codebits(id) ON DELETE cascade
);

CREATE TABLE codebit_topic_jnc (
    codebit_id INTEGER,
    topic_id INTEGER,
    PRIMARY KEY(codebit_id, topic_id),
    FOREIGN KEY(codebit_id) REFERENCES codebits(id) ON DELETE cascade,
    FOREIGN KEY(topic_id) REFERENCES topics(id) ON DELETE cascade
);

/*
freemysqlhosting.net creds:
    u/n: scott.kemperman@gmail.com
    pwd: (KBjR8u!IJ9TYWnB

Server: sql3.freemysqlhosting.net
Name: sql3264960
Username: sql3264960
Password: 4qkCEeX9j6
Port number: 3306
*/


