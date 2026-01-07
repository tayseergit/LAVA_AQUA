# main.py
from core.solver import Solver
from presentation.level_select import LevelSelectScreen
from presentation.level_preview import LevelPreviewScreen


def main():

    while True:
        selector = LevelSelectScreen()
        level_name = selector.run()

        if level_name is None:
            break

        preview = LevelPreviewScreen(level_name)
        solver_key = preview.run()

        if solver_key is None:
            continue

        solver = Solver(level_name)
        try:
            solver.run_solver(solver_key)
        except ValueError as exc:
            print(exc)


if __name__ == "__main__":
    main()
