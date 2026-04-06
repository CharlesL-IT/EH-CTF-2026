# Server Room

## Objective

This branch ends with the player recovering the pincode needed to open the final exit door.

## Expected Flow

1. Enumerate and identify the relevant prison network target
2. Compromise the target and move toward protected data
3. Recover the pincode from the system

## Suggested Theme

This branch is the strongest fit for:

- Network scanning and service enumeration
- Linux exploitation
- File traversal
- Metasploit-assisted exploitation if appropriate
- Web exploitation such as XSS or Burp-driven testing

## Reward

The final output of this branch should be the pincode used at the final exit. The code can be stored in a config file, database, internal note, log source, or protected admin interface.

## Branch Structure

- `challenge-1`: enumeration and foothold
- `challenge-2`: host or application compromise
- `challenge-3`: pincode recovery
