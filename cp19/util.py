import asyncio
import math
import time

NUMBERS = [
    2,
    142702110479723,
    299593572317531,
    3333333333333301,
    3333333333333333,
    3333335652092209,
    4444444444444423,
    4444444444444444,
    4444444488888889,
    5555553133149889,
    5555555555555503,
    5555555555555555,
    6666666666666666,
    6666666666666719,
    6666667141414921,
    7777777536340681,
    7777777777777753,
    7777777777777777,
    9999999999999917,
    9999999999999999
]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    root = math.isqrt(n)
    for i in range(3, root + 1, 2):
        if n % i == 0:
            return False
    return True


async def is_prime_async(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    root = math.isqrt(n)
    for i in range(3, root + 1, 2):
        if n % i == 0:
            return False
        if i % 100_000 == 1:
            await asyncio.sleep(0)
    return True


def time_it_decorator(func):
    def wrapper():
        start_time = time.time()
        result = func()
        end_time = time.time()
        time_elapsed = end_time - start_time
        return result, time_elapsed
    return wrapper


def time_it_decorator_async(func):
    async def wrapper():
        start_time = time.time()
        result = await func()
        end_time = time.time()
        time_elapsed = end_time - start_time
        return result, time_elapsed
    return wrapper


if __name__ == '__main__':
    @time_it_decorator
    def time_it_test():
        result = is_prime(5_000_111_000_222_021)
        return result

    result, time_spent = time_it_test()
    print(f'{result} in {time_spent}')
