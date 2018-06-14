Feature Ideas:
-----------------------------------------------------------------------------

Rest XP - pool of future XP you acquire staying in an Inn gain faster when 
          you log back in.
            rest_xp_pool = 2000   # Amount of XP, based on duration
            rext_xp_rate = 1.21   # Accrued based on duration

XP events - periods where XP rewarded is factored up.  Implementing this and
            Rest XP would depend on reward_xp() function that can take into
            account a global factor and an individual factor.

Categorized inventory - show weapons, etc.  maybe you can subclass this to:
                        show wieldable (show things your player can use)
                        show enchanted weapons

Trash items - avoid these if possible.

Multi-profile  - login as a user should show you a character list if you
                 have more than one character.  You should be able to copy
                 some settings (terminal, colors, auto-loot) from one to
                 another

Inspect compare - when you inspect an item, compare against currently worn
                 item - report whether wearable by your player or not.
                 See "Ansilon" MUD inspect


Talent trees - Similar to Assassin's Creed.  Maybe there are talent points
               that you can receive for the purpose of adding abilities, 
               with costs and dependencies (must have X before Y before Z).
               Maybe these are different per class.
                talent_tree = [
                    {'name': 'chemistry', 'cost': 1, 'level': 12, 'depends': [] }
                    {'name': 'alchemy',   'cost': 2, 'level': 18, 'depends': ['magician', 'chemistry' ] }
                    {'name': 'enchant',   'cost': 3, 'level': 25, 'depends': ['alchemy'}
                ]

Auction House - players can list equipment for sale and the auction house
                will announce and run an auction.  End within some amount
                of time and award to highest bidder.  If nobody bids, maybe
                it automatically re-lists once per day up to some limit.

Procedurally generated areas - Quest/Area that's auto-generated (map to find
                a dragon's lair, which is an automatically generated area
                and lives until you slay the dragon, at which point it is
                destroyed and a new area is auto-generated)

Food / Drink  - not for hunger, but for buffs / effects.  Might be some risk involved.

Combat - Impair NPCs more according to their condition.  As they are wounded, they
         don't dodge/parry, and they lose dexterity and strength



-----
## Abilities:

* Heal
* Resurrect
* Shield (minor/major)

### Commands:

# Specials: @USER commands
Have a special class of "breakout" commands that pertain to users and not to
players.  The idea is that some commands like subscribing to a chat channel 
or altering protocol prefs (MCCP, Colorize, etc) would always be within a
user's commandSet (maybe by virtue of default/extra parsing).  Maybe this 
toggles a player's state to a pause/protect and while you're in the @command
system you're not affected by the world around you.

# Pager system in prompt output
@prefs prompt
@prefs pager [on|off] - page output longer than _preferences['rows']
  This one could be tricky to implement well.  What can break out of a pager
  state, and what becomes of prompt?  (supposedly prompt is only shown once
  paged text is fully flushed and confirmed).  Seems like attacks should break
  through pager.  In a client that enables OOB protocol for chat updates, at
  least that could update in a separate context and not muck up the main
  window.

### Automap
## Found a cool article on mapping, looks like it might be possible to
automap if the world is kept regular enough to make this practical.
It would be really nice if this could be defined as an X * Y grid of text
rows and columns and the map would render within this (so LoD would shift
based on how large a canvas we can allocate)
--

## Modals
Implement a modal which is a class you can inherit and override to implement
a dialog.  It's a state machine that allows for back-n-forth outside of normal
command processing.  One question is: what happens if we enter a modal during
gameplay?  Maybe we disappear or appear "frozen" or similar.  Shouldn't be able
to enter a modal when you're doing certain things(fighting, f.e.)
  The login handler could be re-implemented as a modal.