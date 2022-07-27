import csv
import names
import random
import string

from user_functions import make_select

game_rows = [
    ['League of Legends', 'leagueoflegends.com', 'Riot Games', 'MOBA', 0, 117000000, 20000000000],
    ['Minecraft', 'minecraft.com', 'Mojang Studios', 'Sandbox', 27, 131000000, 200000000],
    ['Online Chess', 'Chess.com', 'Chess.com', 'Strategy', 0, 77000000, 100000000]
]
game_names = ['League of Legends', 'Minecraft', 'Online Chess']

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
    return [ID, ]

def generate_has_table_data():
    query = f"select TeamID from Team"
    t_ids = make_select(query) 
    with open('has.csv', mode='w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow('Name', 'TeamID')
        for i in t_ids:
            writer.writerow(random.sample(game_names), i)

def player_table_data(num_rows):
    with open('player.csv', mode='w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['PlayerID', 'GameName', 'Playstyle', 'ELO', 'TimePlayed', 'MoneySpent', 'isOnline'])
        for i in range (num_rows):
            writer.writerow(generate_player_data(i))

account_table_data('account.csv', ['AccID','Name', 'DiscAccUsername', 'Email'], 1500)
game_table_data()