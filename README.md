SUPER BUGRIO

How to start the game: run the "main.py" file

Developed with: Python 3.9.0
Libraries: pygame 2.1.0
Resolution: 1000*800
Support operating system: mac,windows,linux


-------------------------------
Game Overview: 
-------------------------------
Make it to the last level, defeat the evil monster, win the game!

-------------------------------
Operation guide (Keyboard operation) :	
-------------------------------
A: Left		
D: Right		
Space: jump	
K: Melee attack	
Shift + A/D: Speed up		
J: Long range attack


-------------------------------
Game characters design:
-------------------------------
Player:

The player will have two attacking models: melee and shooting attach; during each cooling down, the player is allowed to shoot five times. The initial HP is 100 points. All the items can interact with the player

Enemy:

All the enemies are finite-state machines; each frame calls a different function based on the enemy's state. The enemies detect the distance between themselves and the player using the searching function to change their state. The enemies allow to change their it from any kind of different state.
The basic attacking model for the enemies is melee attacking and shooting. The first advance attacking model is teleporting to the player's back and melee attack. If this model is not during the cooling down, the enemy will detach the model. The second advance attacking model is attacking during the dash. The enemy will call the attack function and dash to the player at double speed. The last advanced attacking model is switched between melee and shotting depending on the distance between the player and the enemy itself.
The boss has three phases, and each phase will bear attacked five times. The first phase is constantly at the third advanced attacking model above; after the player attacks the boss five times, the boss will go to the second phase. During the second phase, two dummy enemies will be summoned; also, the first advanced attacking model will be used. At the lase phase, the second model will use.

-------------------------------
Item design：
-------------------------------

Blood vessel: A blood vessel could add 10 HP for the player, and they are distributed everywhere in the states.

Scroll: A scroll will give the player 300 HP, to increase the change for player to defeat the boss

Portal door: The portal door will only appear after the player defeat every enemy and will allow the player enter to the next state.


-------------------------------
State design：
-------------------------------
A dedicated class is designed for the game levels. Each level has its environment group, monster group, and item group. Switch between different levels using finish variables and player status. If the player completes a level or dies, the code for switching levels is used to determine which level to switch to, depending on the situation. An intermediate scene is designed to show the levels in between switching levels.
There are two kinds of level objects. The ones where you can fight normal monsters are called normal levels because there is nothing special about this kind of object. We create methods directly in the parent class. Menu objects are unique because they do not operate by moving but by interacting with buttons. So, we created a separate subclass to define its update method.

<img width="400" alt="image" src="https://user-images.githubusercontent.com/93944793/202769834-d389d00d-b2e7-4677-8285-e9f7ca11fcdb.png">



-------------------------------
Game material Announcement
-------------------------------

* /Graphics  ----Picture files used by this game( .png format). 
	All picture files are made by Photoshop and Aseprite .
	(Aseprite is a pixel-art tool to create 2D animations, sprites, and any kind of graphics for games.) 

* /Music ----Music files used by this game(.mp3 format).
	The game background music(background.mp3) file in this document is used in the following link:
	https://freesound.org/people/josefpres/sounds/610926/
	Copyright allowed to be used.
	Other music files used in the document are made by AOQIV(Visual Musical Instrument).
 
-------------------------------
CONTRIBUTE
-------------------------------
1. I designed the entire game interface, including the game characters, menu page, the different levels of the game map, the player image, the enemy image, the props used in the game, and the attack effects of the characters， also involved in the writing of the storyline.
(All images were created by Photoshop and Aseprite, partly inspired by Super Mario.)

2. Modified and debugged the platform data in the map, the position of the game characters.

3. Involved the use of prop classes by enemies and players, who use bullets and swords against each other, modified the attributes of the props according to the state of the game characters.

4. Updated menu information (HP/LEVEL/TIME).



