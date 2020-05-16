import random, os, time
from colorama import init
from colorama import Fore
from colorama import Style

class Pokemon:
	def __init__(self):
		self.name = None
		self.hp = self.maxHp = int(0)
		self.tmpMove = Moves()
		self.moves = []

	def selectPokemon(self, name):
		self.name = name
		self.hp = self.maxHp = 100
		for moveType in ["close", "area", "heal"]:
			self.tmpMove.getMoves(moveType)
			self.moves.append(self.tmpMove)
			self.tmpMove = Moves()

class Moves:
	def __init__(self):
		self.min = int(0)
		self.max = int(0)
		self.attackType = str(None)

	def setAttackValues(self, min, max):
		self.min = min
		self.max = max

	def getMoves(self, attackType):
		self.attackType = attackType
		switch={
			"close": [17, 26],
			"area": [10, 34],
			"heal": [15, 27]
		}
		self.setAttackValues(*switch.get(attackType))

def printHP():
	for obj in [player, enemy]:
		if (obj.hp / obj.maxHp) > 0.5:
			textColor = "GREEN"
		elif (obj.hp / obj.maxHp) > 0.25:
			textColor = "YELLOW"
		else:
			textColor = "RED"

		changeColor = getattr(Fore, textColor)
		print(obj.name + f"s HP: {changeColor}"  + str(obj.hp) + f"{Style.RESET_ALL}/100" + "\n")
	
def selectAttack():
	printHP()
	i = 1
	for move in player.moves:
		if move.attackType == "heal":
			attackTypeText = " Healing "
		else:
			attackTypeText = " Damage "
		print("Attack " + str(i) + ": " + str(move.min) + "-" + str(move.max) + attackTypeText + "(" + move.attackType + " attack)")
		i += 1

	return eval(input("Select your Attack: "))

def execAttack(attackNum):
	if turnPlayer == True:
		attacker = player
		victim = enemy
	else:
		attacker = enemy
		victim = player

	attackDmg = random.randint(attacker.moves[attackNum - 1].min, attacker.moves[attackNum - 1].max)
	if attacker.moves[attackNum - 1].attackType == "heal":
		if attacker.hp + attackDmg > 100:
			attacker.hp = 100
			print("\n" + attacker.name + " fully healed themselves!")
		else:
			attacker.hp += attackDmg
			print("\n" + attacker.name + " healed " + str(attackDmg) + " HP!")
	else:
		victim.hp -= attackDmg
		print(attacker.name + " dealt " + str(attackDmg) + " damage to " + victim.name + "!" + "\n")

#Hah, yeah as if I knew how to build a proper AI. These are mainly condition checks I thought made sense.
def ai():
	#Deliver "killing blow" to player. Has to be first, otherwise only heals himself
	if (player.hp / player.maxHp) < 0.25:
		return 2
	#Healing when HP drops below 25%
	elif (enemy.hp / enemy.maxHp) < 0.25:
		return 2
	#Choose random attack, default behaviour
	else:
		return random.randint(1, 2)

init()

clear = lambda: os.system('cls')
clear()

print("Select a Pokémon!\n1. Eevee\n2. Jigglypuff")
selectedPokemon = eval(input("Type the number of your desired Pokémon: "))

player = Pokemon()
enemy = Pokemon()

clear()

if selectedPokemon == 1:
	print("You've selected Evee!")
	player.selectPokemon("Eevee")
	enemy.selectPokemon("Jigglypuff")
	print("\nYour enemy selected Jigglypuff!")

if selectedPokemon == 2:
	print("You've selected Jigglypuff!")
	player.selectPokemon("Jigglypuff")
	enemy.selectPokemon("Eevee")
	print("\nYour enemy selected Eevee!")


turnPlayer = True

while player.hp > 0 and enemy.hp > 0:
	if turnPlayer == True:
		attack = selectAttack()
		clear()
		execAttack(attack)
		turnPlayer = False
	else:
		attack = ai()
		execAttack(attack)
		turnPlayer = True

if player.hp <= 0:
	print(player.name + " has been defeated!\nYou lose!")
else:
	print(enemy.name + " has been defeated!\nYou win!")
input("Press Enter to end the program...")