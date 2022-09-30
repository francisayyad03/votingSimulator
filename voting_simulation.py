"""CSC108/A08: Fall 2021 -- Assignment 2: voting

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Sophia Huynh, Sadia Sharmin,
Elizabeth Patitsas, Anya Tafliovich.

"""

import copy
from typing import List, TextIO
import voting_systems as vs

from constants import COL_RIDING, COL_RANK, COL_RANGE, COL_APPROVAL


PLURALITY = 'P'
APPROVAL = 'A'
RANGE = 'R'
BORDA = 'B'
IRV = 'I'

QUIT = 'Q'
ALL = 'all'
MSG_INVALID = 'Invalid choice.'

SYSTEM_NAMES = {PLURALITY: 'Plurality',
                APPROVAL: 'Approval',
                RANGE: 'Range',
                BORDA: 'Borda',
                IRV: 'IRV',
                QUIT: 'Quit'}

SYSTEMS = {PLURALITY: (vs.voting_plurality, None),
           APPROVAL: (vs.voting_approval, COL_APPROVAL),
           RANGE: (vs.voting_range, COL_RANGE),
           BORDA: (vs.voting_borda, COL_RANK),
           IRV: (vs.voting_irv, COL_RANK)}


def read_data(datafile: TextIO) -> List['VoteData']:
    """Return the voting data from the file filename.
    Pre: filename is in a valid format and open for reading.
    """

    datafile.readline()  # skip header

    data = []
    for line in datafile:
        data.append(line.strip().split(','))
    return data


def _options_str(options: List[str]) -> str:
    """Create a string specifying selection of an element from options, by
    entering the first letter in the correspoding option.

    Pre: options is a list of non-empty strings

    >>> _options_str(['Alpha', 'Beta', 'Gamma'])
    '[A]lpha, [B]eta, [G]amma'
    >>> _options_str([])
    ''
    """

    result = ''
    for system in options:
        result += '[{}]{}, '.format(system[:1], system[1:])
    return result[:-2]  # strip the final ', '


def prompt_for_system() -> str:
    """Repeatedly prompt the user to select a voting system or to quit the
    simulation, until a valid option is entered. Return the selection.

    """

    prompt = '\nSelect a voting system or {} to quit: '.format(QUIT)
    options = SYSTEM_NAMES.keys()
    options_str = _options_str(SYSTEM_NAMES.values())
    message = '{}\n{}: '.format(prompt, options_str)

    answer = input(message).upper()
    while answer not in options:
        answer = input('{} {}'.format(MSG_INVALID, message)).upper()

    return answer


def prompt_for_riding(maximum: int) -> str:
    """Repeatedly prompt the user to enter ALL or a value between 0 and
    maximum inclusive, until a valid option is entered. Return the
    selection.

    """

    message = 'Enter "{}" or a number between 0 and {}, inclusive: '.format(
        ALL, maximum)
    answer = input(message).lower()

    while not (answer == ALL or
               answer.isdigit() and 0 <= int(answer) <= maximum):
        answer = input('{} {}'.format(MSG_INVALID, message)).upper()

    return answer


def print_header(header: str) -> None:
    """Print the header header."""

    print("\n{}\n{}".format(header, '=' * len(header)))


def print_results_list(result_list: List[int], party_order: List[str]) -> None:
    """Print a formatted message that contains data on the seats assigned
    to the parties in the order of party_order, from the list of
    voting results result_list.

    Pre: len(result_list) == len(party_order)
    """

    num_parties = len(party_order)
    for index in range(num_parties):
        party_formatted = '{}:'.format(party_order[index]).ljust(10)
        print("{}\t{}".format(party_formatted, result_list[index]))


def one_riding(data: 'VoteData', system: str, riding: int,
               party_order: List[str]) -> None:
    """Simulate an election for riding number riding using the voting
    system system, voting data data, and party ordering parter_order.

    Pre: system is one of SYSTEMS.keys()
         riding is valid for data.
    """

    riding_votes = vs.get_votes_in_riding(data, riding)

    if system == PLURALITY:
        ballots = vs.extract_single_ballots(riding_votes)
    else:
        ballots = vs.extract_column(riding_votes, SYSTEMS[system][1])

    # IRV changes its input: work on a copy.
    # IRV produces a single winner, not full results.
    if system == IRV:
        winner = SYSTEMS[system][0](copy.deepcopy(ballots),
                                    copy.deepcopy(party_order))
        return (winner, None)

    # not IRV
    full_results = SYSTEMS[system][0](ballots, party_order)
    winner = vs.get_winner(full_results, party_order)
    return (winner, full_results)


def all_ridings(data: 'VoteData', system: str, num_ridings: int,
                party_order: List[str]) -> None:
    """Simulate an election all num_ridings ridings using the voting
    system system and voting data data.

    Pre: system is one of SYSTEMS.keys()
         num_ridings is valid for data.
    """

    seats = [0] * len(party_order)
    for riding in range(num_ridings):
        winner, _ = one_riding(data, system, riding, party_order)
        seats[party_order.index(winner)] += 1

    return seats


def simulate_elections(data: List['VoteData'], party_order: List[str]) -> None:
    """Run the voting simulations on voting data data based on user input.
    """

    print('Starting voting simulation.')
    print('Reading and cleaning input data.')

    vs.clean_data(data)

    system = prompt_for_system()
    while system != QUIT:

        print('Running voting system {}.'.format(SYSTEM_NAMES[system]))

        num_ridings = len(set(vs.extract_column(data, COL_RIDING)))
        riding = prompt_for_riding(num_ridings - 1)

        if riding != ALL:
            riding = int(riding)
            (winner, results) = one_riding(data, system, riding, party_order)
            print_header('Results for riding {}'.format(riding))
            print('The seat is won by the {} candidate.'.format(winner))
            if system != IRV:
                print_results_list(results, party_order)
        else:
            results = all_ridings(data, system, num_ridings, party_order)
            print_header('Results for all Ridings')
            print_results_list(results, party_order)

        system = prompt_for_system()

    print('End of voting simulation')


if __name__ == '__main__':

    import doctest
    doctest.testmod()

    PARTY_ORDER = ['CPC', 'GREEN', 'LIBERAL', 'NDP']
    CSV_FILENAME = 'sample_votes.csv'

    with open(CSV_FILENAME) as DATAFILE:
        VOTING_DATA = read_data(DATAFILE)

    simulate_elections(VOTING_DATA, PARTY_ORDER)
