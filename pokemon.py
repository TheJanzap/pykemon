from move import move

class pokemon(move):
    def __init__(self, name, hp, config):
        # Set Stats
        self.name = name
        self.hp = hp
        self.max_hp = hp

        # Define moves
        self.moves = {}
        for mv in config:
            self.moves[mv["name"]] = move(mv["min"], mv["max"])

    def add_health(self, value):
        if self.hp + value < 100:
            self.hp = self.hp + value
        else:
            self.hp = 100

    def remove_health(self, value):
        self.hp = self.hp - value

    def attack(self, move, enemy):
        value = self.moves[move].get_value()
        if move != "heal":
            enemy.remove_health(value)
            text = self.name + " dealt " + str(value) + " damage to " + enemy.name + "!"
        else:
            self.add_health(value)
            text = self.name + " healed " + str(value) + " HP!"
        return text
    
    def is_alive(self):
        if self.hp <= 0:
            return False
        else:
            return True