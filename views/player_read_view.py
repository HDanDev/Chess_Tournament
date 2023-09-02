from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QDialog
from PySide6.QtCore import Qt, QDate
from controllers.player_controller import PlayerController
from models.player import Player
from views.partials.date_delegate import DateDelegate
from functools import partial

class PlayerReadView(QWidget):
    def __init__(self, nav):
        super().__init__()

        self.nav = nav
        self.player_controller = PlayerController(nav)
        self.player_data = self.player_controller.get_player_data()
        # self.date_delegate = DateDelegate(self)
        
        self.layout = QVBoxLayout()

        self.label = QLabel("Player List")
        self.layout.addWidget(self.label)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Chess ID", "First name", "Last name", "Date of birth", "Action"])
        # self.table.setItemDelegateForColumn(2, self.date_delegate)
        # self.table.setItemDelegateForColumn(3, self.date_delegate)   
        
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)
        
        self.player_controller.setup_view(self)

    def populate_table(self):
        
        for player in self.player_data:
            self.add_player_to_table(player)
            
        self.table.itemChanged.connect(self.handle_item_changed)    
       
    def add_player_to_table(self, player):
        id = QTableWidgetItem(player.chess_id)
        id.setFlags(id.flags() & ~Qt.ItemIsEnabled)

        first_name = QTableWidgetItem(player.first_name)
        last_name = QTableWidgetItem(player.last_name)

        date_of_birth = QTableWidgetItem(player.date_of_birth.toString(Qt.ISODate))
        date_of_birth.setData(Qt.DisplayRole, date_of_birth.text())
        date_of_birth.setData(Qt.EditRole, player.date_of_birth)
        
        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("delete-button")
        
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, id)
        self.table.setItem(row_position, 1, first_name)
        self.table.setItem(row_position, 2, last_name)
        self.table.setItem(row_position, 3, date_of_birth)
        self.table.setCellWidget(row_position, 4, delete_btn)
        delete_btn.clicked.connect(partial(self.delete, row=row_position))
         
    def handle_item_changed(self, item):
        row = item.row()
        try: 
            id_item = self.table.item(row, 0) 
            player_id = id_item.text()
            edited_player = Player(chess_id=player_id)
            edited_player.first_name=self.table.item(row, 1).text()
            edited_player.last_name=self.table.item(row, 2).text()
            edited_player.date_of_birth=QDate.fromString(self.table.item(row, 3).text(), Qt.ISODate)
            self.player_controller.save_changes(edited_player)
        except Exception as e:
            print(f"Error finding item: {e}")  
            
    def delete(self, row):
            print(f"row : {row}")
            id = self.table.item(row, 0).text()
            try: 
                self.player_controller.delete_one(id)
                self.table.removeRow(row)
            except Exception as e:
                print(f"An error occured while trying to delete the item: {e}")  
                