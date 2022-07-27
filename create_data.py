import csv
import names
import random
import string
import numpy as np

from user_functions import make_select

game_rows = [
    ['League of Legends', 'leagueoflegends.com', 'Riot Games', 'MOBA', 0, 117000000, 20000000000],
    ['Minecraft', 'minecraft.com', 'Mojang Studios', 'Sandbox', 27, 131000000, 200000000],
    ['Online Chess', 'Chess.com', 'Chess.com', 'Strategy', 0, 77000000, 100000000]
]
game_names = ['League of Legends', 'Minecraft', 'Online Chess']
playstyles = ['hardcore', 'casual', 'pro', 'veteran', 'newbie', 'aggressive', 'passive', 'strategic', 'coward', 'team player', 'solo', 'textbook']
organizations = ['TSM', 'C9', 'FPX', 'Samsung', 'Grandmaster', 'SKT', 'NRG', 'WillyWonka', 'USA', 'China', 'Russia']
roles = ['carry', 'strategist', 'coach', 'assistant', 'player', 'manager', 'support', 'advisor']

def random_char(char_len):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(char_len))

def generate_acct_data(ID):
    return [ID, names.get_first_name(), random_char(7), random_char(7) + "@gmail.com"]

def account_table_data(file_name, column_header, num_rows):
    with open(file_name, mode='w', newline='') as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(column_header)
        for i in range(num_rows):
            writer.writerow(generate_acct_data(i))

def game_table_data():
    with open('game.csv', mode='w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['Name', 'DownloadLink', 'DeveloperName', 'Genre', 'Cost', 'PlayerBase', 'MoneyMade'])
        writer.writerows(game_rows)

def generate_player_data(ID):
    return [ID, np.random.choice(game_names, size=1)[0], np.random.choice(playstyles, size=1)[0], random.randint(0, 500), random.randint(100, 1500), random.randint(0, 2000), random.randint(0,1)]

def generate_has_table_data():
    with open('has.csv', mode='w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['Name', 'TeamID'])
        for i in range(50):
            writer.writerow([np.random.choice(game_names, size=1)[0], i])

def player_table_data(num_rows):
    with open('player.csv', mode='w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['PlayerID', 'GameName', 'Playstyle', 'ELO', 'TimePlayed', 'MoneySpent', 'isOnline'])
        for i in range (num_rows):
            writer.writerow(generate_player_data(i))

def owns_table_data():
    with open('owns.csv', mode='w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['GameName', 'PlayerID', 'AccID'])
        with open('player.csv') as player:
            player_reader = csv.reader(player, delimiter=',')
            line_count = 0
            for row in player_reader:
                if line_count > 0:
                    writer.writerow([row[1], row[0], row[0]]) #this is hard coded
                line_count += 1

def generate_team_data(ID):
    name = open('player.csv').read().splitlines()
    # print(name)
    wins = random.randint(0, 60)
    return [ID, (np.random.choice(name, size=1)[0]).split(",")[0], np.random.choice(organizations, size=1)[0], wins, 60 - wins, 5000 * wins]

def team_table_data(num_rows):
    with open('team.csv', mode='w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['TeamID', 'Captain', 'Organization', 'Wins', 'Loses', 'PrizeMoneyEarned'])
        for i in range(num_rows):
            writer.writerow(generate_team_data(i))

def plays_for_table_data():
    with open('playsfor.csv', mode='w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['Gamename', 'PlayerID', 'TeamID', 'Role'])
        with open('player.csv') as player:
            player_reader = csv.reader(player, delimiter=',')
            line_count = 0
            for row in player_reader:
                if line_count > 0 and random.randint(0, 2) == 0:
                    writer.writerow([row[1], row[0], random.randint(0, 50), np.random.choice(roles, size=1)[0]])
                line_count += 1

account_table_data('account.csv', ['AccID','Name', 'DiscAccUsername', 'Email'], 1500)
game_table_data()
player_table_data(1500)
owns_table_data()
team_table_data(50)
plays_for_table_data()
generate_has_table_data()