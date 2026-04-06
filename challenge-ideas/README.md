# Challenge Ideas

This folder contains optional design suggestions for the prison-break CTF. These are intended as organizer notes only. They are not required for the final implementation and should be treated as a menu of ideas rather than a locked plan.

## Design Principles

- Keep the CTF linear at the challenge level but parallel at the branch level
- Make each branch feel mechanically distinct
- Ensure each branch produces a concrete artifact needed for the final exit
- Prefer clue chains where the output of one challenge naturally justifies the next

## Full Suggested Sequence

### Initial Challenge

#### Challenge 1: Smuggled Burner Phone

The player finds or is given a confiscated burner phone image, backup, or emulated filesystem. The lock screen hint and messages contain enough material to recover a passcode or hidden note that opens the cell.

Possible mechanics:

- Extract a phone PIN from image metadata, message timestamps, or a simple pattern-lock clue
- Recover deleted SMS content from a phone backup
- Decode a note hidden in a contact list or image gallery

Suggested output:

- A code, URL, or flag that unlocks the prison cell and reveals the three branch entry points

## Control Room Path

#### Challenge 1: Vulnerable CCTV Portal

Players discover an internal CCTV web portal with weak authentication, exposed credentials, or a simple injection flaw. Solving it yields low-privilege access to monitoring systems.

Possible mechanics:

- Default credentials hidden elsewhere in the environment
- SQL injection on the login form
- Weak password reset flow tied to security questions

Suggested output:

- Operator credentials, VPN config, or an internal hostname needed for the next challenge

#### Challenge 2: Windows Admin Pivot

The CCTV foothold leads to a Windows or Active Directory environment. Players must enumerate shares, recover credentials, or abuse a common misconfiguration to get elevated access.

Possible mechanics:

- Password reuse between web app config and a Windows account
- GPP password, exposed script credential, or accessible share
- Kerberoasting or a simpler lab-safe AD weakness

Suggested output:

- Higher-privilege account access or a remote management path into the control host

#### Challenge 3: Door Control Override

Players use privileged access to interact with the prison door-control system. The goal is not just a flag, but a state change that narratively unlocks the path to the final area.

Possible mechanics:

- Modify a database value controlling door states
- Trigger an internal API with the recovered credentials
- Edit a scheduled task, script, or PLC simulator config to unlock doors

Suggested output:

- Confirmation code, unlock token, or changed game state indicating the final corridor is now accessible

## Guard Room Path

#### Challenge 1: Shift Log Recon

Players find guard schedules, memos, or locker assignments that point to the correct storage location or combination method.

Possible mechanics:

- OSINT-style correlation across notes, badges, and locker labels
- A PDF or image with hidden text
- A notebook page whose dates and initials map to a combination

Suggested output:

- Guard name, locker number, or stash location for the next stage

#### Challenge 2: Encrypted Guard Notes

The guard’s personal notes are protected by a lightweight cryptography or puzzle challenge. This should be more puzzle-oriented than the server path.

Possible mechanics:

- Vigenere or rail-fence cipher with the key hidden in Challenge 1
- Book cipher using a handbook found in the same folder
- Multi-step puzzle where decoded text reveals another clue rather than the final answer directly

Suggested output:

- Safe combination, stash code, or location of the keycard container

#### Challenge 3: Keycard Recovery

Players use the prior clues to access the actual keycard or its digital equivalent.

Possible mechanics:

- Open a locker archive or encrypted zip
- Recover an RFID dump, badge image, or card ID from a workstation
- Assemble pieces of a badge credential from several files

Suggested output:

- The keycard artifact required at the final exit

## Server Room Path

#### Challenge 1: Internal Network Enumeration

Players are given access to a small internal range or a scan result and must identify the relevant prison server that stores exit-related data.

Possible mechanics:

- Nmap-driven discovery of services
- Banner clues that distinguish production from decoy hosts
- A web service with robots.txt or directory hints

Suggested output:

- The specific host, service, or endpoint to target next

#### Challenge 2: Linux or Web Compromise

Players exploit the identified host and gain a foothold sufficient to search for sensitive operational data.

Possible mechanics:

- File traversal in a web app
- Command injection in an admin tool
- Simple Linux privilege escalation after web-shell access

Suggested output:

- Shell access, root access, or access to protected application data

#### Challenge 3: Pincode Extraction

Players search the compromised system and recover the final door pincode.

Possible mechanics:

- Read a config file containing the code
- Decrypt an admin backup with a nearby key
- Query a local database or parse logs for the latest door PIN update

Suggested output:

- The pincode required at the final exit

## Final Exit

#### Challenge 1: Multi-Factor Escape

The final door should require everything the player earned. It should not be solvable by guessing or by only completing one branch.

Possible mechanics:

- Submit keycard ID and pincode to an access panel, then solve one final validation challenge
- Use the keycard to decrypt a file that contains the real format for the pincode entry
- Combine the branch outputs into a final command, phrase, or unlock sequence

Suggested output:

- Final flag and narrative completion of the prison break

## Alternate Ideas

If you want to vary the branches, these swaps fit the same overall structure:

- Replace burner phone forensics with a hidden radio message or QR code chain
- Replace AD escalation with a Linux-based control server if you want less Windows infrastructure
- Replace classical crypto in the guard room with steganography or physical-note reconstruction
- Replace direct exploitation in the server room with log analysis and credential reuse if you want a gentler difficulty curve

## Implementation Advice

- Make challenge outputs reusable artifacts, not just flags
- Keep each branch internally coherent so players do not lose the narrative thread
- Avoid making the guard room too puzzle-heavy if the other branches are strongly technical
- Seed each branch entry point clearly after the initial challenge so players know all three are available
