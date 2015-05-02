-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players ( player_id SERIAL PRIMARY KEY,
			 player_name VARCHAR(40) NOT NULL UNIQUE );

CREATE TABLE matches ( matchid SERIAL PRIMARY KEY,
			player1_id INTEGER NOT NULL REFERENCES players (player_id),
			player2_id INTEGER NOT NULL REFERENCES players (player_id),
			winner_id INTEGER REFERENCES players (player_id),
			draw BOOLEAN );

CREATE VIEW view_match_results AS
			select p.player_id, p.player_name,
			(select count(*) from matches m
			where m.player1_id = p.player_id or m.player2_id = p.player_id) as no_matches,
			(select count(*) from matches m
			where m.winner_id = p.player_id) as no_wins,
			(select count(*) from matches m
			where (m.player1_id = p.player_id or m.player2_id = p.player_id) and draw = true) as no_draws
			from players p;

CREATE VIEW view_current_round AS
			select vmr.player_id, vmr.player_name, vmr.no_matches,
  			vmr.no_wins, vmr.no_draws
			from view_match_results vmr
			where vmr.no_matches =
			  (select min(no_matches) from view_match_results)