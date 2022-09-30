"""A simple checker for functions in voting_systems.py.

Copyright (c) 2021 Anya Tafliovich.
"""

from typing import Any, Dict
import unittest
import voting_systems as vs
import checker

MODULENAME = 'voting_systems'
PYTA_CONFIG = 'pyta/a2_pyta.txt'
TARGET_LEN = 79
SEP = '='

CONSTANTS = {
    'COL_RIDING': 0,
    'COL_VOTER': 1,
    'COL_RANK': 2,
    'COL_RANGE': 3,
    'COL_APPROVAL': 4,
    'SEPARATOR': ';',
    'APPROVAL_TRUE': 'YES',
    'APPROVAL_FALSE': 'NO'
}


class CheckTest(unittest.TestCase):
    """A simple checker (NOT a full tester!) for assignment functions."""

    def setUp(self):
        """Init sample data."""

        self.data = [
            [0, 1, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [1, 4, 2, 3],
             [False, True, False, False]],
            [1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
             [False, False, True, True]],
            [1, 3, ['GREEN', 'NDP', 'CPC', 'LIBERAL'], [1, 5, 1, 2],
             [False, True, False, True]],
            [1, 4, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [3, 0, 5, 2],
             [True, False, True, True]]]
        self.order = ['CPC', 'GREEN', 'LIBERAL', 'NDP']

    def test_clean_data(self) -> None:
        """A simple check for clean_data."""

        self._check_simple_type(
            vs.clean_data,
            [[['0', '1', 'NDP;Liberal;Green;CPC', '1;4;2;3', 'NO;YES;NO;NO']]],
            type(None))

    def test_extract_column(self) -> None:
        """A simple check for extract_column."""

        self._check_list_type(vs.extract_column,
                              [[[1, 2, 3], [4, 5, 6]], 2],
                              int)

    def test_extract_single_ballots(self) -> None:
        """A simple check for extract_single_ballots."""

        self._check_list_type(vs.extract_single_ballots,
                              [self.data],
                              str)

    def test_get_votes_in_riding(self) -> None:
        """A simple check for get_votes_in_riding."""

        self._check_list_type(vs.get_votes_in_riding,
                              [self.data, 1],
                              list)

    def test_voting_plurality(self) -> None:
        """A simple check for voting_plurality."""

        ballots = ['GREEN', 'GREEN', 'NDP', 'GREEN', 'CPC']
        self._check_list_type(vs.voting_plurality,
                              [ballots, self.order],
                              int)

    def test_voting_approval(self) -> None:
        """A simple check for voting_approval."""

        ballots = [[True, True, False, False],
                   [False, False, False, True],
                   [False, True, False, False]]
        self._check_list_type(vs.voting_approval,
                              [ballots, self.order],
                              int)

    def test_voting_borda(self) -> None:
        """A simple check for voting_borda."""

        ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
                   ['CPC', 'LIBERAL', 'GREEN', 'NDP'],
                   ['LIBERAL', 'NDP', 'GREEN', 'CPC']]
        self._check_list_type(vs.voting_borda,
                              [ballots, self.order],
                              int)

    def test_remove_party(self) -> None:
        """A simple check for remove_party."""

        ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
                   ['CPC', 'LIBERAL', 'GREEN', 'NDP'],
                   ['LIBERAL', 'NDP', 'GREEN', 'CPC']]
        self._check_simple_type(vs.remove_party,
                                [ballots, 'GREEN'],
                                type(None))

    def test_get_lowest(self) -> None:
        """A simple check for get_lowest."""

        self._check_simple_type(vs.get_lowest,
                                [[1, 2, 3], ['a', 'b', 'c']],
                                str)

    def test_voting_irv(self) -> None:
        """A simple check for voting_irv."""

        ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
                   ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
                   ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
        self._check_simple_type(vs.voting_irv,
                                [ballots, self.order],
                                str)

    def test_get_winner(self) -> None:
        """A simple check for get_winner."""

        self._check_simple_type(vs.get_winner,
                                [[1, 3, 2, 4], self.order],
                                str)

    def test_check_constants(self) -> None:
        """Check that values of constants are not changed."""

        print('\nChecking that constants refer to their original values')
        self._check_constants(CONSTANTS, vs)
        print('  check complete')

    def _check_simple_type(self, func: callable, args: list,
                           expected: type) -> None:
        """Check that func called with arguments args returns a value of type
        expected. Display the progress and the result of the check.

        """

        print('\nChecking {}...'.format(func.__name__))
        result = checker.type_check_simple(func, args, expected)
        self.assertTrue(result[0], result[1])
        print('  check complete')

    def _check_list_type(self, func: callable, args: list,
                         of_type: type) -> None:
        """Check that func called with arguments args returns a List of values
        of value of type of_type. Display the progress and the result
        of the check.

        """

        print('\nChecking {}...'.format(func.__name__))
        result = checker.returns_list_of(func, args, of_type)
        self.assertTrue(result[0], result[1])
        print('  check complete')

    def _check_constants(self, name2value: Dict[str, Any], mod: Any) -> None:
        """Check that, for each (name, value) pair in name2value, the value of
        a variable named name in module mod is value.

        """

        for name, expected in name2value.items():
            actual = getattr(mod, name)
            msg = 'The value of {} should be {} but is {}.'.format(
                name, expected, actual)
            self.assertEqual(expected, actual, msg)


checker.ensure_no_io(MODULENAME)

print(''.center(TARGET_LEN, SEP))
print(' Start: checking coding style '.center(TARGET_LEN, SEP))
checker.run_pyta(MODULENAME + '.py', PYTA_CONFIG)
print(' End checking coding style '.center(TARGET_LEN, SEP))

print(' Start: checking type contracts '.center(TARGET_LEN, SEP))
unittest.main(exit=False)
print(' End checking type contracts '.center(TARGET_LEN, SEP))

print('\nScroll up to see ALL RESULTS:')
print('  - checking coding style')
print('  - checking type contract\n')
