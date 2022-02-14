# spin nad slow functions
import itertools
import time
from util import is_prime, time_it_decorator
from threading import Thread, Event


def spin(msg: str, done: Event) -> None:
    status = ''
    # the trick for text-mode animation: move the cursor back to the start of
    # the line with the carriage return ASCII control character '\r'
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        if done.wait(0.3):
            break

    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')


def slow() -> int:
    # time.sleep(3)   # blocks the calling thread but releases the GIL
    is_prime(5_000_111_000_222_021)
    return 42


@time_it_decorator
def supervisor() -> int:
    done = Event()
    # to create a new Thread, provide a function as the 'target' keyword argument, and positional
    # arguments to the target as a tuple passed via 'args'
    spinner = Thread(target=spin, args=('thinking!', done))
    # prints <Thread(Thread-1 (spin), initial)>, 'initial' means thread has not started yet
    print(f'spinner object: {spinner}')
    spinner.start()
    result = slow() # blocks the main thread, but releases the GIL
    done.set()
    spinner.join()
    return result


def main() -> None:
    result, time_elapsed = supervisor()
    print(f'Answer: {result} in {time_elapsed}')


if __name__ == '__main__':
    main()


