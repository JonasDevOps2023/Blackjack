import csv

class Player():
	def __init__(self, name, chips=0, house = False):
		self.name = name
		self.wallet = 0
		self.hand = []
		self.handTotal = 0
		self.house = house
		self.cardsShown = None

		self.deposit(chips)

	def bet(self, amount):
		try:
			amount = int(amount)
		except:
			print("Betting amount has to be an integer")
		
		if self.wallet > amount:
			self.wallet - amount
			return True
		else:
			print("Insufficient founds")
			return False


	def deposit(self, amount):
		if not self.house:
			try:
				if amount > 0:
					self.wallet += int(amount)
				else:
					print("Can not deposit a negative amount!")
			except:
				print("This requires numeric input.")
		else:
			try:
				with open("dealer.csv", newline='') as f:
					reader = csv.DictReader(f)
					self.wallet = int(reader[0]['wallet'])
					print(self.wallet)
			except:
				with open("dealer.csv", 'w', newline='') as f:
					fieldnames = ['name', "wallet"]

					writer = csv.DictWriter(f, fieldnames=fieldnames)

					writer.writeheader()
					writer.writerow({'name': "Dealer", 'wallet': 1000})
					self.wallet = 10000


	def recieveCard(self, Card, house = False):
		# card = [Name of card, Value of card]
		self.hand.append(Card)
		#print(f"self.hand len: {len(self.hand)}")

		if not house:
			self.handTotal = self.calculate_hand_value(self.hand)
		else:
			self.handTotal, state = self.calculate_hand_value_house(self.hand)
			return state

		#if not self.isAce(card):
		#	self.handTotal += card[1]
		print(f"Current hand: {self.hand} : {self.handTotal}")
		try:
			self.cardsShown += 1
		except:
			self.cardsShown = 1


	def calculate_hand_value(self, hand):
		# Initialize the total value and the count of 'ace' cards
		total_value = 0
		ace_count = 0

	    # Iterate through the cards in the hand
		for card in hand:
			if card[1] == 'ace':
				ace_count += 1
			else:
				total_value += card[1]

	    # Add the maximum possible value for 'ace' cards (14) while staying below 21
		while ace_count > 0 and total_value + 14 <= 21:
			total_value += 14
			ace_count -= 1

	    # Add the remaining 'ace' cards as 1
		total_value += ace_count

		return total_value


	def isAce(self, card):
		if card[1] == "ace":
			#print(f"DEBUG WHY LOSE ACE {self.handTotal}")
			if self.handTotal + 14 > 21:
				self.handTotal += 1
			else:
				self.handTotal += 14
			return True
		else:
			return False


	def resetHand(self):
		self.hand = []
		self.handTotal = 0
		self.cardsShown = 0

	#def houseTurn(self):

	def getCard(self):
		send = self.cardsShown
		self.cardsShown += 1
		return send

	def getCardsShown(self):
		return self.cardsShown


	def calculate_hand_value_house(self, hand):
	    # Initialize the total value and the count of 'ace' cards
		total_value = 0
		ace_count = 0

	    # Iterate through the cards in the hand
		for card in hand:
			if card[1] == 'ace':
				ace_count += 1
			else:
				total_value += card[1]

	    # Add the maximum possible value for 'ace' cards (14) while staying below 21
		while ace_count > 0 and total_value + 14 <= 21:
			total_value += 14
			ace_count -= 1

	    # If adding 14 would make the hand 17 or higher without busting, treat remaining 'ace' cards as 1
		while ace_count > 0 and total_value + 1 <= 17:
			total_value += 1
			ace_count -= 1

	    # Add the remaining 'ace' cards as 1
		total_value += ace_count
		if total_value >= 17:
			return total_value, False
			print("Inside")
		print("Outside")
		return total_value, True



