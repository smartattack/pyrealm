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



