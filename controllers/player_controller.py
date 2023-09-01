from PySide6.QtWidgets import QTableWidgetItem, QHeaderView
from PySide6.QtCore import QDateTime 
from repositories.player_repository import PlayerRepository
from models.player import Player
from datetime import datetime

class PlayerController:
    
    def __init__(self, nav, player_data={}):
        self.nav = nav
        self.player_data = player_data
        self.data_repository = PlayerRepository()
        self.player_model = Player
        
    def setup_view(self, view):
        self.view = view
        self.view.populate_table()
        self.view.table.horizontalHeader().setStretchLastSection(True)
        self.view.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def get_player_data(self):
        return self.data_repository.read_json()

    def save_changes(self, player):
        self.data_repository.update_json(player)
        
    def save_new_item(self, player):
        self.data_repository.add_json(player)
            
    # def add_player(self, player):
    #     try:
    #         self.registered_players.append(player)
    #     except Exception as e:
    #         print(f"Error adding player: {e}")