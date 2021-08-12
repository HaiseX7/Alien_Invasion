# Alien_Invasion
A video game made using PyGame that emulates galactic invasion.
This Game contains 8 Classes all with their own unique purpose.

An indentation means that the function was called from the outer function its indented off of

# How to run
run alien_invasion.py throught the terminal or through an IDE

# Controls
The game is started by clicking the mouse on the buttons for the difficulty and start game

*Directional Keys*- moves the ship

*Spacebar*- fires a bullet

*R*- restarts the game

*Q*- quits the game

*P*- starts the game if a difficulty has been selected

# Alien Invasion:

This class is designed to handle the main instance of the game and everything that involves running it specifically.  
  
## *init()* 
creates the instances (Settings, Ship, Bullet, Scoreboard, Game Stats, and Button), sprite groups (Bullets and Aliens), screen, music, and fleet of aliens.

        1.) create_fleet() creates the fleet of aliens using a nested for loop 
            - create_alien() creates an instance of the Alien class to fill the Aliens group    
        
## *run_game()* 
runs a while loop that runs the game. In this loop we call the functions that check events, update the ship, aliens, bullets, and screen. 

### check_events() 
iterates through the event loop and checks for user input.

        1.) check_keydown_events() checks key presses that're needed for updating the game (ship movement, firing bullets, quitting or resetting the game etc.)
            - fire_bullet() responds to a space bar press and creates an instance of Alien and adds it to the group that was initialized in init()
            - start_game() starts the game after the player presses the p key
            - reset_stats() helps reset the game after the r key is pressed. 
            - write_high_score() is called right before the quit button is pressed.
        2.) check_keyup_events() checks when a key press is released so we can do things like stopping the ship
        3.) check_play_button() checks if the mouse has clicked the play button from the button class and if it was clicked it starts the game
            - If _check_difficulty_selected(): 
              - set_difficulty() uses Settings class to initialize difficulty settings
                - Music.button_click() plays the sound for a button click
                - start_game() starts the game after the player presses the button using the mouse
                  - Settings.initialize_dynamic_settings() intializes the settings that dynamically change throughout the game using the Settings class
                  - Scoreboard.prep_score() displays score using Scoreboard class
                  - Scoreboard.prep_level() displays level using Scoreboard class
                  - Scoreboard.prep_ships() displays ships lives using Scoreboard class
                  
### Ship.update() 
updates the ship using the Ship class

### update_bullets() 
updates bullets group

        1.) Bullets.update() moves the Bullets group using the update function from the Bullet class
        2.) remove_bullet() removes bullets the pass the edge
        3.) check_bullet_alien_collision() checks for collisions and if all the aliens are destroyed creates a new fleet
            - If theres a collision: 
              - prep_score() and check_high_score() display the score if an alien was hit and check if there was a high score after the m                   score                   was updated
            - If the fleet was destroyed: 
              - Settings.increase_speed() increases the difficulty of the game after a fleet was destroyed using the Settings class,                                               Scoreboard.prep_level() displays a new level if the fleet was destroyed using the Scoreboard class, and create_fleet() creates the new fleet
            
### update_aliens() 
updates everything regarding the aliens group

        1.) check_fleet_edges() checks if the fleet has reached and edge and if so it calls change_fleet_direction()
            - change_fleet_direction() changes the direction of the fleet
        2.) aliens.update() updates the aliens group using the update() function from the Alien class
        3.) check_ship_collision() checks if theres a ship collision
            - ship_hit() is called (soft resets the game)
        4.) check_aliens_bottom() checks If an alien reaches the bottom of the screen. If one does it counts as the ship being hit
            - ship_hit() is called (soft resets the game)
        
### *update_screen()* 
continously updates the screen to account for everything that was initiated and everything thats been occuring in run_game()

        1.) Ship.blitme() draws the ship to rectangle using the Ship class
        2.) Bullet.draw_bullet() draws the bullets to the screen using the bullet class
        3.) Aliens.draw() draws the aliens to the screen using the Group class that was imported
        4.) Scoreboard.show_score() shows all the statistics on the screen using the Scoreboard class
        5.) If the game isn't active and a difficulty hasn't been selected: 
            - draw_difficulties()
        6.) If the game isn't active: 
            - Button.draw_button() draws the button to the screen using the Button class
    
# Ship:

This class is designed to control all the information regarding the ship and also uses the Sprite class to show ship lives

## *init()* 
initializes Alien Invasions screen and its rect, it loads the image, it defines its coordinates, and sets its moving flags
## *update()* 
updates the ships x position in response to user input
## *center_ship()* 
centers the ship once the game hard or soft resets
## *blitme()* 
draws the ship image onto a rect which is then pasted on to the screen

# Alien:

This class is designed to control all the information regarding a single alien.

## *init()* 
initializes Alien Invasions screen and its rect, it loads the image, and it defines its coordinates
## *update()* 
updates the aliens x position
## *check_edges()* 
returns true if an alien has reached the edge

# Bullet

This class controls the info on one bullet and also uses the Sprite class

## *init()* 
initializes the screen, rect and its position, and an instance of settings
## *update()*
updates the position of each bullet
## *draw_bullet()*
draws the bullet to the screen

# Settings:

This class is designed to control the static and dynamic settings of the game

## *init()* 
initializes the static settings for the screen, ship, bullet, and alien and also defines the speedup scale and initializes all the dynamic settings through a function call
## *initialize_dynamic_settings()* 
initializes the dynamic settings for the game such as fleet direction and the speed of the aliens, ship, and bullets
## *increase_speed()* 
is a function that is called in Alien Invasion that increases the speed of the dynamic settings after a fleet is destroyed

# Scoreboard:

This class displays the stats on the screen

## *init()*
initializes font settings and instances of Alien Invasion, Settings, and Game Stats. Also it calls prep_score, prep_high_score, prep_level(), and prep_ships() to prepare them for display by rendering them
## *show_score()*
displays the score, high score, level, and ship lives
## *check_high_score()* 
checks to see if a high score was reached. called in check_bullet_alien_collisions.
## *write_high_score()*
writes the high score to a file once the game is ended

# Game Stats

This class controls the game's statistics

## *init()* 
initializes the stats by using reset_stats() and tries to write the high score to a JSON file so it can be saved once the program is exited
## *reset_stats()* 
redefines the game statistics after a new game

# Button

This class controls the play button

## *init()* 
initializes properties of the button and a screen and rect
## *prep_msg()* 
renders a message and defines its rect
## *draw_button* 
draws the button after its message has rendered

# Music

This class controls the music and sound design of the game

## *init()*
initializes pygame.mixer
## *play_music()*
loops the games main music
## *button_click()*
plays a sound whenever a button object is clicked with the mouse
