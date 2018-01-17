"""\
This is a module to solve the knapsack problem.
"""

import operator
from random import randint

def sort_items(items, side='value', desc=False, copy=True):
    fn = {
            'value': lambda x: x[0],
            'weight': lambda x: x[1]
            }
    if copy:
        items = items.copy()

    items.sort(key=fn[side], reverse=desc)
    return items

def sum_items(items, side='value'):
    idx = {
            'value': 0,
            'weight': 1
            }
    return sum(map(operator.itemgetter(idx[side]), items))

def main():
    weight_limit = 15
    items = [(randint(10, 100), randint(1, 5)) for _ in range(10)] # (value, weight)
    weight_sorted_items = sort_items(items, side='weight') # smallest weight first
    value_sorted_items = sort_items(items, side='value', desc=True) # highest value first

    print(sum_items(weight_sorted_items, 'weight'))
    print(sum_items(value_sorted_items, 'value'))

main()
