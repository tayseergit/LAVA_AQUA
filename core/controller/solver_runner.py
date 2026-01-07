import time
import pygame

from core.component.symbols import DIRECTION


def visualize_solver_path(
    path,
    initial_state,
    result_class,
    display,
    solver_name,
    visited_states,
    generated_states,
    execution_time,
    cost=0,
    sleep_time=0.1,
):
    handler = result_class()

    for action in path:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        dy, dx = DIRECTION[action]
        handler.update_environment_and_player(initial_state, (dy, dx))

        display.update_display()
        time.sleep(sleep_time)

    print(f"\n===== {solver_name.upper()} STATS =====")
    print("Visited:", visited_states)
    print("Generated:", generated_states)
    if cost>0 :
        print("cost : ",cost)
    print("Length:", len(path))
    print(f"Execution Time: {execution_time:.6f} seconds")
    print("=====================\n")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        display.update_display()
    pygame.display.quit()
