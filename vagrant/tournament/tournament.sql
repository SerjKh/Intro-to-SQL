-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE TABLE players (
	id serial PRIMARY KEY,
	name text
);
CREATE TABLE matches (
	id serial,
	winner integer ,
	looser integer
);
CREATE VIEW playerStandingsView AS SELECT winners.id, winners.name, winners.wins, COUNT(matches.id) AS total FROM 
(SELECT players.id AS id, players.name AS name, COUNT(matches.id) AS wins FROM players LEFT JOIN matches on players.id = matches.winner GROUP BY players.id)
AS winners LEFT JOIN matches ON winners.id = matches.winner OR winners.id = matches.looser GROUP BY winners.id, winners.name, winners.wins ORDER BY winners.wins DESC;