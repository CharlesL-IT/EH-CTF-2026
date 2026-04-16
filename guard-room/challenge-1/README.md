# Timed Entry

## Category
Crypto

## Story
In order to be able to escape the prison, you're going to need one of those extra keycards you overheard the guards talking about. They say you can find one in the vault stored in the guard room. 

Right now, the first guard room still stands between you and the inner cell blocks. A keypad terminal controls the next security door, and the guards swear the access check is airtight.

The system only asks for one thing: the password. If you can slip past Guard Room 1, you get one step closer to the vault deeper inside the prison.

## Objective
Recover the correct password and use it to obtain the flag.

## Files Provided
- `timing_side_channel_challenge.py`

## Connection
- Host: `<challenge-host>`
- Port: `1227`

## Notes
- The service prompts for a password and returns either success or failure.
- The password uses uppercase letters, lowercase letters, digits, and symbols.
- This is Guard Room 1. Guard Room 2 continues with `Seed-cret_Escape`.

## Flag Format
`PrisonCTF{...}`
