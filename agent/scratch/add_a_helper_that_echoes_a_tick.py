"""Scratch act from the brain coder. One file. Do not treat as merged."""

GOAL = 'add a helper that echoes a tick'
SYMBOLS = ['add', 'helper', 'that', 'echo', 'echoes', 'tick', 'ticks']

def act():
    return {'goal': GOAL, 'symbols': SYMBOLS}

if __name__ == '__main__':
    print(act())
