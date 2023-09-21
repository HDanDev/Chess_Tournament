from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QDialog
from PySide6.QtCore import Qt, QDate, Signal
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from models.player import Player
from views.partials.date_delegate import DateDelegate
from functools import partial

class PlayerReadView(QWidget):
    closed = Signal()
    def __init__(self, nav, tournament=""):
        super().__init__()

        self.nav = nav
        self.player_controller = PlayerController(nav)
        self.player_data = tournament.registered_players if tournament != "" else sorted(self.player_controller.get_player_data(), key=lambda x: x.last_name)
                     
        # self.date_delegate = DateDelegate(self)
        self.tournament = tournament
        self.tournament_controller = TournamentController(self.nav, self.tournament)
        self.is_tournament_related = True if tournament != "" else False                    
        
        self.layout = QVBoxLayout()

        self.label = QLabel("Player List")
        self.layout.addWidget(self.label)

        self.create_main_table()

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
        
        self.row_position = self.table.rowCount()
        self.table.insertRow(self.row_position)
        self.table.setItem(self.row_position, 0, id)
        self.table.setItem(self.row_position, 1, first_name)
        self.table.setItem(self.row_position, 2, last_name)
        self.table.setItem(self.row_position, 3, date_of_birth)
        self.table.setCellWidget(self.row_position, 4, delete_btn)
        # delete_btn.clicked.connect(partial(self.delete_in_tournament, row=self.row_position)) if self.is_tournament_related else delete_btn.clicked.connect(partial(self.delete, row=self.row_position))
        delete_btn.clicked.connect(self.delete_in_tournament) if self.is_tournament_related else delete_btn.clicked.connect(self.delete)
         
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
            
    def create_main_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Chess ID", "First name", "Last name", "Date of birth", "Action"])
        self.sort_order = [Qt.AscendingOrder] * self.table.columnCount()
        self.table.horizontalHeader().sectionClicked.connect(self.sort_rows)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.table.setItemDelegateForColumn(2, self.date_delegate)
        # self.table.setItemDelegateForColumn(3, self.date_delegate)   
        
        self.layout.addWidget(self.table)
            
    def clear_main_table(self):
        self.layout.removeWidget(self.table)
        self.table.deleteLater()
        
    def actualize_main_table(self):
        self.clear_main_table()
        self.create_main_table()
        self.populate_table() 
        
    def hide_delete_column(self):
        self.table.setColumnHidden(4, True) 
            
    def delete(self):
            sender = self.sender()
            if isinstance(sender, QPushButton):
                row = self.table.indexAt(sender.pos()).row()
                id = self.table.item(row, 0).text()
                try: 
                    self.player_controller.delete_one(id)
                    self.table.removeRow(row)
                except Exception as e:
                    print(f"An error occured while trying to delete the item: {e}")                  
                
    def delete_in_tournament(self, row):
            sender = self.sender()
            if isinstance(sender, QPushButton):
                row = self.table.indexAt(sender.pos()).row()
                id = self.table.item(row, 0).text() if self.table.item(row, 0) else None
                for player in self.tournament.registered_players:
                    try: 
                        if player.chess_id == id: 
                            self.tournament_controller.remove_player(player)
                            self.tournament_controller.save_changes(self.tournament)  
                            self.table.removeRow(row)
                    except Exception as e:
                        print(f"An error occured while trying to delete the item: {e}")                  
        
    def sort_rows(self, column):
        current_order = self.sort_order[column]
        self.sort_order[column] = Qt.DescendingOrder if current_order == Qt.AscendingOrder else Qt.AscendingOrder
        self.table.sortItems(column, current_order) 
        
    def closeEvent(self, event):
        self.closed.emit()
        event.accept()