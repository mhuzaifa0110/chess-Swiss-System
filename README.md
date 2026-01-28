# Swiss System (Chess) – Simple Tournament Apps

This folder has **3 small GUI programs** (Tkinter) for managing a chess tournament using a **Swiss-style pairing** idea.

## What is “Swiss system” (simple)
- Players play several rounds.
- You try to pair players with **similar scores** each round.
- Scores go up when players win (and sometimes for a draw).

## Files in this folder

### `swiss chess.py`
- **Purpose**: Swiss tournament app with a clear “tournament” class (`SwissTournament`) and a GUI (`TournamentApp`).
- **Pairing**: Sorts players by score (and name for ties), then pairs players in that order. It also tries to avoid pairing the same opponents again.
- **Bye**: If there is an odd number of players, one player gets a **BYE** (free point). This is handled safely.
- **Results input**: You type scores (example: `1` and `0`, or `0.5` and `0.5`) for each pairing.

### `swiss chess 2.py`
- **Purpose**: A simpler Swiss pairing GUI (`ChessTournament`) that stores players and scores in dictionaries.
- **Pairing**: Sorts players by score and pairs top-to-top.
- **Results input**: You type the **winner name** (or `draw`) for each pairing.
- **Important note**: It uses `"Bye"` as a fake player. If you type `"bye"` as the winner, it can cause an error because `"Bye"` is not in the scores list. (So this version is **less safe**.)

### `swiss_withList` (no file extension)
- **Purpose**: Very similar to `swiss chess 2.py`, but it also shows a **round summary window** after you record results.
- **Pairing**: Same style (sort by score, pair top-to-top, and `"Bye"` for odd players).
- **Tip**: This file has **no `.py` extension**. It is still Python code. You can rename it to `swiss_withList.py` to make it easier to run.

## How to run (Windows)
Open PowerShell in this folder and run one of these:

```bash
python "swiss chess.py"
python "swiss chess 2.py"
python "swiss_withList.py"
```


```bash
python "swiss_withList.py"
```

## Which one should I use?
- **Best overall**: `swiss_withList.py` (better structure, safer BYE handling, tries to avoid repeat opponents). I am working on this currently and making it more user-friendly. it has some repetitive window opening, and you have to close it everytime it opens. but i have conducted an online tournament on using this one, and it was successful.
