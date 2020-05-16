import json, os
from colorama import init, Fore, Style
from random import choice, randint
from pokemon import pokemon

class game:
    def __init__(self):
        # Define Variables
        self.clear_cmd = lambda: os.system('cls')
        self.player = None
        self.enemy = None
        self.turn = "Player"

        # Get Config
        with open('config.json', 'r') as f:
            self.config = json.load(f)

    def get_input(self, text):
        response = input(text)
        return response

    def write_cmd(self, text):
        print(text)
    
    def new_line(self):
        print("")

    def pokemon_select(self):
        text = "Select a Pokémon!\n"
        count = 1
        
        # Build Text from Config
        for pok in self.config['pokemon']:
            text = text + str(count) + ". " + pok['name'] + "\n"
            count = count + 1

        self.write_cmd(text)
        input = int(self.get_input("Type the number of your desired Pokémon: "))

        # Set player
        player_stats = self.config['pokemon'][input-1]
        self.player = pokemon(player_stats['name'], player_stats['hp'], self.config['moves'])

        # Choose and set enemy
        rand = choice([i for i in range(0, count-1) if i != input-1])
        enemy_stats = self.config['pokemon'][rand]
        self.enemy = pokemon(enemy_stats['name'], player_stats['hp'], self.config['moves'])

        # Write Output
        self.clear_cmd()
        text = "You've selected " + self.player.name + "!\n"
        text = text + "Your enemy selected " + self.enemy.name + "!"
        self.write_cmd(text)
        self.new_line()

    def get_color(self, health, max_health):
        if (health/max_health) > 0.5:
            return Fore.GREEN
        elif (health/max_health) > 0.25:
            return Fore.YELLOW
        else:
            return Fore.RED

    def round(self):
        if self.turn == "Player":
            # Print Health
            text = self.player.name + "'s HP: " + self.get_color(self.player.hp, self.player.max_hp) + str(self.player.hp) + Style.RESET_ALL +"/" + str(self.player.max_hp) + "\n"
            text = text + self.enemy.name + "'s HP: " + self.get_color(self.enemy.hp, self.enemy.max_hp) + str(self.enemy.hp) + Style.RESET_ALL + "/" + str(self.enemy.max_hp)
            self.write_cmd(text)
            self.new_line()

            # Print Moves
            text = ""
            count = 1
            for mov in self.config['moves']:
                text = text + "Attack " + str(count) + ": " + str(mov['min']) + "-" + str(mov['max']) + " " + str(mov['name']) + " attack\n"
                count = count + 1
            self.write_cmd(text)
            input = int(self.get_input("Select your attack:"))
            self.clear_cmd()

            # Get move and execute
            move = self.config['moves'][input-1]['name']
            text = self.player.attack(move, self.enemy)
            self.write_cmd(text)

            # Change Turn
            self.turn = "Bot"
        else:
            # Smart ass AI
            if (self.player.hp/self.player.max_hp) < 0.25:
                move = "area"
            elif (self.enemy.hp/self.enemy.max_hp) < 0.25:
                move = "heal"
            else:
                rand = randint(0, len(self.enemy.moves)-1)
                move = self.config['moves'][rand]['name']
            text = self.enemy.attack(move, self.player)
            self.write_cmd(text)
            self.new_line()

            # Change Turn
            self.turn = "Player"

        

    def start_game(self):
        # Game Loop
        while self.player.is_alive() and self.enemy.is_alive():
            self.round()

        if self.player.is_alive():
            text = self.enemy.name + "has been defeated!\nYou win!"
        else:
            text = self.player.name + "has been defeated!\n You lose!"
        self.write_cmd(text)