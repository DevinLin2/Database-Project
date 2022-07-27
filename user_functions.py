from http.client import FOUND
import mysql.connector
import random

from pymysql import NULL


# code which allows a selection query of the database
def make_select(query, params):
    return_val = NULL
    try:
        # connects to locally(for now) held server and executes the query
        connection = mysql.connector.connect(host='localhost', database='matchmaking',
                                             user='root', password='Destroyer21823iw.')
        connection.cursor().execute(query, params)
        # fetches selected data
        return_val = connection.cursor().fetchall()

    except mysql.connector.Error as err:
        print("Failed to query: ".format(err))

    #closes connection to database and returns selected data
    finally:
        if connection.is_connected():
            connection.cursor().close()
            connection.close()
            return return_val


# code for queries to change existing database (insert, update, delete)
def sql_insert(query, params):
    # connects and commits according to input query
    try:
        connection = mysql.connector.connect(host='localhost', database='matchmaking',
                                             user='root', password='Destroyer21823iw.')
        connection.cursor().execute(query, params)
        connection.commit()
        connection.cursor().close()

    except mysql.connector.Error as err:
        print("Failed to query: ".format(err))

    # closes connection when done
    finally:
        if connection.is_connected():
            connection.close()


# prints and returns the information of player associated with a game and ingame name
def search_player(ign, game_name):
    query = "select * from Player where InGameID = ? and Name = ?"
    params = (ign, game_name)
    selection = make_select(query, params)
    print(selection)
    return selection


#creates a new user account, associated with this database and not a specific game
def create_account(accID, name, discAccUser, email):
    query = f"insert into Account (ACCID, Name, DiscAccUsername, Email) " \
            f"values (?, ?, ?, ?)"
    params = accID, name, discAccUser, email
    sql_insert(query, params)


#link_game adds a player(player of a specific game associated with an account)
def link_game(gameID, game_name, playstyle, elo, time_played, money_spent, is_online):
    player_profile_query = "insert into Player (InGameID, Name, Playstyle, ELO, TimePlayed, MoneySpent, isOnline) values (" \
                           "?, ?, ?, ?, ?, ?, ?)"
    params = (gameID, game_name, playstyle, elo, time_played, money_spent, is_online)
    sql_insert(player_profile_query, params)


#update_game_profile changes the information associated with a player
def update_game_profile(ign, gamename, playstyle, elo, time_played, money_spent, is_online):
    query = "update Player set Playstyle = ? and" \
            " TimePlayed = ? and MoneySpent = ? and isOnline = ?" \
            "ELO = ? where InGameID = ? and Name = ?"
    params = (playstyle, time_played, money_spent, is_online, elo, ign, gamename)
    sql_insert(query, params)


#create_team creates a new team
def create_team(team_id, captain, org_name, wins, losses, prize_money):
    team_query = "insert into Team (TeamID, Captain, Organization, Wins, Loses, PrizeMoneyEarned) values (" \
                 "?, ?, ?, ?, ?, ?)"
    params = (team_id, captain, org_name, wins, losses, prize_money)
    sql_insert(team_query, params)


# find_team prints and returns the information associated with a team
def find_team(org_name):
    query = "select * from Team where Organization = ?"
    params = org_name
    selection = make_select(query, params)
    print(selection)
    return selection


# update_team updates the information associated with a team
def update_team(team_id, captain, org_name, wins, losses, prize_money):
    query = "update Team set Captain = ? and" \
            " Organization = ? and Wins = ? and Loses = ?" \
            "PrizeMoneyEarned = ? where TeamID = ?"
    params = (captain, org_name, wins, losses, prize_money, team_id)
    sql_insert(query, params)


# join_team inserts an association between a player and a team
def join_team(game_name, player_id, team_id, role):
    join_query = "insert into Plays_For (Name, PlayerID, TeamID, Role) values (" \
                 "?, ?, ?, ?)"
    params = (game_name, player_id, team_id, role)
    sql_insert(join_query, params)


# leave_team removes the association between a specific player and a team
def leave_team(game_name, player_id, team_id):
    leave_query = "delete * from Plays_For where Name = ? and PlayerID = ? and TeamID = ?"
    params = (game_name, player_id, team_id)
    sql_insert(leave_query, params)


# check_roster prints and returns a list of all playerid's associated with a team
def check_roster(team_id):
    query = "select PlayerID from Plays_For where TeamID = ?"
    params = team_id
    roster = make_select(query, params)
    print(roster)
    return roster


# help_func displays all available functions
def help_func(funcs):
    print("Functions currently available are as follows: ", funcs.keys(), ",  end.")


# recursive function to perform quicksort on tourny draws
def quick_sort(team, elo, low, high):
    # until it's only sorting items of the same value
    if low < high:
        # re-partition into smaller subdivisions
        p = part(team, elo, low, high)
        quick_sort(team, elo, low, p - 1)
        quick_sort(team, elo, p + 1, high)
        

# other half of quicksort function to sort tourny draws
def part(team, elo, low, high):
  pivot = elo[high]
  i = low-1
  # traverse through all elements
  # move pivot down if lower
  for j in range(low, high):
    if elo[j] <= pivot:
      i = i + 1
      (team[i], team[j]) = (team[j], team[i])
      (elo[i], elo[j]) = (elo[j], elo[i])
  # move the pivot up
  (elo[i+1], elo[high]) = (elo[high], elo[i+1])
  (team[i+1], team[high]) = (team[high], team[i+1])
  return i+1


# returns number of byes appropriate for this round
# should return 0 for rounds after the first one
def number_of_byes(count):
    power_of_2 = -1
    while count >= 2^(power_of_2+1):
        power_of_2 += 1
    # return double that number, because you want each bye team
    # and the number of teams that win without a bye
    # to total to a power of 2
    return 2*(count - 2^power_of_2)


def eligible_player(p_ids, game):
    eligible_players = []
    for i in p_ids:
        if search_player(i, game)["Name"] == game:
            eligible_players.append(i)
    return eligible_players



# gives team draws given a list of available teams for the tournament
# gives byes to highest average elo teams, if available
# afterwards, pairs highest and lowest elo teams
def team_tourny_draw(available_teams_arr, game):
    #remove teams with no eligible members
    for i in available_teams_arr:
        if eligible_player(check_roster(available_teams_arr[i]), game) is NULL:
            available_teams_arr[i].pop()
            
    #take team avg elo
    team_avg_elo = []
    for i in range(len(available_teams_arr)):
        roster_size = 0
        team_elo = 0
        for player in eligible_player(check_roster(available_teams_arr[i]), game):
            roster_size += 1
            team_elo += search_player(player, game)["ELO"]
        team_avg_elo[i] = team_elo/roster_size
    #order teams by avg elo
    quick_sort(available_teams_arr, team_avg_elo, 0, len(team_avg_elo) - 1)
    # find next power of two, and give teams byes
    # such that subsequent rounds will not have byes
    bye_count = number_of_byes(len(available_teams_arr))
    # match teams, highest avg elos get byes, after that it's highest vs lowest
    byes = 0
    matchups = []
    # while there are byes, pair highest elo teams with byes
    while byes < bye_count:
        matchups.append([available_teams_arr.pop(0), 'bye'])
    # after going through byes, pair highest and lowest
    while len(available_teams_arr) < 1:
        matchups.append([available_teams_arr.pop(-1), available_teams_arr(0)])
    print(matchups)
    return matchups


def turn_string_to_list(string):
    return_list = string.strip('][').split(', ')
    for i in return_list:
        i = int(i)
    return return_list


# draws tournament seeding for singles players into semi-random teams 
# system alternates highest and lowest elo ratings until last player in team size
# at which point it picks the player which brings the team closest to the mean elo rating
# should theoretically make teams with mean elos approximating the draw mean
# approximation worse with major outliers
# creates temporary teams in teams table, then draws from those teams
# if player count doesn't divide evenly by desired_team_size, some players
# (the remainder) miss out
def singles_tourny_draw(available_players, desired_team_size, game):
    # remove ineligible players(wrong game)
    available_players = eligible_player(available_players, game)
    # will be used to seed the temporary team numbers
    tourny_team_ids_int = random.randrange(10000000, 99900000, 10000)
    draw_mean_elo = 0
    player_elo_list = []
    # grab player elos, tab up overall elos
    for player in available_players:
        player_elo = search_player(player, game)["ELO"]
        draw_mean_elo += player_elo
        player_elo_list.append(player_elo)
    # sort players by elo
    quick_sort(available_players, draw_mean_elo, 0, len(draw_mean_elo) - 1)
    # add players to teams
    teams_list = []
    for i in range((available_players)/desired_team_size):
        # creates teams in a team_id range so that they can be easily 
        # deleted after tournament
        t_id = tourny_team_ids_int + i
        team_name = f"Tournament Team {i}"
        create_team(t_id, -1, team_name, 0, 0, 0)
        tempteam = []
        team_elo = 0
        # alternating highest and lowest elo until last player in team
        # also adding up elos to help figure out the last player
        for j in range(desired_team_size-1):
            if j%2 == 0:
                tempteam.append(available_players.pop(0))
                team_elo += player_elo_list.pop(0)
                join_team(game, tempteam[j], t_id, "Tournament")
            else:
                tempteam.append(available_players.pop(available_players(-1)))
                team_elo += player_elo_list.pop(-1)
                join_team(game, tempteam[j], t_id, "Tournament")
        # last player rounds out team
        # list is already sorted, so we go through until we've either
        # parsed through the whole thing, or found the point where
        # the difference between the team's elo and the mean elo starts increasing
        # elo_goal is the elo for a final player which would make
        # the team have the same elo avg as the mean
        k = 0
        found_closest = False
        elo_goal = draw_mean_elo*desired_team_size - team_elo*(desired_team_size-1)
        while k < (len(available_players)-1) and not found_closest:
            # if we're in the sweet spot, we take that value
            if abs(team_elo[k] - elo_goal) < abs(team_elo[k+1] - elo_goal):
                found_closest = True
                k-=1
            k+=1
        available_players.pop(available_players(k))
        player_elo_list.pop(k)
        join_team(game, tempteam[j], t_id, "Tournament")
        # team is complete, now we add it to a list of teams
        teams_list.append(t_id)
    # run draw with tournament teams
    return team_tourny_draw(teams_list)



if __name__ == '__main__':
    #functions maintains a dict of all functions
    #users can see list of all keys in 'help', and can use keys to input functions
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
        "check_roster": check_roster,
        "eligible_player": eligible_player,
        "team_tourny_draw": team_tourny_draw,
        "singles_tourny_draw": singles_tourny_draw,
        "help": help_func
    }
    function_inputs = {
        "create_account": "(acc_id: int, game_name: str, disc_acc_user: str, email: str)",
        "link_game": "(gameID: int, game_name: str, playstyle: str, elo: str, time_played: str, money_spent: str, is_online: int)",
        "search_player": "(ign: str, game_name: str)",
        "update_game_profile": "(ign: str, game_name: str, playstyle: str, elo: int, time_played: int, money_spent: int, is_online: int)",
        "join_team": "(game_name: int, player_id: int, team_id: int)",
        "find_team": "(org_name: str)",
        "create_team": "(team_id: int, captain: str, org_name: str, wins: int, losses: int, prize_money: int)",
        "update_team": "(team_id: int, captain: str, org_name: str, wins: int, losses: int, prize_money: int)",
        "leave_team": "(game_name: str, player_id: int, team_id: int)",
        "check_roster": "(team_id: int)",
        "team_tourny_draw": "(available_teams_arr: List[team_id(int)], game: str)",
        "singles_tourny_draw": "(available_players: List[player_id(int)], desired_team_size: int, game: str)",
        "help": ""
    }
    user_input = ''
    # continually accepts functions until you end
    while user_input != 'end':
        user_input = input("Please type a function name, or type \'end\' to end.")
        #This if statement just stops you from getting the arguments reminder for the help function
        if user_input == 'help':
            help_func(functions)
        # after you input a desired function, it returns with a list of expected args
        elif user_input in functions:
            print("Reminder: the expected arguments for this function are: ", function_inputs[user_input])
            user_input_args = input("Please enter your arguments, each separated by a space")
            user_input_args = user_input_args.split()
            # parses out arguments from string
            for i in user_input_args:
                if i.isnumeric():
                    i = int(i)
            if user_input is "team_tourny_draw" or user_input is "singles_tourny_draw":
                user_input_args[0] = turn_string_to_list(user_input_args[0])
            functions[user_input](*user_input_args)
        elif user_input != 'end':
            print("Sorry, your function was not recognized. Please try \'help\' if you're stuck!")
