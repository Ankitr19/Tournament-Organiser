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
    WinsToZeroQuery = "UPDATE players SET Wins = 0;"
    MatchesToZeroQuery = "UPDATE players SET Matches = 0;"
    RemoveDataQuery = "DELETE FROM matches;"
    conn = connect()
    c =  conn.cursor()
    c.execute(WinsToZeroQuery)
    c.execute(MatchesToZeroQuery)
    c.execute(RemoveDataQuery)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
   #RemoveMatchesQuery = "DELETE FROM matches;"
    RemovePlayerQuery = "DELETE FROM players;"
    conn = connect()
    c = conn.cursor()
    c.execute(RemovePlayerQuery)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    CountQuery = "SELECT COUNT(playerId) as NUM FROM players;"
    conn = connect()
    c = conn.cursor()
    c.execute(CountQuery)
    result = int(c.fetchone()[0])
    conn.commit()
    conn.close()
    return result


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    RegisterQuery = "INSERT INTO players (Name) VALUES (%s);"
    conn = connect()
    c = conn.cursor()
    c.execute(RegisterQuery,(name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    StandingsQuery = "SELECT * FROM players ORDER BY Wins DESC;"
    conn = connect()
    c = conn.cursor()
    c.execute(StandingsQuery)
    result = c.fetchall()
    conn.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    AddMatchQuery = "INSERT INTO matches (WinnerId,LoserId) VALUES ({0},{1});".format(winner,loser)
    AddWinnerQuery = "UPDATE players SET Matches=Matches+1,Wins=Wins+1 WHERE playerId = {0};".format(winner)
    AddLoserQuery = "UPDATE players SET Matches=Matches+1 WHERE playerId = {0};".format(loser)
    conn = connect()
    c = conn.cursor()
    c.execute(AddMatchQuery)
    c.execute(AddWinnerQuery)
    c.execute(AddLoserQuery)
    conn.commit()
    conn.close()
 
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
    Pairings = []
    Players = playerStandings()
    if len(Players)<2:
        raise KeyError("Not enough players.")
    for i in range(0,len(Players),2):
        Pairings.append((Players[i][0], Players[i][1], Players[i+1][0], Players[i+1][1]))
    return Pairings


