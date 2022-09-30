# UWU What's this!?
# OWOWOWO!!!

from typing import Any
import traceback
import copy
import voting_systems as v

# Check if equal
def eq(val, exp, p = True) -> int:
    if val != exp:
        if not p:
            print('Variable check failed!')
        print('Expected:', exp)
        print('Got:', val)
        return 1
    return 0

# Print name of func being tested
def t(func):
    print('========================')
    print('Testing function:', func.__name__)

# Test function with error handling and result checking
def test(func, args, expected, p = True) -> int:
    if p:
        t(func)
    result = False
    try:
        copy_ = copy.deepcopy(args) if isinstance(args, list) else args
        result = func(*args) == expected

        if result:
            print('Test passed!')
        else:
            print('Test failed!')
            args = copy.deepcopy(copy_) if isinstance(copy_, list) else args

            eq(func(*args), expected)
            print('Arguments:\n' + str(copy_)[1:-1])           
    except Exception as e:
        print('Error thrown!')
        print('Arguments:\n' + str(copy_)[1:-1])
        print('Error:\n' + str(e))

    return 0 if result else 1
        
def run_tests():
    errors = 0
    
    # irv tie
    bal = [['1', '11', '111'], ['11', '111', '1']]
    order = ['1', '11', '111']
    t(v.voting_irv)
    errors += test(v.voting_irv, [bal, order], '11', False)
    errors += eq(bal, [['11'], ['11']], False)
    errors += eq(order, ['11'], False)
    
    # get_winner tie
    errors += test(v.get_winner, [[0, 0, 0], ['1', '11', '111']], '1')
    
    # get_winner 1 len
    errors += test(v.get_winner, [[0], ['1']], '1')
    
    # get_lowest tie
    errors += test(v.get_lowest, [[0, 0, 0], ['1', '11', '111']], '1')
    
    # get_lowest negative
    errors += test(v.get_lowest, [[-10, -9999999, 0], ['1', '11', '111']], '11')
    
    # remove_party empty
    bal = [['1'], ['1']]
    t(v.remove_party)
    errors += test(v.remove_party, [bal, '1'], None, False)
    errors += eq(bal, [[],[]])
    
    # voting_borda len 1
    errors += test(v.voting_borda, [[['1']], ['1']], [0])
    
    # voting_borda len 0
    errors += test(v.voting_borda, [[], []], [])
    
    # voting_range len 1
    errors += test(v.voting_range, [[[2], [4]], ['A']], [6])
    
    # voting_range len 0
    errors += test(v.voting_range, [[[], [], []], []], [])
    
    # voting_approval len 0
    errors += test(v.voting_approval, [[[], [], []], []], [])
    
    # voting_plurality len 0
    errors += test(v.voting_plurality, [[], []], [])
    
    # get_votes_in_riding len 0
    errors += test(v.get_votes_in_riding, [[], 2], [])
    
    # extract_single_ballots len 0
    errors += test(v.extract_single_ballots, [[]], [])
    
    # extract_column varied length, diff types
    lst = [[2, 3, 4],
           ['2', '4', '6', 7],
           [False, False, True, True, False],
           [4, [2, 3], [4, 6]]]
    errors += test(v.extract_column, [lst, 2], [4, '6', True, [4, 6]])
    
    # clean_data negative
    lst = [['-1444', '-5', '1;2', '2;1', 'NO;YES']]
    t(v.clean_data)
    errors += test(v.clean_data, [lst], None, False)
    errors += eq(lst, [[-1444, -5, ['1', '2'], [2, 1], [False, True]]])
    
    # clean_data len 0
    lst = []
    t(v.clean_data)
    errors += test(v.clean_data, [lst], None, False)
    errors += eq(lst, [])

    print('========================')
    print('Tests failed:', errors)

run_tests()