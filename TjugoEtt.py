from random import shuffle
from player import Player

class Game:
	def __init__(self):
		self.players = []
		self.house = None
		self.hands = 0
		self.deck = []

		self.currentPlayer = 0

		self.deckIndex = 0
		
		self.createDeck()
		self.shuffleDeck()
		self.makeHouse()


	def makeHouse(self):
		self.house = Player("Dealer", house = True)

	def addPlayer(self, name, chips):
		try:
			self.players.append(Player(name, chips=chips))
		except:
			pass

		#return Player(name)

	def createDeck(self):
		if len(self.deck) > 0:
			self.deck = []
		suits = ["spades", "clubs", "diamonds", "hearts"]
		ranks = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
		values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

		#ranks = ["Ace", "Ace", "Ace", "Ace", "Ace", "Ace", "Ace", "Ace", "Ace", "Ace", "Ace", "Ace", "Ace"]
		#values = ["Ace", "Ace", "Ace", "Ace", "Ace", "Ace", "Ace", "Ace", "Ace", "Ace", "Ace", "Ace"]
		for suit in suits:
			point = 0
			for rank in ranks:
				name = f"{rank}_of_{suit}"
				if rank == "ace":
					points = "ace"
				else:
					points = values[point]
					point += 1
				self.deck.append([name, points])
		print(self.deck[0])

	def shuffleDeck(self):
		shuffle(self.deck)


	def dealNextCard(self, house = False,):

		if not house:
			self.players[self.currentPlayer].recieveCard(self.deck[0])
			del self.deck[0]
		else:
			state = self.house.recieveCard(self.deck[0], house = True)
			del self.deck[0]
			return state


	def getHouseTotal(self):
		return self.house.handTotal

	def getHouseCards(self):
		return self.house.hand


	def nextPlayer(self):
		#print("NEXT PLAYER")
		self.currentPlayer = self.currentPlayer+1 if (self.currentPlayer + 1) < (len(self.players)) else 0
		#if self.currentPlayer == 0:
		#	DoHouse()

	def printHands(self):
		for player in self.players:
			print(f"{player.name} has Cards: {player.hand}, and that is {player.handTotal}")

	def getCurrentPlayer(self):
		return self.currentPlayer

	def getCurrentPlayerStats(self):
		return self.players[self.currentPlayer].hand, self.players[self.currentPlayer].handTotal

	def getPlayerStats(self):
		names = []
		hands = []
		handTotals = []
		#print(len(self.players))
		for player in self.players: 
			#print(player.handTotal)
			names.append(player.name)
			hands.append(player.hand)
			handTotals.append(player.handTotal)
		return names, hands, handTotals, player.getCardsShown()

	def doHouse(self):
		state = True
		while state:
			state = self.dealNextCard(house = True)

	def nextRound(self):
		self.house.resetHand()
		for player in self.players:
			player.resetHand()
		self.currentPlayer = 0