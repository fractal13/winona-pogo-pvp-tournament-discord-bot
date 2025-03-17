Draft Tournament Support
------------------------

## Overview

A draft tournament is one where a group of trainers take turns selecting
a pokemon from the allowed pool of pokemon. Once a pokemon has been selected
by one trainer, no other trainer can select it. Allowed pokemon pools
can be open or thematically selected. Some things to consider when
choosing a pool:

- shadow
- mega
- regional (e.g. galarian stunfisk vs unova stunfisk)
- move set (e.g. genesect drive differences)
- purified (probably doesn't matter)
- ??other??

Some draft tournaments start with one or more ban rounds, where pokemon
in the allowed pool are banned by trainers. If banned, the pokemon is no 
longer available for selection.

A draft order is usually set at the beginning of the tournament, and trainers
take their turns banning or drafting according to that order. It is common
practice for the draft order to follow a "snake" pattern, where the last
trainer in the first round becomes the first trainer in the next round, and
the draft order reverses each round. *Are there other draft orders that
people like or use?*

Once each trainer has drafted their team of pokemon, the trainers battle using
only their selected pokemon. Formats that I've seen include

- teams of 6 pokemon, each battle each trainer selects 3 to bring
- teams of 8 pokemon, each round the opponent trainer temporarily bans 2 of 
  the trainer's pokemon, each battle the trainer selects 3 of the 
  remaining 6 to bring
- ?Others?

The tournament is usually run in rounds, where trainers are paired up,
do a best-of-n set of battles, and record the result. Currently (2024),
the tournament pairings and recording of battles are usually done using
the [Dracoviz system](https://www.dracoviz.gg).

When all of the rounds are completed, the trainer with the best record
wins the tournament. Again, this ranking is usually done within the
Dracoviz system at the current time.

# Draft Tournament Support Features

We plan to create a discord bot to support tournament creation and
management. Specifically, the first iteration will be able to support
the drafting process, leaving the pairing and round management to the
Dracoviz system.

This is a list of the actions that the bot will provide to support the
drafting process. The following subsections of this document will provide
more details about each of these actions.

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
- Admin removes trainer from tournament


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
  - automatic reminders would be better than manual commands.
  - manual command could still be an option.

## Admin removes trainer from tournament
  - ??


# Data Structures

## User Information

- Discord name
- Discord name in server
- Discord ID
- POGO trainer name
- POGO trainer code
- User's preferred timezone

## Tournament Information

- Discord server name
- Discord server ID
- Discord role for all trainers in the tournament
- Tournament name
- Tournament description
- Tournament CP cap
- Round length
- Number of ban rounds
- Link to Dracoviz or other tournament management system
- (not yet) tournament disallowed pokemon list
- (not yet) tournament allowed pokemon list

## Pokemon Species Information

- Name
- Dex number
- Region (if applicable)
- Form (if applicable)
- Shadow status
- ?? Anything else that could be used to distinguish between unique selections

# TODO

Is there an API for Dracoviz that we could use to download data for rounds? 
What about submit team selections for trainers? What about trainers reporting
their match results?

