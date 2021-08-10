# Alien_Invasion
A video game made using PyGame that emulates galactic invasion.
This Game contains 8 Classes all with their own unique purpose.

Alien Invasion (1):

  This class is designed to handle the main instance of the game
  and everything that involves running it specifically.  
  
  - init() creates the instances (Settings, Ship, Bullet, Scoreboard, Game Stats, and Button), sprite groups (Bullets and Aliens), screen, and fleet of aliens.
      - create_fleet() creates the fleet of aliens using a nested for loop     
  
  - run_game() runs a while loop that runs the game. In this loop we call the functions that check events, update the ship, aliens, bullets, and screen.  
      - check_events() iterates through the event loop and checks for user input.  
           - check_keydown_events() checks key presses that're needed for updating the game (ship movement, firing bullets, quitting or resetting the game etc.)
                - fire_bullet() responds to a space bar press and creates an instance of Alien and adds it to the group that was initialized in init()
                - start_game() starts the game after the player presses the p key
                - reset_stats() helps reset the game after the r key is pressed. 
           - check_keyup_events() checks when a key press is released so we can do things like stopping the ship
           - check_play_button() checks if the mouse has clicked the play button from the button class and if it was clicked it starts the game
                - start_game() starts the game after the player presses the button using the mouse
                - Settings.initialize_dynamic_settings() intializes the settings that dynamically change throughout the game using the Settings class
                - Scoreboard.prep_score() displays score using Scoreboard class
                - Scoreboard.prep_level() displays level using Scoreboard class
                - Scoreboard.prep_ships() displays ships lives using Scoreboard class
      - Ship.update() updates the ship using the Ship class
      - update_bullets() updates and gets rid of bullets that fly off the screen
           - Bullets.update() moves the Bullets group using the update function from the Bullet class
           - check_bullet_alien_collision() checks for collisions and if all the aliens are destroyed creates a new fleet
                - If theres a collision: prep_score() and check_high_score() display the score if an alien was hit and check if there was a high score after the m                   score was updated
                - If the fleet was destroyed: Settings.increase_speed() increases the difficulty of the game after a fleet was destroyed using the Settings class,                   Scoreboard.prep_level() displays a new level if the fleet was destroyed using the Scoreboard class, and create_fleet() creates the new fleet
              
