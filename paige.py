def combos(L, n):
    if n == 0:
        yield tuple()
    else:
        for x in L:
            for sub_combo in combos(L, n-1):
                answer = (x,) + sub_combo
                if len(answer) == len(set(answer)):
                    yield (x,) + sub_combo

def gen_scenarios():
    for colors in combos(('red', 'green', 'blue', 'white', 'yellow'), 5):
        if not colors.index('green') == colors.index('white') - 1:
            continue
        for nats in combos(('dane', 'swede', 'brit', 'norwegian', 'german'), 5):
            if (abs(nats.index('norwegian') - colors.index('blue')) == 1) and\
               (nats.index('brit') == colors.index('red')) and\
               (nats.index('norwegian') == 0):
                pass
            else:
                continue
            for drinks in combos(('tea', 'milk', 'beer', 'water', 'coffee'), 5):
                if colors.index('green') == drinks.index('coffee') and\
                   nats.index('dane') == drinks.index('tea'):
                    pass
                else:
                    continue
                for smokes in combos(('dunhill', 'blue master', 'prince', 'blends', 'pall mall'), 5):
                    if smokes.index('dunhill') == colors.index('yellow'):
                        pass
                    else:
                        continue
                    for pets in (('dog', 'cat', 'horse', 'fish', 'bird'), 5):
                        yield colors, nats, drinks, smokes, pets

for scenario in gen_scenarios():
    print scenario
