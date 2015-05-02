#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = psycopg2.connect('dbname=tournament')
    c = DB.cursor()
    c.execute("DELETE FROM matches")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = psycopg2.connect('dbname=tournament')
    c = DB.cursor()
    c.execute("DELETE FROM players")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    """Returns the number of players currently registered."""
    DB = psycopg2.connect('dbname=tournament')
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM players")
    player_count = c.fetchone()[0]
    DB.close()
    return player_count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = psycopg2.connect('dbname=tournament')
    c = DB.cursor()
    c.execute("INSERT INTO players (player_name) values (%s)", (name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = psycopg2.connect('dbname=tournament')
    c = DB.cursor()
    c.execute("SELECT player_id, player_name, no_wins, no_matches " +
              "FROM view_match_results ORDER BY no_wins DESC, " +
              "no_matches ASC, no_draws DESC")
    results = c.fetchall()
    DB.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    DB = psycopg2.connect('dbname=tournament')
    c = DB.cursor()
    c.execute("INSERT INTO matches (player1_id,player2_id,winner_id) " +
              "values (%s,%s,%s)",
              (winner, loser, winner))
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    results = []
    player = 1
    DB = psycopg2.connect('dbname=tournament')
    c = DB.cursor()
    c.execute("SELECT player_id, player_name FROM view_current_round " +
              "ORDER BY no_wins, no_draws")
    sql_results = c.fetchall()
    for sql_result in sql_results:
        if player == 1:
            players = [sql_result[0]]
            players.append(sql_result[1])
            player = 2
        else:
            results.append([players[0], players[1], sql_result[0],
                            sql_result[1]])
            player = 1
    DB.close()

    return results
