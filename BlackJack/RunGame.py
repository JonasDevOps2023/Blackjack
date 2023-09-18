from PySide2 import QtCore
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QMainWindow, QMessageBox, QPushButton, QStackedLayout, QComboBox, QHBoxLayout, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QLayout, QWidget, QApplication

from TjugoEtt import Game

class MyWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.game = Game()

        self.cardOffsetCompensation = -10
        self.cardOffset = 30
        self.cardImageWidth = 500 / 8
        self.cardImageHeight = 726 / 8
        self.cardLimit = 8


        self.players = []
        self.current_player = 0
        self.nameWidth = 200
        self.nameHeight = 40


        self.initialize_UI()
        

    def initialize_UI(self):
        self.central_wid = QWidget()
        self.window_tabs = QStackedLayout()

        self.start_screen = self.create_start_screen()
        self.name_screen = self.create_name_screen()
        self.game_screen = self.create_game_screen()

        self.window_tabs.addWidget(self.start_screen)
        self.window_tabs.addWidget(self.name_screen)
        self.window_tabs.addWidget(self.game_screen)

        self.central_wid.setLayout(self.window_tabs)
        self.setCentralWidget(self.central_wid)

        
    def create_start_screen(self):
        start_screen = QWidget()
        start_screen_layout = QGridLayout()
        
        self.start_label = QLabel("Welcome! Lets begin?")

        self.btn_switch = QPushButton("Begin!")
        self.btn_switch.clicked.connect(self.switch_to_name_screen)
        self.btn_switch.setFixedSize(50,30)
        self.btn_switch

        start_screen_layout.addWidget(self.start_label, 0, 1, QtCore.Qt.AlignCenter)
        start_screen_layout.addWidget(self.btn_switch, 2, 1, QtCore.Qt.AlignCenter)

        start_screen.setLayout(start_screen_layout)

        return start_screen


    def create_name_screen(self):

        name_screen = QWidget()
        self.name_screen_layout = QGridLayout()
        self.v_box_layout = QVBoxLayout()
        self.h_box_layout = QHBoxLayout()
        self.name_screen_layout.setSizeConstraint(QLayout.SetFixedSize)

        self.current_players_label = QLabel(f"Players:")
        self.current_players_label.setWordWrap(True)

        self.name_label = QLabel(f"Player name")
        self.name_label.setFixedSize(100, 30)

        self.name_player = QLineEdit()
        self.name_player.setFixedSize(100, 30)

        self.chips_label = QLabel(f"Player chips")
        self.chips_label.setFixedSize(100, 30)

        self.chips_player = QLineEdit()
        self.chips_player.setFixedSize(100, 30)

        self.name_button_add = QPushButton("Add Player")
        self.name_button_add.clicked.connect(self.addPlayer)
        self.name_button_add.setFixedSize(100, 30)

        self.name_button_play = QPushButton("Play")
        self.name_button_play.clicked.connect(self.play)
        self.name_button_play.setFixedSize(100, 30)

        self.name_screen_layout.addWidget(self.current_players_label, 0,0, QtCore.Qt.AlignCenter, stretch=0)
        self.name_screen_layout.addWidget(self.name_label, 1, 0, QtCore.Qt.AlignCenter, stretch=0)
        self.name_screen_layout.addWidget(self.name_player, 1, 1, QtCore.Qt.AlignRight, stretch=0)
        self.name_screen_layout.addWidget(self.chips_label, 2, 0, QtCore.Qt.AlignCenter, stretch=0)
        self.name_screen_layout.addWidget(self.chips_player, 2, 1, QtCore.Qt.AlignRight, stretch=0)
        self.name_screen_layout.addWidget(self.name_button_add, 3, 0, QtCore.Qt.AlignLeft, stretch=0)
        self.name_screen_layout.addWidget(self.name_button_play, 3, 1, QtCore.Qt.AlignRight, stretch=0)
        
        name_screen.setLayout(self.name_screen_layout)
        
        return name_screen


    def create_game_screen(self):
        game_screen = QWidget()
        self.game_screen_layout = QGridLayout()
        self.game_screen_layout.setSizeConstraint(QLayout.SetFixedSize)

        self.dealer_label = QLabel(f"Dealer:" )
        self.dealer_total_label = QLabel("")
        self.dealer_bust_label = QLabel("")
        self.dealer_card_labels = [QLabel() for _ in range(self.cardLimit)]
        self.dealer_card_pixmaps = [QPixmap() for _ in range(self.cardLimit)]
        self.dealer_card_QBoxes = [QVBoxLayout() for _ in range(self.cardLimit)]

        self.game_screen_layout.addWidget(self.dealer_label, 0, 0, QtCore.Qt.AlignCenter)
        self.game_screen_layout.addWidget(self.dealer_total_label, 1, 0, QtCore.Qt.AlignCenter)
        self.game_screen_layout

        self.game_players_grid_widget = QWidget()
        self.game_players_grid_layout = QGridLayout()
        self.game_players_grid_layout.setSizeConstraint(QLayout.SetFixedSize)


        self.game_button_continue = QPushButton("Hit")
        self.game_button_continue.clicked.connect(self.hit)
        self.game_button_continue.setFixedSize(100, 30)

        self.game_button_stop = QPushButton("Stand")
        self.game_button_stop.clicked.connect(self.stand)
        self.game_button_stop.setFixedSize(100, 30)

        self.next_round_button = QPushButton("Next round")
        self.next_round_button.clicked.connect(self.nextRound)
        self.next_round_button.setVisible(False)

        self.game_screen_layout.addWidget(self.game_button_continue, 7, 0, QtCore.Qt.AlignCenter)
        self.game_screen_layout.addWidget(self.game_button_stop, 7, 1, QtCore.Qt.AlignCenter)
        self.game_screen_layout.addWidget(self.next_round_button, 8, 1, QtCore.Qt.AlignRight)
        

        game_screen.setLayout(self.game_screen_layout)
        

        return game_screen
        


    def switch_to_name_screen(self):
        self.start_screen.hide()
        self.name_screen.show()

    def switch_to_game_screen(self):
        self.name_screen.hide()
        self.game_screen.show()
        self.setupGameWidgets()
        self.updateStats()

    #def verifyChips(self, amount):


    def play(self):
        #print(f"length of self.players: {len(self.players)}")

        if len(self.name_player.text()) > 0:
            self.addPlayer()
        else:
            print("Name too short")
        if len(self.game.players) == 0:
            for player in self.players:
                self.game.addPlayer(player[0], player[1])

        self.switch_to_game_screen()
            

    
    def showHouseCards(self):
        house_cards = self.game.getHouseCards()
        for index in range(len(house_cards)):
            #print("HOUSE CARD")
            self.dealer_card_pixmaps[index].load(f"./cards/{house_cards[index][0]}.png")
            self.dealer_card_pixmaps[index] = self.dealer_card_pixmaps[index].scaled(self.cardImageWidth, self.cardImageHeight)
            self.dealer_card_labels[index].setPixmap(self.dealer_card_pixmaps[index])

    def resetHouse(self):
        for index in range(len(self.dealer_card_labels)):
            #print("HOUSE CARD")
            self.dealer_card_pixmaps[index] = QPixmap()
            self.dealer_card_labels[index].setPixmap(self.dealer_card_pixmaps[index])


    def setupGameWidgets(self):
        self.game_players_names = [QLabel(f"{name[0]}\n${name[1]}") for name in self.players]
        for nameLabel in self.game_players_names:
            nameLabel.setWordWrap(True)
        self.game_players_hands = [QLabel() for _ in range(len(self.players))]
        print(F"PLAYER PLAYER PLAYER PLAYER PLAYER {self.players}")
        self.game_players_status = [QLabel() for _ in range(len(self.players))]
        self.game_players_cards = [[QPixmap() for _ in range(self.cardLimit)] for _ in range(len(self.players))]
        self.game_players_cards_labels = [[QLabel() for _ in range(self.cardLimit)] for _ in range(len(self.players))]
        self.game_player_cards_grids_widget = [QWidget() for _ in range(len(self.players))]
        self.game_player_cards_grids_layout = [[QVBoxLayout() for _ in range(self.cardLimit)] for _ in range(len(self.players))]

        for index, (name, hand, status, cards) in enumerate(zip(self.game_players_names, self.game_players_hands, self.game_players_status, self.game_players_cards)):
            name.setFixedSize(self.nameWidth, self.nameHeight)
            hand.setFixedSize(self.nameWidth, self.nameHeight)
            status.setFixedSize(self.nameWidth, self.nameHeight)
            
            self.game_screen_layout.addWidget(name, 3, index, QtCore.Qt.AlignCenter)
            self.game_screen_layout.addWidget(hand, 4, index, QtCore.Qt.AlignCenter)
            self.game_screen_layout.addWidget(status, 5, index, QtCore.Qt.AlignCenter)


            for indexTwo in range(len(cards)):
                offset = (self.cardOffset / 2) * (indexTwo+1)
                self.game_players_cards[index][indexTwo] = QPixmap()
                
                self.game_players_cards_labels[index][indexTwo].setPixmap(self.game_players_cards[index][indexTwo])

                self.game_player_cards_grids_layout[index][indexTwo].addWidget(self.game_players_cards_labels[index][indexTwo])
                self.game_player_cards_grids_layout[index][indexTwo].setContentsMargins(self.cardOffsetCompensation + offset, self.cardOffsetCompensation + offset, 10, 10)

                self.game_screen_layout.addLayout(self.game_player_cards_grids_layout[index][indexTwo], 6, index, QtCore.Qt.AlignLeft)
        
        
        for index in range(len(self.dealer_card_labels)):
            offset = self.cardOffset * (index+1)
            self.dealer_card_labels[index].setPixmap(QPixmap())
            self.dealer_card_QBoxes[index].addWidget(self.dealer_card_labels[index])
            self.dealer_card_QBoxes[index].setContentsMargins(offset, offset, 10, 10)
            self.game_screen_layout.addLayout(self.dealer_card_QBoxes[index], 2, 0, QtCore.Qt.AlignCenter)

    def resetGameWidgets(self):
        for index, (name, hand, status, cards) in enumerate(zip(self.game_players_names, self.game_players_hands, self.game_players_status, self.game_players_cards)):
            for indexTwo in range(len(cards)):
                    offset = self.cardOffset * (indexTwo+1)
                    
                    self.game_players_cards[index][indexTwo] = QPixmap()
                    self.game_players_cards_labels[index][indexTwo].setPixmap(self.game_players_cards[index][indexTwo])


        
    def updateStats(self, house = False):

        _, hands, handsTotals, cardsShown = self.game.getPlayerStats()

        if not self.game.players[self.current_player].cardsShown == None:
            index = self.game.players[self.current_player].cardsShown - 1
            if self.game_players_cards[self.current_player][index].isNull():
                print(f"self.current_player: {self.current_player} hands: {len(hands)}")
                print(f"./cards/{hands[self.current_player][index][0]}.png")
                #self.game_players_cards[self.current_player][index] = QPixmap(f"./cards/{hands[self.current_player][index][0]}.png")

                self.game_players_cards[self.current_player][index].load(f"./cards/{hands[self.current_player][index][0]}.png")
                self.game_players_cards[self.current_player][index] = self.game_players_cards[self.current_player][index].scaled(self.cardImageWidth, self.cardImageHeight)
                self.game_players_cards_labels[self.current_player][index].setPixmap(self.game_players_cards[self.current_player][index])
                #break
                self.game_players_cards_labels[self.current_player][index].move(6, self.current_player)
        else:
            self.game.players[self.current_player].cardsShown = 0


        print(f"self.game_players_hands: {len(self.game_players_hands)}    self.current_player {self.current_player}    handsTotals: {len(handsTotals)}")
        self.game_players_names[self.current_player].setText(f"--->{self.players[self.current_player][0]}<---\n${self.players[self.current_player][1]}")
        self.game_players_hands[self.current_player].setText(str(handsTotals[self.current_player]))
        if handsTotals[self.current_player] > 21:
            self.game_players_status[self.current_player].setText('BUST')
            self.nextPlayer()

        elif handsTotals[self.current_player] == 21:
            self.nextPlayer()

                
    def updateEnd(self):
        dealer_total = self.game.getHouseTotal()
        #self.dealer_label.set
        self.dealer_total_label.setText(str(dealer_total))
        self.showHouseCards()

        
        if dealer_total > 21:
            print("DEALER BUSTED")
            self.dealer_bust_label.setText("BUST")
            
            for player in range(len(self.players)):
                if self.game.players[player].handTotal <= 21:
                    print("PLAYER WON")
                    self.game_players_status[player].setText("WON!")
        else:
            for player in range(len(self.players)):
                player_total = self.game.players[player].handTotal
                if player_total < dealer_total:
                    self.game_players_status[player].setText("LOST!")
                elif player_total == dealer_total:
                    self.game_players_status[player].setText("DRAW!")
                elif player_total <= 21:
                    self.game_players_status[player].setText("WON!")
        

    def OLDupdateEnd(self):
        self.dealer_total_label.setText(str(self.game.getHouseTotal()))
        for player in range(len(self.players)):
            if self.game.getHouseTotal() > 21:
                print("DEALER BUSTED")
                self.dealer_bust_label.setText("BUST")
                if self.game.players[player].handTotal <= 21:
                    print("PLAYER WON")
                    self.game_players_status[player].setText("WON!")
            else:
                if self.game.players[player].handTotal < self.game.getHouseTotal():
                    self.game_players_status[player].setText("LOST!")
                elif self.game.players[player].handTotal == self.game.getHouseTotal():
                    self.game_players_status[player].setText("DRAW!")
                elif self.game.players[player].handTotal > self.game.getHouseTotal() and self.game.players[player].handTotal <= 21:
                    self.game_players_status[player].setText("WON!")


    def resetHands(self):
        self.resetGameWidgets()

        
    def hit(self):

        self.game.dealNextCard()
        self.updateStats()

    def stand(self):
        self.game_players_status[self.current_player].setText("Stand")

        self.nextPlayer()

    def nextPlayer(self):
        if self.current_player + 1 == len(self.players):
            self.game_players_names[self.current_player].setText(f"{self.players[self.current_player][0]}\n${self.players[self.current_player][1]}")
            self.next_round_button.setVisible(True)
            self.game_button_continue.setVisible(False)
            self.game_button_stop.setVisible(False)
            self.game.doHouse()
            self.updateEnd()
            self.current_player = 0
            self.game_players_names[self.current_player].setText(f"--->{self.players[self.current_player][0]}<---\n${self.players[self.current_player][1]}")

        else:
            self.game_players_names[self.current_player].setText(f"{self.players[self.current_player][0]}\n${self.players[self.current_player][1]}")
            self.current_player = self.current_player+1 if (self.current_player + 1) < (len(self.players)) else 0
            self.game_players_names[self.current_player].setText(f"--->{self.players[self.current_player][0]}<---\n${self.players[self.current_player][1]}")
            self.game.nextPlayer()

    def nextRound(self):
        self.game_button_continue.setVisible(True)
        self.game_button_stop.setVisible(True)
        self.next_round_button.setVisible(False)
        for i in range(len(self.game_players_hands)):
            self.game_players_hands[i].setText("")
            self.game_players_status[i].setText("")
        self.dealer_total_label.setText("")
        self.game.nextRound()
        self.resetHands()
        #self.resetHouse()
        self.resetHouse()


    def addPlayer(self):
        validate = 0
        try:
            validate = int(self.chips_player.text())
        except:
            self.error_popup("Chips must be a integer bigger than 0")
        if validate > 0:
            self.updateAddPlayerScreen(self.name_player.text(), self.chips_player.text())
            self.players.append([self.name_player.text(), validate])
            self.name_player.setText("")
            self.chips_player.setText("")
            print(f"added player, total: {len(self.players)} players.")
        else:
            self.error_popup("Chips amount must be more than 0")

    

    def updateAddPlayerScreen(self, name, chips):
        self.current_players_label.setText(self.current_players_label.text()+f"\n {name}    $ {chips}")

    def error_popup(self, error_message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(error_message)
        error_dialog.exec_()

    def getNameAndChips(self):
        return f""



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow()
    main.resize(500, 500)
    main.show()

    sys.exit(app.exec_())

