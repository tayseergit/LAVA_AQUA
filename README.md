# 🔥 LAVA Game

LAVA is a grid-based puzzle game that demonstrates classic **AI search algorithms**.  
The user selects a level and lets different algorithms solve it automatically.

---

## ▶️ How to Run

Make sure you have **Python 3.10 or higher** installed.

From the project root directory, run:

```bash
python main.py




🎮 Controls
Level Selection

Arrow Keys (↑ ↓ ← →) → Move between available levels

Enter → Confirm and start the selected level

Algorithm Controls (During Gameplay)

u → Run UCS (Uniform Cost Search)

b → Run BFS (Breadth-First Search)

d → Run DFS (Depth-First Search)

Each key triggers the selected algorithm to automatically solve the current level.

🧠 Algorithms

UCS (Uniform Cost Search)
Explores paths based on the lowest cumulative cost and guarantees the optimal solution.

BFS (Breadth-First Search)
Explores the state space level by level and guarantees the shortest path in unweighted graphs.

DFS (Depth-First Search)
Explores as deep as possible before backtracking. Fast but not optimal.

📁 Project Structure
.
├── main.py
├── core
│   ├── actions.py
│   ├── states.py
│   ├── solver.py
│   └── controller
│       ├── ucs.py
│       ├── bfs_solver.py
│       └── dfs_solver.py
├── data
│   └── maps_txt
└── presentation