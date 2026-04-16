# Seed-cret Escape (Guard Room 2) - Walkthrough

## Challenge Summary
In this PrisonCTF challenge, players target a Fox River Penitentiary vault service that claims to generate a fresh 15-character password every round. The service leaks the first 5 characters of the password and asks the player to guess the full value.

The bug is that the password is not generated with a cryptographically secure source. Instead, the server reseeds Python's `random` module with the current Unix timestamp every time it creates a password:

```python
random.seed(int(time.time()))
characters = string.ascii_lowercase + string.digits
return ''.join(random.choice(characters) for _ in range(15))
```

Because the seed is just the current second, the password space collapses from "15 random characters" to "whatever values are produced by a very small window of nearby timestamps."

## Why the Challenge Is Breakable
The key problems in `Seed-cret_Escape.py` are:

1. `random.seed(int(time.time()))` uses a predictable seed.
2. The seed only changes once per second.
3. The service leaks the first 5 characters of the generated password.
4. The password is regenerated only when the prompt is produced, so the attacker can estimate the seed from connection time.

An attacker does not need to brute-force all possible 15-character passwords. They only need to:

1. Connect to the service.
2. Capture the leaked 5-character prefix.
3. Try a small window of timestamps around the current time.
4. Reproduce the same PRNG output locally.
5. Submit the matching 15-character password.

## Relevant Server Logic
From `Seed-cret_Escape.py`:

```python
def generate_password():
    random.seed(int(time.time()))
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(15))

...

password = generate_password()
hint = f"""The password is: {password[:5]}..........\nYour guess: """
conn.sendall(hint.encode())
```

This means the server tells us the first 5 characters of a password that was generated from a timestamp-based seed we can closely estimate.

## Solve Strategy
The intended solve is:

1. Record `int(time.time())` when connecting.
2. Read the server banner and extract the 5-character prefix.
3. Regenerate candidate passwords using the local time as the base seed.
4. Check a small window around that seed, such as `-3` to `+3` seconds.
5. Stop when a generated password starts with the leaked prefix.
6. Send the full candidate back to the server.

Because network delay is usually small, a tight window is enough.

## Solver Script
`Seed-cret_Escape_solution.py` automates the attack:

- Connects to the service on port `1337`
- Records the local connection-time seed
- Parses the leaked prefix with a regex
- Regenerates candidate passwords for nearby timestamps
- Submits the first full password whose prefix matches

The core logic is:

```python
def generate_password(seed):
    random.seed(seed)
    return ''.join(random.choice(CHARACTERS) for _ in range(15))

def find_best_candidate(base_seed, window, prefix):
    offsets = [0]
    for i in range(1, window + 1):
        offsets.extend((-i, i))

    for offset in offsets:
        seed = base_seed + offset
        candidate = generate_password(seed)
        if candidate.startswith(prefix):
            return seed, candidate
```

This works because the local script and the server use the same PRNG and the same seed format.

## Attack Flow
Example attack flow:

1. Connect to the server.
2. Receive something like `The password is: abc12..........`
3. Try seeds such as `current_time - 3` through `current_time + 3`.
4. Generate a 15-character password for each candidate seed.
5. Find the one that begins with `abc12`.
6. Send that full password to the service.
7. Receive the flag.

## Flag
The server returns:

```text
PrisonCTF{t1m3_15_0f_th3_3553nc3}
```

## Lesson
This challenge demonstrates a classic failure mode:

- Python's `random` module is not cryptographically secure.
- Seeding from the current time makes outputs predictable.
- Even a partial output leak can make recovery trivial.

For a secure design, the password should be generated with a cryptographic source such as `secrets.choice()` or `secrets.token_urlsafe()`, and the service should never reveal any part of the password.
