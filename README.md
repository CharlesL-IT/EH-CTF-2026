# EH-CTF-2026

A prison-break themed capture the flag created in Spring 2026 for students in Ethical Hacking 650.631 at Johns Hopkins.

<img src="assets/Prison%20break%20CTF%20escape%20map.png" alt="Prison Break CTF Map" width="600" />

## Overview

This CTF is designed as a linear progression challenge rather than a jeopardy-style board. Players begin locked in a prison cell, solve an initial escape challenge, and then branch into three concurrent paths. Each path contains three ordered challenges that must be solved in sequence.

The three mid-game paths are:

1. Control Room
2. Guard Room
3. Server Room

Players must complete all three paths before approaching the final exit. The final door requires a keycard, a pincode, and completion of one final challenge.

## Intended Progression

```text
Initial Cell Escape
        |
        +--> Control Room (3 linear challenges) --> Door controls unlocked
        |
        +--> Guard Room   (3 linear challenges) --> Keycard acquired
        |
        +--> Server Room  (3 linear challenges) --> Pincode recovered
        |
        --> Final Exit Challenge
```

## Design Goals

- Use narrative progression to make the CTF feel like an escape scenario rather than a disconnected puzzle set.
- Require players to combine different skill areas across web, crypto, host exploitation, enumeration, and privilege escalation.
- Keep the three main branches independent enough to pursue in parallel after the initial escape.
- Gate the final exit behind artifacts recovered from different branches.

## Proposed Challenge Count

- 1 initial challenge to escape the cell
- 3 challenges in the control room path
- 3 challenges in the guard room path
- 3 challenges in the server room path
- 1 final challenge at the exit

Total: 11 challenges

## Repository Structure

```text
assets/
initial-challenge/
control-room/
guard-room/
server-room/
final-exit/
```

Each room folder contains a room-level `README.md` plus one subfolder per planned challenge stage. Each challenge subfolder currently contains a placeholder `README.md` so the structure can be committed to Git.

## Path Summaries

### Initial Challenge

The player starts in a prison cell and must solve the opening challenge to get out. This should establish the theme, introduce the first clue chain, and teach the player how progression artifacts will be delivered.

### Control Room

This path represents access to the prison systems that control doors, CCTV, and other operational infrastructure. The expected outcome is the ability to open the doors leading toward the final exit.

### Guard Room

This path focuses on obtaining a physical access artifact: the keycard needed for the final door. It can lean into puzzle solving, physical-space narrative clues, or guarded storage.

### Server Room

This path focuses on breaking into prison systems to recover the pincode required at the final exit. It is the best fit for network enumeration, Linux exploitation, file traversal, or web-to-host compromise.

### Final Exit

The last challenge should verify that the player has fully completed the prison break. It should require the artifacts from the other paths and provide a strong narrative finish.

## Suggested Theme Mapping From Whiteboard Notes

- Initial challenge: phone smuggling, prison-cell clue discovery, SMS or communication-based unlock, or a small intro puzzle that yields the first step out of the cell
- Control room: CCTV or prison website access, Active Directory or Windows system access, then a system-level action to unlock doors
- Guard room: clue hunt and puzzle work, including crypto elements, ending with recovery of the keycard
- Server room: network scan, Linux compromise, traversal or web exploitation, ending with recovery of the pincode
- Final exit: use the keycard and pincode together, then solve one final gate challenge

## Build Notes

- These docs are intended for organizers and builders, not participants.
- Folder-level README files should describe intended progression, dependencies, and implementation notes without locking in the final flag format yet.
- Individual challenge folders are placeholders for later assets, services, Docker content, binaries, writeups, or deployment notes.
