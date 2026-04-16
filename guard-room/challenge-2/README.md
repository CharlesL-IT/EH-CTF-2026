# Seed-cret Escape

## Category
Crypto

## Story
While you have made it through the first door, you now need to make it through a second door using the prison emergency release terminal. Fox River Penitentiary keeps its emergency release codes behind a "secure" vault terminal. The warden insists the password changes constantly and is impossible to predict, even if a few characters leak each round.

Your have reached the terminal, and you only have one job now: break into the vault before the guards make their rounds.

## Objective
Recover the full vault password and use it to obtain the flag.

## Files Provided
- `Seed-cret_Escape.py`

## Connection
- Host: `<challenge-host>`
- Port: `1337`

## Notes
- The service reveals the first 5 characters of the current password before asking for your guess.
- The password is 15 characters long.
- Lowercase letters and digits are used.

## Flag Format
`PrisonCTF{...}`
