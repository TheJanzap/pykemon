import random
import os
from colorama import init, Fore, Style


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
			# Creates a temp move, adds it the moves list and creates a new tmpMove
			self.tmpMove.getMoves(moveType)
			self.moves.append(self.tmpMove)
			self.tmpMove = Moves()

	def execAttack(self, attackNum, victim):
		# Set random value between the min/max values of the chosen attack
		attackDmg = random.randint(
			self.moves[attackNum - 1].min, self.moves[attackNum - 1].max)
			
		if self.moves[attackNum - 1].attackType == "heal":
			# Ensures that healing will never heal more than maxHp
			if self.hp + attackDmg > self.maxHp:
				self.hp = self.maxHp
				print(self.name + " fully healed themselves!")
			else:
				self.hp += attackDmg
				print(self.name + " healed " + str(attackDmg) + " HP!")
		else:
			# Regular damage attack
			victim.hp -= attackDmg
			print(self.name + " dealt " + str(attackDmg) +
				  " damage to " + victim.name + "!")


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
		switch = {
			"close": [17, 26],
			"area": [10, 34],
			"heal": [15, 27]
		}
		self.setAttackValues(*switch.get(attackType))


def initGame():
	#Necessary to get colorama working in Windows
	init()

	#Clears screen
	def clear(): return os.system('cls' if os.name == 'nt' else 'clear')
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
		print("Your enemy selected Jigglypuff!")

	if selectedPokemon == 2:
		print("You've selected Jigglypuff!")
		player.selectPokemon("Jigglypuff")
		enemy.selectPokemon("Eevee")
		print("Your enemy selected Eevee!")

	turnPlayer = True

	return player, enemy, turnPlayer, clear



def printHP():
	print("")
	for obj in [player, enemy]:
		if (obj.hp / obj.maxHp) > 0.5:
			textColor = "GREEN"
		elif (obj.hp / obj.maxHp) > 0.25:
			textColor = "YELLOW"
		else:
			textColor = "RED"

		changeColor = getattr(Fore, textColor)
		print(obj.name + f"s HP: {changeColor}" +
			  str(obj.hp) + f"{Style.RESET_ALL}/100")


def selectAttack():
	printHP()
	print("")
	i = 1
	for move in player.moves:
		if move.attackType == "heal":
			attackBehaviourText = " Healing "
		else:
			attackBehaviourText = " Damage "
		print("Attack " + str(i) + ": " + str(move.min) + "-" +
			  str(move.max) + attackBehaviourText + "(" + move.attackType + " attack)")
		i += 1

	return eval(input("Select your Attack: "))


def ai():
	# Hah, yeah as if I knew how to build a proper AI. These are mainly condition checks I thought made sense.
	# Deliver "killing blow" to player. Has to be first, otherwise only heals himself
	if (player.hp / player.maxHp) < 0.25:
		return 2
	# Healing when HP drops below 25%
	elif (enemy.hp / enemy.maxHp) < 0.25:
		return 2
	# Choose random attack, default behaviour
	else:
		return random.randint(1, 2)


if __name__ == "__main__":

	player, enemy, turnPlayer, clear = initGame()

	# Win/Lose condition check
	while player.hp > 0 and enemy.hp > 0:
		if turnPlayer == True:
			attack = selectAttack()
			clear()
			player.execAttack(attack, enemy)
			turnPlayer = False
		else:
			attack = ai()
			enemy.execAttack(attack, player)
			turnPlayer = True

	if player.hp <= 0:
		print(player.name + " has been defeated!\nYou lose!")
	else:
		print(enemy.name + " has been defeated!\nYou win!")
	input("\nPress Enter to end the program...")
