from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QDialog
from PySide6.QtCore import Qt, QDateTime
from controllers.tournament_controller import TournamentController
from models.tournament import Tournament
from views.partials.date_delegate import DateDelegate
from views.partials.int_delegate import IntDelegate
from functools import partial

class TournamentReadView(QWidget):
    def __init__(self, nav):
        super().__init__()

        self.nav = nav
        self.tournament_controller = TournamentController(nav)
        self.tournament_data = self.tournament_controller.get_tournament_data()
        # self.tournament = Tournament()
        self.date_delegate = DateDelegate(self)
        self.int_delegate = IntDelegate(self)
        self.id_column = 9
        
        self.layout = QVBoxLayout()

        self.label = QLabel("Tournament List")
        self.layout.addWidget(self.label)

        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(["Name", "Location", "Starting date", "Ending date", "Number of rounds", "Current round", "Registered players", "Remarks", "Action"])
        self.table.setColumnHidden(self.id_column, True) 
        # self.table.setItemDelegateForColumn(2, self.date_delegate)
        # self.table.setItemDelegateForColumn(3, self.date_delegate)   
        self.table.setItemDelegateForColumn(4, self.int_delegate)
        
        self.sort_order = [Qt.AscendingOrder] * self.table.columnCount()
        self.table.horizontalHeader().sectionClicked.connect(self.sort_rows)

        
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)
        
        self.tournament_controller.setup_view(self)

    def populate_table(self):
        
        for tournament in self.tournament_data:
            self.add_tournament_to_table(tournament)
            
        self.table.itemChanged.connect(self.handle_item_changed)    
       
    def add_tournament_to_table(self, tournament):
        id = QTableWidgetItem(tournament.id)
        id.setFlags(id.flags() & ~Qt.ItemIsEnabled)

        name = QTableWidgetItem(tournament.name)
        location = QTableWidgetItem(tournament.location)

        start_date = QTableWidgetItem(tournament.start_date.toString(Qt.ISODate))
        start_date.setData(Qt.DisplayRole, start_date.text())
        start_date.setData(Qt.EditRole, tournament.start_date)

        end_date = QTableWidgetItem(tournament.end_date.toString(Qt.ISODate))
        end_date.setData(Qt.DisplayRole, end_date.text())
        end_date.setData(Qt.EditRole, tournament.end_date)

        num_rounds = QTableWidgetItem(str(tournament._num_rounds))
        num_rounds.setData(Qt.EditRole, int(tournament._num_rounds))
        
        current_round = QTableWidgetItem(str(tournament._current_round))
        current_round.setFlags(current_round.flags() & ~Qt.ItemIsEditable)
        
        total_registered_players = QTableWidgetItem(str(tournament._total_registered_players))
        total_registered_players.setFlags(total_registered_players.flags() & ~Qt.ItemIsEditable)
        
        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("delete-button")

        remarks = QTableWidgetItem(tournament.remarks)
                
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, name)
        self.table.setItem(row_position, 1, location)
        self.table.setItem(row_position, 2, start_date)
        self.table.setItem(row_position, 3, end_date)
        self.table.setItem(row_position, 4, num_rounds)
        self.table.setItem(row_position, 5, current_round)
        self.table.setItem(row_position, 6, total_registered_players)
        self.table.setItem(row_position, 7, remarks)
        self.table.setCellWidget(row_position, 8, delete_btn)
        self.table.setItem(row_position, self.id_column, id)
        
        delete_btn.clicked.connect(partial(self.delete, row=row_position))
        
    def handle_item_changed(self, item):
        row = item.row()
        try: 
            id_item = self.table.item(row, self.id_column) 
            tournament_id = id_item.text()
            edited_tournament = self.tournament_controller.tournament_repository.find_one_by_id(tournament_id)
            edited_tournament.id=tournament_id
            edited_tournament.name=self.table.item(row, 0).text()
            edited_tournament.location=self.table.item(row, 1).text()
            edited_tournament.start_date=QDateTime.fromString(self.table.item(row, 2).text(), Qt.ISODate)
            edited_tournament.end_date=QDateTime.fromString(self.table.item(row, 3).text(), Qt.ISODate)
            edited_tournament.num_rounds=int(self.table.item(row, 4).text())
            edited_tournament.remarks=self.table.item(row, 6).text()
                
            self.tournament_controller.save_changes(edited_tournament)
        except Exception as e:
            print(f"Error fnding item: {e}")  
            
    def delete(self, row):
        id = self.table.item(row, self.id_column).text()
        try: 
            self.tournament_controller.delete_one(id)
            self.table.removeRow(row)
        except Exception as e:
            print(f"An error occured while trying to delete the item: {e}")              
            
    def sort_rows(self, column):
        current_order = self.sort_order[column]
        self.sort_order[column] = Qt.DescendingOrder if current_order == Qt.AscendingOrder else Qt.AscendingOrder
        self.table.sortItems(column, current_order)