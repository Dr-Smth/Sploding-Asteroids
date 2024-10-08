import pygame
import os
import sys
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *
from start import handle_start_state
from ship_select import handle_ship_select_state
from running import handle_running_state
from game_over import handle_game_over_state

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def main():
    print("Starting 'Sploding Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    # Initiates delta time variable
    dt = 0

    # Initiates player variables
    player_lives = 3
    player_score = 0
    asteroid_kill_score = 0
    asteroid_kills = 0
    time_score = 0
    high_score = 0

    # Load player assets
    player_assets = []

    for filename in os.listdir(PLAYER_SHIP_ASSETS):
        # Constructs full path to asset
        image_path = os.path.join(PLAYER_SHIP_ASSETS, filename)

        image = pygame.image.load(image_path).convert_alpha()

        player_assets.append(image)

    # Load shot asset
    shot_image = pygame.image.load(SHOT_IMAGE).convert_alpha()

    # Load asteroid assets
    asteroid_assets = []

    for filename in os.listdir(ASTERPOD_ASSETS):
        # Constructs full path to asset
        image_path = os.path.join(ASTERPOD_ASSETS, filename)

        image = pygame.image.load(image_path).convert_alpha()

        asteroid_assets.append(image)

    
    # Scale images
    player_assets = [pygame.transform.scale(img, (64, 64)) for img in player_assets]
    shot_image = pygame.transform.scale(shot_image, (32, 32))

    selected_ship_index = 30  # Default selected ship
    selected_ship_image = player_assets[selected_ship_index]
        
    # Initialize sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Assign sprite groups to class-level containers
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    # Initiates player and astroid field
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, selected_ship_image, shot_image)
    asteroid_field = AsteroidField(asteroid_assets)

    # Initiates game font for on screen text
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 24)

    game_state = "start"  # Possible states: "start", "ship_select", "running", "game_over"
    prev_game_state = None # Initilises prev game state
  
    def reset_game():
        nonlocal player_score, asteroid_kill_score, asteroid_kills, time_score, player_lives
       
        # Reset the score
        player_lives = 3
        player_score = 0
        asteroid_kill_score = 0
        asteroid_kills = 0
        time_score = 0

        reset_level()

    def reset_level():
        nonlocal updatable, drawable, asteroids, shots, player, asteroid_field, selected_ship_image

        # Clear all sprite groups
        updatable.empty()
        drawable.empty()
        asteroids.empty()
        shots.empty()

        # Reinitialize sprite groups and containers
        Player.containers = (updatable, drawable)
        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = updatable
        Shot.containers = (shots, updatable, drawable)

        # Recreate player and asteroid field
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, selected_ship_image, shot_image)
        asteroid_field = AsteroidField(asteroid_assets)

    while True:
        events = pygame.event.get()  # Collects all events once per frame

        if game_state == "start":
            game_state = handle_start_state(screen, font, events, high_score)
        elif game_state == "ship_select":
            game_state, selected_ship_index, selected_ship_image = handle_ship_select_state(screen, font, events, player_assets, selected_ship_index)
        elif game_state == "running":
            game_state, player_score, asteroid_kill_score, asteroid_kills, time_score, player_lives = handle_running_state(screen, updatable, drawable, asteroids, shots, player, dt, player_lives, player_score, asteroid_kill_score, asteroid_kills, time_score, font, events, reset_level)
        elif game_state == "game_over":
            game_state, high_score = handle_game_over_state(screen, font, events, player_score, asteroid_kill_score, asteroid_kills, high_score)

        # Check if we need to reset the game
        if game_state == "running" and prev_game_state in ["start", "game_over"]:
            reset_game()

        prev_game_state = game_state  # Update the previous game state

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()