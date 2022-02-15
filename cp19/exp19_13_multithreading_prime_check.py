import sys
from time import perf_counter
from typing import NamedTuple
from threading import Thread
from queue import SimpleQueue
from util import is_prime, NUMBERS


class PrimeResult(NamedTuple):
    n: int
    prime: bool
    elapsed: float


JobQueue = SimpleQueue[int]
ResultQueue = SimpleQueue[PrimeResult]


def check(n: int) -> PrimeResult:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)


def worker(jobs: JobQueue, results: ResultQueue) -> None:
    while n := jobs.get():
        results.put(check(n))
    results.put(PrimeResult(0, False, 0.0))


def start_jobs(
        threads: int, jobs: JobQueue, results: ResultQueue
) -> None:
    for n in NUMBERS:
        jobs.put(n)
    for _ in range(threads):
        thread = Thread(target=worker, args=(jobs, results))
        thread.start()
        jobs.put(0)


def report(threads: int, results: ResultQueue) -> int:
    checked = 0
    thread_done = 0
    while thread_done < threads:
        n, prime, elapsed = results.get()
        if n == 0:
            thread_done += 1
        else:
            checked += 1
            label = 'P' if prime else ' '
            print(f'{n:16}  {label}  {elapsed:9.6}s')
    return checked


def main() -> None:
    if len(sys.argv) < 2:
        number_of_threads = 12
    else:
        number_of_threads = int(sys.argv[1])
    print(f'Checking {len(NUMBERS)} numbers with {number_of_threads} threads')
    t0 = perf_counter()
    jobs: JobQueue = SimpleQueue()
    results: ResultQueue = SimpleQueue()
    start_jobs(number_of_threads, jobs, results)
    checked = report(number_of_threads, results)
    elapsed = perf_counter() - t0
    print(f'{checked} checks in {elapsed:.2f}s')


if __name__ == '__main__':
    main()