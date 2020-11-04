import time


def gen1():
    for itm in range(10):
        yield f'gen1 {itm}'


def gen2():
    for itm in range(10):
        yield f'gen2 {itm}'


def master_gen():
    yield from gen1()
    yield from gen2()


for itm in master_gen():
    print(itm)
    time.sleep(1)
