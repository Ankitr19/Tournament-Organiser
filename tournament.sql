-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players
(
	playerId SERIAL PRIMARY KEY,
	Name VARCHAR(50) NOT NULL,
	Wins INTEGER DEFAULT 0,
	Matches INTEGER DEFAULT 0
);

CREATE TABLE matches
(
	MatchId SERIAL PRIMARY KEY,
	WinnerId INTEGER,
	LoserId INTEGER,
	FOREIGN KEY (WinnerId) REFERENCES players(playerId),
	FOREIGN KEY (LoserId) REFERENCES players(playerId)
);

