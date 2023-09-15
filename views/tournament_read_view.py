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
        
        self.layout = QVBoxLayout()

        self.label = QLabel("Tournament List")
        self.layout.addWidget(self.label)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Name", "Location", "Starting date", "Ending date", "Number of rounds", "Remarks", "Action"])
        self.table.setColumnHidden(7, True) 
        # self.table.setItemDelegateForColumn(2, self.date_delegate)
        # self.table.setItemDelegateForColumn(3, self.date_delegate)   
        self.table.setItemDelegateForColumn(4, self.int_delegate)

        
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
        self.table.setItem(row_position, 5, remarks)
        self.table.setCellWidget(row_position, 6, delete_btn)
        self.table.setItem(row_position, 7, id)
        
        delete_btn.clicked.connect(partial(self.delete, row=row_position))
        
    def handle_item_changed(self, item):
        row = item.row()
        try: 
            id_item = self.table.item(row, 7) 
            tournament_id = id_item.text()
            edited_tournament = Tournament(
                id=tournament_id,
                name=self.table.item(row, 0).text(),
                location=self.table.item(row, 1).text(),
                start_date=QDateTime.fromString(self.table.item(row, 2).text(), Qt.ISODate),
                end_date=QDateTime.fromString(self.table.item(row, 3).text(), Qt.ISODate),
                num_rounds=int(self.table.item(row, 4).text()),
                remarks=self.table.item(row, 5).text()
            )
            self.tournament_controller.save_changes(edited_tournament)
        except Exception as e:
            print(f"Error fnding item: {e}")  
            
    def delete(self, row):
        print(f"row : {row}")
        id = self.table.item(row, 7).text()
        try: 
            self.tournament_controller.delete_one(id)
            self.table.removeRow(row)
        except Exception as e:
            print(f"An error occured while trying to delete the item: {e}")  
            