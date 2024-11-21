Draft Tournament Support Features
---------------------------------

- User registers for tournament
- User leaves tournament
- User selects a pokemon ban
- User selects a pokemon draft
- User lists pokemon available/banned/drafted
- User requests strings to copy/paste into pvpoke for simulations/sorting/etc.
- Admin creates tournament
- Admin updates tournament meta data
- Admin sets draft order
- Admin starts draft
- Admin starts battle round
- Admin sends reminders to complete round battles
- Admin removes player from tournament


## User registers for tournament
  Joining a tournament effects:
    * the user to be entered in the tournament
    * the user joined to the discord server role for the tournament
    * ??
  + Before the draft begins, automatic
  + After the draft begins, ??

## User leaves tournament
  Leaving a tournament effects:
    * the user to be removed from the tournament
    * the user removed from the discord server role for the tournament
    * ??
  + Before the draft begins, automatic
  + After the draft begins, all bans stay in place, all previous selections become bans, automatic
  + After battles begin, ??

## User selects a pokemon ban
  If the pokemon has not been banned, and the pokemon is available to be banned:
  - the pokemon is marked as banned
  - the pokemon is added to the user's ban list
  - the next trainer to ban/draft is tagged
  
## User selects a pokemon draft
  If the pokemon has not been banned, and the pokemon has not been drafted, and the pokemon is available to be drafted:
  - the pokemon is marked as drafted
  - the pokemon is added to the user's draft list
  - the next trainer to draft is tagged
  - if this was the last draft, then the admin is tagged.

## User lists pokemon available/banned/drafted
  For all pokemon available in the draft, the user will information about it.
  
## User requests strings to copy/paste into pvpoke for simulations/sorting/etc.
  More details need to be provided. This feature supports users planning
  their bans/drafts by using pvpoke, or other external tools.

## Admin creates tournament
  The admin will specify all of the meta data about the tournament.
  See the list of tournament information below.

## Admin updates tournament meta data
  The admin edits the tournament meta data.

## Admin sets draft order
  We can possibly:
  - randomly shuffle users
  - allow admins to set the order (via csv file?)
  - shuffle users with a timezone sensitive sort

## Admin starts draft
  - First user to ban/draft is tagged
  - status of tournament is set to ban/draft stage

## Admin starts battle round
  - All users (role) are tagged

## Admin sends reminders to complete round battles
  This could happen by manual command of admin, or by schedule.
  - tag all users who have not had their battles completely reported.

## Admin removes player from tournament
  - ??


User Information
----------------

- Discord name
- Discord name in server
- Discord ID
- POGO trainer name
- POGO trainer code
- User's preferred timezone

Tournament Information
----------------------

- Discord server name
- Discord server ID
- Discord role for all players in the tournament
- Tournament name
- Tournament description
- Tournament CP cap
- Round length
- Number of ban rounds
- Link to Dracoviz or other tournament management system
- (not yet) tournament disallowed pokemon list
- (not yet) tournament allowed pokemon list

Pokemon Species Information
-------------------

- Name
- Dex number
- Region (if applicable)
- Form (if applicable)
- Shadow status
- ?? Anything else that could be used to distinguish between unique selections

TODO
----

Is there an API for Dracoviz that we could use to download data for rounds? 
What about submit team selections for players? What about players reporting
their match results?

