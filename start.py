import pygame
import sys
from constants import *

def handle_start_state(screen, font, events, high_score):
    # Fill the screen with a background color
    screen.fill((0, 0, 0))

    # Render the game title, instructions, and high score
    title_text = font.render("'Sploding Asteroids !!!", True, (255, 255, 255))
    instruction_text = font.render("Press ENTER to Start", True, (255, 255, 255))
    select_ship_text = font.render("Press S to Select Your Ship", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))

    # Get rectangles for positioning
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    select_ship_rect = select_ship_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
    high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 150))

    # Blit the text onto the screen
    screen.blit(title_text, title_rect)
    screen.blit(instruction_text, instruction_rect)
    screen.blit(select_ship_text, select_ship_rect)
    screen.blit(high_score_text, high_score_rect)

    # Handle events on start screen
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Start the game
                return "running"
            elif event.key == pygame.K_s:
                # Go to ship selection screen
                return "ship_select"

    return "start"