import tkinter as tk
from tkinter import simpledialog, messagebox

# Class for the Swiss System Tournament
class SwissTournament:
    def __init__(self, players, rounds):
        self.players = [{"name": player, "score": 0, "opponents": []} for player in players]
        self.rounds = rounds
        self.pairings = []
        self.current_round = 0

    def pair_players(self):
        # Sort players by score and name (score descending, name alphabetically for tie-break)
        self.players.sort(key=lambda x: (-x["score"], x["name"]))
        pairings = []
        unpaired = []

        i = 0
        # Pair players with similar scores
        while i < len(self.players) - 1:
            p1 = self.players[i]
            p2 = self.players[i + 1]

            # Ensure players haven't played each other before
            if p2["name"] not in p1["opponents"]:
                pairings.append((p1, p2))
                p1["opponents"].append(p2["name"])
                p2["opponents"].append(p1["name"])
                i += 2
            else:
                unpaired.append(p1)
                i += 1

        # Handle any unpaired players (due to odd number of players)
        if i == len(self.players) - 1:
            unpaired.append(self.players[-1])

        # If we have unpaired players, assign a bye to one player
        if unpaired:
            pairings.append((unpaired[0], None))  # None means bye

        self.pairings = pairings

    def update_scores(self, round_results):
        # Update player scores based on results
        for pairing, (p1_score, p2_score) in zip(self.pairings, round_results):
            pairing[0]["score"] += p1_score
            if pairing[1]:  # Handle bye scenario
                pairing[1]["score"] += p2_score

    def next_round(self):
        # Advance to the next round and generate new pairings
        self.current_round += 1
        if self.current_round <= self.rounds:
            self.pair_players()  # Generate new pairings
            return True
        return False

# GUI class for the tournament
class TournamentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Swiss System Chess Tournament")

        self.players = []
        self.tournament = None
        self.results_vars = []

        # GUI Components
        self.label = tk.Label(root, text="Enter number of rounds:")
        self.label.pack(pady=10)

        self.entry_rounds = tk.Entry(root)
        self.entry_rounds.pack(pady=5)

        self.button_add_players = tk.Button(root, text="Add Players", command=self.add_players)
        self.button_add_players.pack(pady=5)

        self.button_start = tk.Button(root, text="Start Tournament", command=self.start_tournament)
        self.button_start.pack(pady=5)

        self.result_frame = tk.Frame(root)
        self.result_frame.pack(pady=20)

        self.next_round_button = tk.Button(root, text="Next Round", command=self.next_round, state=tk.DISABLED)
        self.next_round_button.pack(pady=5)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=20)

    def add_players(self):
        num_players = simpledialog.askinteger("Input", "Enter the number of players:")
        for _ in range(num_players):
            player_name = simpledialog.askstring("Input", "Enter player name:")
            self.players.append(player_name)

    def start_tournament(self):
        rounds = int(self.entry_rounds.get())
        self.tournament = SwissTournament(self.players, rounds)
        self.next_round()

    def next_round(self):
        self.clear_results()

        if self.tournament.next_round():
            self.display_pairings()
            self.next_round_button.config(state=tk.NORMAL)
        else:
            self.display_final_standings()

    def display_pairings(self):
        pairings = self.tournament.pairings
        self.result_label.config(text=f"Round {self.tournament.current_round} pairings:")

        for i, pairing in enumerate(pairings):
            p1 = pairing[0]["name"]
            p2 = pairing[1]["name"] if pairing[1] else "BYE"

            # Player 1's score entry
            label_p1 = tk.Label(self.result_frame, text=f"{p1} score:")
            label_p1.grid(row=i, column=0, padx=10, pady=5)

            result_var_p1 = tk.DoubleVar()
            result_entry_p1 = tk.Entry(self.result_frame, textvariable=result_var_p1)
            result_entry_p1.grid(row=i, column=1, padx=10, pady=5)

            if pairing[1]:
                # Player 2's score entry
                label_p2 = tk.Label(self.result_frame, text=f"{p2} score:")
                label_p2.grid(row=i, column=2, padx=10, pady=5)

                result_var_p2 = tk.DoubleVar()
                result_entry_p2 = tk.Entry(self.result_frame, textvariable=result_var_p2)
                result_entry_p2.grid(row=i, column=3, padx=10, pady=5)

                self.results_vars.append((result_var_p1, result_var_p2))
            else:
                # Bye: Player 1 gets a default score of 1
                result_var_p1.set(1.0)
                self.results_vars.append((result_var_p1, tk.DoubleVar()))  # No player 2

    def save_results(self):
        results = []
        for result_var_p1, result_var_p2 in self.results_vars:
            p1_score = result_var_p1.get()
            p2_score = result_var_p2.get() if result_var_p2.get() != 0 else 0  # Handle default zero for bye
            results.append((p1_score, p2_score))
        self.tournament.update_scores(results)

    def display_final_standings(self):
        standings = sorted(self.tournament.players, key=lambda x: (-x["score"], x["name"]))
        result_text = "Final Standings:\n"
        for i, player in enumerate(standings):
            result_text += f"{i+1}. {player['name']} - {player['score']} points\n"
        self.result_label.config(text=result_text)
        self.next_round_button.config(state=tk.DISABLED)

    def clear_results(self):
        # Clear previous round results from the GUI
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        self.results_vars.clear()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentApp(root)
    root.mainloop()