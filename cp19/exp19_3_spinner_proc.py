import asyncio
import itertools
import time
from util import is_prime, time_it_decorator
from multiprocessing import Process, Event  # multiprocessing.Event is a function, not an object like threading.Event
from multiprocessing import synchronize     # imported to write type hints


def spin(msg: str, done: Event) -> None:
    status = ''
    for char in itertools.cycle('-\|/'):
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        if done.wait(.03):
            break

    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')


def slow():
    is_prime(5_000_111_000_222_021)
    return 42


@time_it_decorator
def supervisor() -> int:
    done = Event()
    spinner = Process(target=spin, args=('thinking!', done))
    print(f'spinner object: {spinner}')
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result


def main():
    result, time_elapsed = supervisor()
    print(f'Answer: {result} in {time_elapsed}')


if __name__ == '__main__':
    main()

# NOTE: communication between processes that are isolated by the operating system and can't share Python objects.
# This means that objects crossing process boundaries have to be serialized and deserialized, which creates overhead.
# Since Python 3.8, there is a 'multiprocessing.shared_memory' package in the standard library, but it does not
# support instances of user-defined classes. Other than raw bytes, the package allows processes to share
# a ShareableList, a mutable sequence type that can hold a fixed number of items of types int, float, bool, None,
# as well as str and bytes up to 10MB per item.
