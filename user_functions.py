import mysql.connector
import inspect


def make_select(query):
    try:
        connection = mysql.connector.connect(host='localhost', database='matchmaking',
                                             user='root', password='Destroyer21823iw.')
        connection.cursor().execute(query)
        return_val = connection.cursor().fetchall()

    except mysql.connector.Error as err:
        print("Failed to query: ".format(err))

    finally:
        if connection.is_connected():
            connection.cursor().close()
            connection.close()
            print("Connection closed")
            return return_val


def sql_insert(query):
    try:
        connection = mysql.connector.connect(host='localhost', database='matchmaking',
                                             user='root', password='Destroyer21823iw.')
        connection.cursor().execute(query)
        connection.commit()
        print("Insertion committed.")
        connection.cursor().close()

    except mysql.connector.Error as err:
        print("Failed to query: ".format(err))

    finally:
        if connection.is_connected():
            connection.close()
            print("Connection closed")


def search_player(ign):
    query = f"select * from player_table where InGameID = {ign}"
    selection = make_select(query)
    print(selection)
    return selection


def create_account(accID, name, discAccUser, email):
    query = f"insert into account_table (ACCID, Name, DiscAccUsername, Email) " \
            f"values ({accID}, {name}, {discAccUser}, {email})"
    sql_insert(query)


def link_game(gameID, game_name, playstyle, elo, time_played, money_spent, is_online):
    game_name_query = make_select(f"select name from game_table where name = {game_name}")
    player_profile_query = f"insert into player_table (InGameID, Name, Playstyle, ELO, TimePlayed, MoneySpent, isOnline) values (" \
                           f"{gameID}, {game_name_query}, {playstyle}, {elo}, {time_played}, {money_spent}, {is_online})"
    sql_insert(player_profile_query)


def update_game_profile(ign, gamename, playstyle, elo, time_played, money_spent, is_online):
    query = f"update player_table set Playstyle = {playstyle} and" \
            f" TimePlayed = {time_played} and MoneySpent = {money_spent} and isOnline = {is_online}" \
            f"ELO = {elo} where InGameID = {ign} and Name = {gamename}"
    sql_insert(query)


def create_team(team_id, captain, org_name, wins, losses, prize_money):
    team_query = f"insert into team_table (TeamID, Captain, Organization, Wins, Loses, PrizeMoneyEarned) values (" \
                 f"{team_id}, {captain}, {org_name}, {wins}, {losses}, {prize_money})"
    sql_insert(team_query)


def find_team(org_name):
    query = f"select * from team_table where Organization = {org_name}"
    selection = make_select(query)
    print(selection)
    return selection


def update_team(team_id, captain, org_name, wins, losses, prize_money):
    query = f"update team_table set  Captain = {captain} and" \
            f" Organization = {org_name} and Wins = {wins} and Loses = {losses}" \
            f"PrizeMoneyEarned = {prize_money} where TeamID = {team_id}"
    sql_insert(query)


def join_team(game_name, player_id, team_id, role):
    join_query = f"insert into plays_for_table (Name, PlayerID, TeamID, Role) values (" \
                 f"{game_name}, {player_id}, {team_id}, {role})"
    sql_insert(join_query)


def leave_team(game_name, player_id, team_id):
    leave_query = f"delete * from plays_for_table where Name = {game_name} and PlayerID = {player_id} and TeamID = {team_id}"
    sql_insert(leave_query)


def help_func(funcs):
    print("Functions currently available are as follows: ", funcs.keys(), ",  end.")


if __name__ == '__main__':
    functions = {
        "create_account": create_account,
        "link_game": link_game,
        "search_player": search_player,
        "update_game_profile": update_game_profile,
        "join_team": join_team,
        "find_team": find_team,
        "create_team": create_team,
        "update_team": update_team,
        "leave_team": leave_team,
        "help": help_func
    }
    user_input = ''
    while user_input != 'end':
        user_input = input("Please type a function name, or type \'end\' to end.")
        if user_input == 'help':
            help_func(functions)
        elif user_input in functions:
            print("Reminder: the expected arguments for this function are: ", inspect.getfullargspec(user_input))
            user_input_args = input("Please enter your arguments.")
            functions[user_input](user_input_args)
        elif user_input != 'end':
            print("Sorry, your function was not recognized. Please try \'help\' if you're stuck!")
