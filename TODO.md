# To Do

## Rooms

* ~~Move code to check/list exits into rooms.py (avoid importing DIR_*)~~
* ~~Update room info display to wrap based on width (down to maybe 40 chars)~~

## STORAGE

* ~~Generalized save/load to work with all types (items, rooms, players, npcs, shops, etc)~~
* Move _checksum, _last_saved into base_object, as properties
* Move "skip_list" into object as property to avoid having to pass it during save()
* Boot_db() to load all world objects on startup

## Items

* Create base_item
* Create weapon, armor, book, food, potion, scroll, key, container,
         staff, wand, money, food, clothing, drink, trash, misc?

## Characters / Chargen / Login

* Implement banned
* Implement badwords
* Implement races
* Implement random chargen

## Command Handler

* Create pager
* Test wrapping
* Create customizable prompt?
* Create score, help

### Expand command system based on states

The command table will include data about what the nominal state of a player
  must be in order to execute a command.  Give feedback on failures.

* Implement state (health / dead)
* Implement position (sitting, laying down, standing, flying, etc)
* ex. "land" - only works if flying
* ex. "run" only works if >= standing

### Complex commands

* runto: auto-move to a destination (by rooom name/area name)
      This should work only if you've been there before, which means keeping
      track of user-known rooms.  Do we want to do this?  (maybe eventually)

SEE IDEAS.md as well - stuff a few ideas there