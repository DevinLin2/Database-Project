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
    return make_select(query)


def create_account(accID, name, discAccUser, email):
    query = f"insert into account_table (ACCID, Name, DiscAccUsername, Email) " \
            f"values ({accID}, {name}, {discAccUser}, {email})"
    sql_insert(query)


def link_game(gameID, game_name, playstyle, elo):
    game_name_query = make_select(f"select name from game_table where name = {game_name}")
    player_profile_query = f"insert into player_table (InGameID, Name, Playstyle, ELO) values (" \
                           f"{gameID}, {game_name_query}, {playstyle}, {elo})"
    sql_insert(player_profile_query)
    query = f"insert into plays_table (Name, InGameID) values({game_name_query}, {gameID})"
    sql_insert(query)


def edit_game_profile(ign, gamename, playstyle, elo):
    query = f"update player_table set Playstyle = {playstyle} and " \
            f"ELO = {elo} where InGameID = {ign} and Name = {gamename}"
    sql_insert(query)


def help_func(funcs):
    print("Functions currently available are as follows: ", funcs.keys(), ",  end.")


if __name__ == '__main__':
    functions = {
        "help": help_func,
        "search_player": search_player,
        "create_account": create_account,
        "link_game": link_game,
        "edit_game_profile": edit_game_profile
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
