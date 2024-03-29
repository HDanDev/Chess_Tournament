from PySide6.QtCore import QDateTime
from repositories.tournament_repository import TournamentRepository
from models.match import MatchResult
from models.match import Match
from controllers.player_controller import PlayerController
from models.round import Round
from models.tournament import Tournament
import random


class TournamentController:
    def __init__(self, nav, tournament={}):
        self.nav = nav
        self.tournament = tournament
        self.player_controller = PlayerController(self.nav)
        self.tournament_repository = TournamentRepository()
        self.tournament_model = Tournament

    def setup_view(self, view):
        self.view = view
        self.view.populate_table()
        # self.view.table.horizontalHeader().setStretchLastSection(True)
        # self.view.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def get_tournament_data(self):
        return self.tournament_repository.read_json()

    def save_changes(self, tournament):
        self.tournament_repository.update_json(tournament)

    def save_new_item(self, tournament):
        self.tournament_repository.add_json(tournament)

    def delete_one(self, id):
        self.tournament_repository.delete_json(id)

    def add_player(self, player):
        try:
            self.tournament.add_player(player)
        except Exception as e:
            print(f"Error adding player: {e}")

    def remove_player(self, player):
        try:
            self.tournament.remove_player(player)
        except Exception as e:
            print(f"Error removing player: {e}")

    def clear_registered_players(self):
        self.tournament.registered_players.clear()

    def generate_pairs(self, is_simulation=False, current_round=1):
        try:
            self.tournament.current_round = current_round

            new_round = Round()
            new_round.name = f"Round {self.tournament.current_round}"
            new_round.start_datetime = QDateTime.currentDateTime()

            if self.tournament.current_round == 1:
                random.shuffle(self.tournament.registered_players)
                sorted_players = self.tournament.registered_players

            else:
                sorted_players = self.sort_players_by_scores()
                # sorted_players = sorted(
                # self.tournament.registered_players,
                # key=lambda player: player[1], reverse=True
                # )

            already_paired_players = []

            for player in sorted_players:
                if player.chess_id not in already_paired_players:
                    new_match = Match()
                    new_match.player1 = player
                    new_match.player2 = self.find_player_with_least_fought_opponent(
                        player, sorted_players, already_paired_players
                        )
                    new_round.add_match(new_match)
                    already_paired_players += [new_match.player1.chess_id, new_match.player2.chess_id]

            # for i in range(0, len(sorted_players), 2):
            #     if i + 1 < len(sorted_players):
            #         new_match = Match()
            #         new_match.player1 = sorted_players[i]
            #         new_match.player2 = sorted_players[i + 1]
            #         new_round.add_match(new_match)

            self.tournament.add_round(new_round)

            if is_simulation:
                self.generate_random_results(new_round)

        except Exception as e:
            print(f"Error generating pairs: {e}")

    def update_matches_results(self, round, results_list):
        for i, match in enumerate(round.matches):
            match.result = results_list[i]
            print(
                f"Outcome of {match.get_match_name()}: "
                f"{match.result} / "
                f"{match.score[0][0].get_full_name()} "
                f"has now: {match.score[0][1]} points, "
                f"and {match.score[1][0].get_full_name()}: "
                f"{match.score[1][1]} points"
            )
            self.tournament.update_player_score(
                match.score[0][0],
                match.score[0][1]
                )
            self.tournament.update_player_score(
                match.score[1][0],
                match.score[1][1]
                )
            self.player_controller.save_changes(
                match.score[0][0]
                )
            self.player_controller.save_changes(
                match.score[1][0]
                )

    def get_opponents_count(self, player):
        opponents_count = {}
        for round in self.tournament.rounds:
            for match in round.matches:
                if player == match.player1:
                    opponent = match.player2
                elif player == match.player2:
                    opponent = match.player1
                else:
                    continue

                if opponent in opponents_count:
                    opponents_count[opponent] += 1
                else:
                    opponents_count[opponent] = 1

        print(opponents_count)

        return opponents_count

    def find_player_with_least_fought_opponent(
            self, player, players, excluded_players
            ):
        opponents_count = self.get_opponents_count(player)
        valid_opponents = [
            opponent for opponent in players if opponent.chess_id != player.chess_id
            and opponent.chess_id not in excluded_players
            ]
        least_fought_opponent = min(valid_opponents, key=lambda x: opponents_count.get(x, 0), default=None)

        return least_fought_opponent

    def modify_matches_results(self, match, score_1, score_2):
        match.player1.update_points(self.tournament.id, score_1)
        match.player2.update_points(self.tournament.id, score_2)
        self.player_controller.save_changes(match.player1)
        self.player_controller.save_changes(match.player2)
        print("ok")

    def generate_random_results(self, round):
        outcome = list(MatchResult)
        for match in round.matches:
            random_result = random.choice(outcome)
            match.result = random_result
            print(
                f"Outcome of {match.get_match_name()}: "
                f"{match.result} / player one has now: "
                f"{match.score[0][1]} points, and player 2: "
                f"{match.score[1][1]} points"
            )
            self.tournament.update_player_score(
                match.score[0][0],
                match.score[0][1]
                )
            self.tournament.update_player_score(
                match.score[1][0],
                match.score[1][1]
                )
            self.player_controller.save_changes(
                match.score[0][0]
                )
            self.player_controller.save_changes(
                match.score[1][0]
                )
        self.set_round_end_date(round, False)
        self.save_changes(self.tournament)

    def sort_players_by_scores(self):
        return sorted(
            self.tournament.registered_players,
            key=lambda player: player.get_points(self.tournament.id),
            reverse=True,
        )

    def check_is_player_already_selected(
            self,
            tournament_players,
            all_players,
            id
    ):
        tournament_players_ids = set(
            player.chess_id for player in tournament_players
            )
        all_players_ids = set(player.chess_id for player in all_players)

        return id in tournament_players_ids and id in all_players_ids

    def set_round_start_date(self, round, date):
        round.start_datetime = date

    def set_round_end_date(self, round, hasChangedDate, date=""):
        round.end_datetime = (
            date if hasChangedDate and date else QDateTime.currentDateTime()
        )

    def set_round_name(self, round, name):
        round.name = name

    def manage_round_data(
        self,
        round,
        results_list,
        round_name,
        round_start_date,
        has_start_date_changed,
        round_end_date,
        has_end_date_changed,
    ):
        self.update_matches_results(round, results_list)
        if round_start_date and has_start_date_changed:
            self.set_round_start_date(round, round_start_date)
        self.set_round_end_date(round, has_end_date_changed, round_end_date)
        if round_name:
            self.set_round_name(round, round_name)
        self.save_changes(self.tournament)
