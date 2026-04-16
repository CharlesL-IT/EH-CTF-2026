import random
import string
import time


CHARACTERS = string.ascii_lowercase + string.digits
PASSWORD_LENGTH = 15


def generate_password(seed):
    rng = random.Random(seed)
    return ''.join(rng.choice(CHARACTERS) for _ in range(PASSWORD_LENGTH))


def find_matching_seed(prefix, window):
    # the base seed is current time minus 3 seconds
    base_seed = int(time.time()) - 3
    offsets = [0]
    for step in range(1, window + 1):
        offsets.extend((-step, step))

    for offset in offsets:
        seed = base_seed + offset
        candidate = generate_password(seed)
        if candidate.startswith(prefix):
            return base_seed, seed, candidate

    return base_seed, None, None


def main():
    window = 3
    prefix = input("Enter the known 5-character prefix: ").strip().lower()
    if len(prefix) != 5 or any(ch not in CHARACTERS for ch in prefix):
        raise SystemExit("Prefix must be exactly 5 characters using lowercase letters and digits.")

    base_seed, matched_seed, candidate = find_matching_seed(prefix, window)

    print(f"Current Unix seed: {base_seed}")
    print(f"Scanning seeds from {base_seed - window} to {base_seed + window}")
    print(f"Looking for prefix: {prefix}")

    if matched_seed is None:
        print("No matching password found in the configured window.")
        return

    print(f"Matched seed: {matched_seed}")
    print(f"Recovered password: {candidate}")


if __name__ == "__main__":
    main()