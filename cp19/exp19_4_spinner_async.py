# It is the job of OS scheduler to allocate CPU time to drive threads and processes. In contrast, coroutines
# are driven by an application-level event loop that manages a queue of pending coroutines, drives them one by one,
# monitors events triggered by I/O operations initiated by coroutines, and passes control back to the corresponding
# coroutine when each event happens. The event loop and the library coroutines and the user coroutines all execute in
# a single thread. Therefore, any time spent in a coroutine slows down the event loop - and all other coroutines.
import asyncio
import itertools
import time
from util import is_prime, time_it_decorator_async, is_prime_async


async def spin(msg: str) -> None:
    status = ''
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')
        try:
            await asyncio.sleep(0.3)
        except asyncio.CancelledError:
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')


async def slow() -> int:
    # time.sleep(3)     # blocks event loop thread
    # await asyncio.sleep(3)
    # is_prime(5_000_111_000_222_021)
    await is_prime_async(5_000_111_000_222_021)
    return 42


@time_it_decorator_async
async def supervisor() -> int:
    spinner = asyncio.create_task(spin('thinking!'))
    print(f'spinner object: {spinner}')
    # start_time = time.time()
    result = await slow()
    # end_time = time.time()
    spinner.cancel()
    # print(f'{end_time - start_time}')
    return result


def main() -> None:
    result, time_spent = asyncio.run(supervisor())
    print(f'Answer: {result} in {time_spent}')


if __name__ == '__main__':
    main()


# three ways of running a coroutine:

# asyncio.run(coro()) - Called from a regular function to drive a coroutine object which usually is the entry point for
# all the asynchronous code in the program (like supervisor in this example). This call blocks until the body of coro
# returns. The return value of the run() call is whatever the body of coro returns.

# asyncio.create_task(coro())
# Called from a coroutine to schedule another coroutine to be executed eventually. This call does not suspend the
# current coroutine. It returns a Task instance, an object that wraps the coroutine object and provides methods to
# control and query its state.

# await coro()
# Called from a coroutine to transfer control to the coroutine object returned by coro(). This suspends the current
# coroutine until the coro returns. The value of the 'await' expression is whatever body of coro returns.
