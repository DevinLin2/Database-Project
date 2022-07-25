import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='matchmaking',
                                         user='root',
                                         password='Destroyer21823iw.')
    # if connection.is_connected():
    #     db_Info = connection.get_server_info()
    #     print("Connected to MySQL Server version ", db_Info)
    #     cursor = connection.cursor()
    #     cursor.execute("select database();")
    #     record = cursor.fetchone()
    #     print("You're connected to database: ", record)
    account_table = """CREATE TABLE Account (
                        AccID int(15) NOT NULL,
                        Name varchar(30) NOT NULL,
                        DiscAccUsername varchar(30),
                        Email varchar(250) NOT NULL,
                        PRIMARY KEY (AccID))"""
    game_table = """CREATE TABLE Game (
                    Name varchar(30) NOT NULL,
                    DownloadLink varchar(250) NOT NULL, 
                    DeveloperName varchar(30) NOT NULL,
                    Genre varchar(20) NOT NULL,
                    Cost int(10) NOT NULL,
                    PlayerBase int(30) NOT NULL,
                    MoneyMade int(30) NOT NULL,
                    PRIMARY KEY (Name))"""
    player_table = """CREATE TABLE Player (
                        PlayerID varchar(30) NOT NULL,
                        Name varchar(30) NOT NULL,
                        Playstyle varchar(30) NOT NULL,
                        ELO int(30) NOT NULL,
                        TimePlayed int(15) NOT NULL,
                        MoneySpent int(30) NOT NULL,
                        PRIMARY KEY (PlayerID, Name),
                        CONSTRAINT Player_Game_Name_fk FOREIGN KEY (Name) REFERENCES Game(Name) 
                            ON UPDATE CASCADE ON DELETE CASCADE)"""
    team_table = """CREATE TABLE Team (
                    TeamID int(15) NOT NULL,
                    Captain varchar(30) NOT NULL,
                    Size int(10) NOT NULL,
                    Wins int(10) NOT NULL, 
                    Loses int(10) NOT NULL, 
                    PrizeMoneyEarned int(30) NOT NULL,
                    PRIMARY KEY (TeamID, Captain))"""
    owns_table = """CREATE TABLE Owns (
                    Name varchar(30) NOT NULL,
                    PlayerID varchar(30) NOT NULL,
                    AccID int(15) NOT NULL,
                    PRIMARY KEY (Name, PlayerID, AccID),
                    CONSTRAINT Owns_Game_Name_fk FOREIGN KEY (Name) REFERENCES Game(Name) 
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    CONSTRAINT Owns_Player_PlayerID_fk FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID)
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    CONSTRAINT Owns_Account_fk FOREIGN KEY (AccID) REFERENCES Account(AccID)
                        ON UPDATE CASCADE ON DELETE CASCADE)"""
    has_table = """CREATE TABLE Has (
                    Name varchar(30) NOT NULL,
                    Captain varchar(30) NOT NULL,
                    TeamID int(15) NOT NULL,
                    PRIMARY KEY (Name, PlayerID, Captain),
                    CONSTRAINT Has_Game_Name_fk FOREIGN KEY (Name) REFERENCES Game(Name) 
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    CONSTRAINT Plays_For_Team_fk FOREIGN KEY (Captain, TeamID) REFERENCES Team(Captain, TeamID)
                        ON UPDATE CASCADE ON DELETE CASCADE)"""
    plays_for_table = """CREATE TABLE Plays_For (
                    Name varchar(30) NOT NULL,
                    PlayerID varchar(30) NOT NULL,
                    Captain varchar(30) NOT NULL,
                    TeamID int(15) NOT NULL,
                    Role varchar(30) NOT NULL,
                    PRIMARY KEY (Name, PlayerID, Captain),
                    CONSTRAINT Plays_For_Game_Name_fk FOREIGN KEY (Name) REFERENCES Game(Name) 
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    CONSTRAINT Plays_For_Player_PlayerID_fk FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID)
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    CONSTRAINT Plays_For_Team_fk FOREIGN KEY (Captain, TeamID) REFERENCES Team(Captain, TeamID)
                        ON UPDATE CASCADE ON DELETE CASCADE)"""
    plays_table = """CREATE TABLE Plays (
                    PlayerID varchar(30) NOT NULL, 
                    Name varchar(30) NOT NULL, 
                    PRIMARY KEY (PlayerID, Name),
                    CONSTRAINT Plays_Game_Name_fk FOREIGN KEY (Name) REFERENCES Game(Name)
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    CONSTRAINT Plays_Player_PlayerID_fk FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID)
                        ON UPDATE CASCADE ON DELETE CASCADE)"""
    cursor = connection.cursor()
    cursor.execute(account_table)
    cursor.execute(game_table)
    cursor.execute(player_table)
    cursor.execute(team_table)
    cursor.execute(owns_table)
    cursor.execute(has_table)
    cursor.execute(plays_for_table)
    cursor.execute(plays_table)

except mysql.connector.Error as error:
    print("Failed to create table in MySQL: {}".format(error))
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")