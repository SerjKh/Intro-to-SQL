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
    DB = connect()
    cur = DB.cursor()
    cur.execute("DELETE from matches;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cur = DB.cursor()
    cur.execute("DELETE from players;")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cur = DB.cursor()
    cur.execute("SELECT COUNT(players.id) from players;")
    numOfPlayers = cur.fetchall()[0][0]
    DB.close()
    return numOfPlayers

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cur = DB.cursor()
    cur.execute("INSERT INTO players (name) VALUES (%s)" , (name,))
    DB.commit()
    DB.close()

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
    playersList = []
    DB = connect()
    cur = DB.cursor()
    cur.execute("SELECT * FROM playerStandingsView;")
    for player in cur.fetchall():
        playersList.append((player[0], player[1], player[2], player[3]))
    DB.close()
    return playersList

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    cur = DB.cursor()
    cmd = """ INSERT INTO matches (winner,looser) VALUES ('{0}','{1}') """
    cur.execute(cmd.format(winner,loser))
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
    players = playerStandings()
    pairs = []
    for i in range(0,len(players)/2+1,2):
        pairs.append((players[i][0],players[i][1],players[i+1][0],players[i+1][1]))
    return pairs

