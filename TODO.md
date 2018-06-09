###To Do:
-----------------------------------------------------------------------------
## STORAGE

* Generalized save/load to work with all types (items, rooms, players, npcs, shops, etc)
* Boot_db() to load all world objects on startup


## Items

* Create base_item
* Create weapon, armor, book, food, potion, scroll, key, container, 
         staff, wand, money, food, clothing, drink, trash, misc?


## Characters / Chargen / Login

* Implement banned
* Implement badwords
* Implement races
* Implement classes
* Implement random chargen


## Command Handler

* Create pager
* Test wrapping
* Create customizable prompt
* Create @who
* Create score, help, quit
* First set of commands:  who, tell, shout(broadcast), quit, stats* write unit tests!

# Expand command system based on states:
The command table will include data about what the nominal state of a player
  must be in order to execute a command.  Give feedback on failures.

* Implement state (health / dead)
* Implement position (sitting, laying down, standing, flying, etc)
* ex. "land" - only works if flying
* ex. "run" only works if >= standing

# Complex commands:

* runto: auto-move to a destination (by rooom name/area name)
      This should work only if you've been there before, which means keeping
      track of user-known rooms.  Do we want to do this?  (maybe eventually)


## SEE IDEAS.md as well - stuff a few ideas there