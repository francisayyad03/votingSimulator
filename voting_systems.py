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

from typing import List

from constants import (COL_RIDING, COL_VOTER, COL_RANK, COL_RANGE,
                       COL_APPROVAL, APPROVAL_TRUE, APPROVAL_FALSE,
                       SEPARATOR)

# In the following docstrings, 'VoteData' refers to a list of 5
# elements of the following types:
#
# at index COL_RIDING: int         (this is the riding number)
# at index COL_VOTER: int         (this is the voter number)
# at index COL_RANK: List[str]   (this is the rank ballot)
# at index COL_RANGE: List[int]   (this is the range ballot)
# at index COL_APPROVAL: List[bool]  (this is the approval ballot)

###############################################################################
# Task 0: Creating example data
###############################################################################

SAMPLE_DATA_1 = [[0, 1, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [1, 4, 2, 3],
                  [False, True, False, False]],
                 [1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
                  [False, False, True, True]],
                 [1, 3, ['GREEN', 'NDP', 'CPC', 'LIBERAL'], [1, 5, 1, 2],
                  [False, True, False, True]],
                 [1, 4, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [3, 0, 5, 2],
                  [True, False, True, True]]]
SAMPLE_ORDER_1 = ['CPC', 'GREEN', 'LIBERAL', 'NDP']


SAMPLE_DATA_2 = [[117, 12, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [2, 4, 1, 3],
                  [True, False, True, False]],
                 [117, 21, ['GREEN', 'LIBERAL', 'NDP', 'CPC'], [4, 5, 5, 5],
                  [True, True, True, True]],
                 [72, 12, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [0, 1, 1, 5],
                  [False, True, True, True]]]



###############################################################################
# Task 1: Data cleaning
###############################################################################

def clean_data(data: List[List[str]]) -> None:
    """Modify data so that the applicable string values are converted to
    their appropriate type, making data of type List['VoteType'].

    Pre: Each item in data is in the format
     at index COL_RIDING: a str that can be converted to an integer (riding)
     at index COL_VOTER: a str that can be converted to an integer (voter ID)
     at index COL_RANK: a SEPARATOR-separated non-empty string (rank ballot)
     at index COL_RANGE: a SEPARATOR-separated non-empty string of ints
                         (range ballot)
     at index COL_APPROVAL: a SEPARATOR-separated non-empty string of
                         APPROVAL_TRUE's and APPROVAL_FALSE's (approval ballot)

    >>> data = [['0', '1', 'NDP;Liberal;Green;CPC', '1;4;2;3', 'NO;YES;NO;NO']]
    >>> expected = [[0, 1, ['NDP', 'Liberal', 'Green', 'CPC'], [1, 4, 2, 3],
    ...             [False, True, False, False]]]
    >>> clean_data(data)
    >>> data == expected
    True

    >>> data = [['117', '12', 'LIBERAL;CPC;NDP;GREEN', '2;4;1;3',
    ...          'YES;NO;YES;NO'],
    ...          ['117', '21', 'GREEN;LIBERAL;NDP;CPC', '4;5;5;5',
    ...           'YES;YES;YES;YES'],
    ...          ['72', '12', 'NDP;LIBERAL;GREEN;CPC', '0;1;1;5',
    ...           'NO;YES;YES;YES']]
    >>> expected = [[117, 12, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [2,4,1,3],
    ...           [True, False, True, False]],
    ...          [117, 21, ['GREEN', 'LIBERAL', 'NDP', 'CPC'], [4,5,5,5],
    ...           [True, True, True, True]],
    ...          [72, 12, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [0,1,1,5],
    ...           [False, True, True, True]]]
    >>> clean_data(data)
    >>> data == expected
    True
    """

    for person in data:
        riding = int(person[COL_RIDING])
        voter = int(person[COL_VOTER])
        rank_vote = person[COL_RANK].split(';')
        range_vote = person[COL_RANGE].split(';')
        col_approval = person[COL_APPROVAL].split(';')
        approval = []
        range_v = []
        for item in col_approval:
            approval.append(item == APPROVAL_TRUE)
        for item in range_vote:
            range_v.append(int(item))
        data.insert(data.index(person),
                    [riding, voter, rank_vote, range_v, approval])
        data.remove(person)


###############################################################################
# Task 2: Data extraction
###############################################################################

def extract_column(data: List[list], column: int) -> list:
    """Return a list containing only the elements at index column for each
    sublist in data.

    Pre: each sublist of data has an item at index column.

    >>> extract_column([[1, 2, 3], [4, 5, 6]], 2)
    [3, 6]

    >>> extract_column([[1, 2, 3], [4, 5, 6], [7,8,9,10]], 1)
    [2, 5, 8]
    """

    col = []
    for row in data:
        col.append(row[column])
    return col


def extract_single_ballots(data: List['VoteData']) -> List[str]:
    """Return a list containing only the highest ranked candidate from
    each rank ballot in voting data data.

    Pre: data is a list of valid 'VoteData's
         The rank ballot is at index COL_RANK for each voter.

    >>> extract_single_ballots(SAMPLE_DATA_1)
    ['NDP', 'LIBERAL', 'GREEN', 'LIBERAL']

    >>> extract_single_ballots(SAMPLE_DATA_2)
    ['LIBERAL', 'GREEN', 'NDP']
    """
    single_ballot = []
    rank_lst = extract_column(data, COL_RANK)
    for item in rank_lst:
        single_ballot.append(item[0])
    return single_ballot

def get_votes_in_riding(data: List['VoteData'],
                        riding: int) -> List['VoteData']:
    """Return a list containing only voting data for riding riding from
    voting data data.

    Pre: data is a list of valid 'VoteData's

    >>> expected = [[1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
    ...              [False, False, True, True]],
    ...             [1, 3, ['GREEN', 'NDP', 'CPC', 'LIBERAL'], [1, 5, 1, 2],
    ...              [False, True, False, True]],
    ...             [1, 4, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [3, 0, 5, 2],
    ...              [True, False, True, True]]]
    >>> get_votes_in_riding(SAMPLE_DATA_1, 1) == expected
    True

    >>> expected2 = [[117, 12, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [2,4,1,3],
    ...              [True, False, True, False]],
    ...             [117, 21, ['GREEN', 'LIBERAL', 'NDP', 'CPC'], [4,5,5,5],
    ...              [True, True, True, True]]]

    >>> get_votes_in_riding(SAMPLE_DATA_2, 117) == expected2
    True

    """
    riding_votes = []
    riding_lst = extract_column(data, COL_RIDING)
    count = 0
    while count < len(riding_lst):
        if riding_lst[count] == riding:
            riding_votes.append(data[count])
        count += 1
    return riding_votes





###############################################################################
# Task 3.1: Plurality Voting System
###############################################################################

def voting_plurality(single_ballots: List[str],
                     party_order: List[str]) -> List[int]:
    """Return the total number of ballots cast for each party in
    single-candidate ballots single_ballots, in the order specified in
    party_order.

    Pre: each item in single_ballots appears in party_order

    >>> voting_plurality(['GREEN', 'GREEN', 'NDP', 'GREEN', 'CPC'],
    ...                  SAMPLE_ORDER_1)
    [1, 3, 0, 1]

    >>> voting_plurality(['GREEN', 'GREEN', 'GREEN', 'GREEN', 'GREEN'],
    ...                  SAMPLE_ORDER_1)
    [0, 5, 0, 0]
    """

    votes = []
    for party in party_order:
        count = 0
        for ballot in single_ballots:
            if ballot == party:
                count += 1
        votes.append(count)

    return votes


###############################################################################
# Task 3.2: Approval Voting System
###############################################################################

# Note: even though the only thing we need from party_order in this
# function is its length, we still design all voting functions to
# receive party_order, for consistency and readability.
def voting_approval(approval_ballots: List[List[bool]],
                    party_order: List[str]) -> List[int]:
    """Return the total number of approvals for each party in approval
    ballots approval_ballots, in the order specified in party_order.

    Pre: len of each sublist of approval_ballots is len(party_order)
         the approvals in each ballot are specified in the order of party_order

    >>> voting_approval([[True, True, False, False],
    ...                  [False, False, False, True],
    ...                  [False, True, False, False]], SAMPLE_ORDER_1)
    [1, 2, 0, 1]

    >>> voting_approval([[False, False, False, False],
    ...                  [True, False, True, True],
    ...                  [False, True, True, False]], SAMPLE_ORDER_1)
    [1, 1, 2, 1]
    """


    votes = []
    count = 0
    while count < len(party_order):
        count2 = 0
        data2 = extract_column(approval_ballots, count)
        for item in data2:
            if item:
                count2 += 1
        votes.append(count2)
        count += 1
    return votes



###############################################################################
# Task 3.3: Range Voting System
###############################################################################

def voting_range(range_ballots: List[List[int]],
                 party_order: List[str]) -> List[int]:
    """Return the total score for each party in range ballots
    range_ballots, in the order specified in party_order.

    Pre: len of each sublist of range_ballots is len(party_order)
         the scores in each ballot are specified in the order of party_order

    >>> voting_range([[1, 3, 4, 5], [5, 5, 1, 2], [1, 4, 1, 1]],
    ...              SAMPLE_ORDER_1)
    [7, 12, 6, 8]

    >>> voting_range([[1, 2, 3, 4], [3, 2, 1, 0], [5, 4, 3, 1]],
    ...              SAMPLE_ORDER_1)
    [9, 8, 7, 5]
    """

    votes = []
    count = 0
    while count < len(party_order):
        total = 0
        data2 = extract_column(range_ballots, count)
        for item in data2:
            total += item
        votes.append(total)
        count += 1
    return votes


###############################################################################
# Task 3.4: Borda Count Voting System
###############################################################################

def voting_borda(rank_ballots: List[List[str]],
                 party_order: List[str]) -> List[int]:
    """Return the Borda count for each party in rank ballots rank_ballots,
    in the order specified in party_order.

    Pre: each ballot contains all and only elements of party_order

    >>> voting_borda([['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...               ['CPC', 'LIBERAL', 'GREEN', 'NDP'],
    ...               ['LIBERAL', 'NDP', 'GREEN', 'CPC']], SAMPLE_ORDER_1)
    [4, 4, 8, 2]

    >>> voting_borda([['CPC', 'GREEN', 'LIBERAL', 'NDP'],
    ...               ['CPC', 'LIBERAL', 'NDP', 'GREEN'],
    ...               ['LIBERAL', 'CPC', 'NDP', 'GREEN']], SAMPLE_ORDER_1)
    [8, 2, 6, 2]
    """

    lst = [0] * len(party_order)
    for index in range(len(party_order)):
        total = len(party_order) - (index + 1)
        col = extract_column(rank_ballots, index)
        for vote in col:
            lst[party_order.index(vote)] += total

    return lst
###############################################################################
# Task 3.5: Instant Run-off Voting System
###############################################################################

def remove_party(rank_ballots: List[List[str]], party_to_remove: str) -> None:
    """Change rank ballots rank_ballots by removing the party
    party_to_remove from each ballot.

    Pre: party_to_remove is in all of the ballots in rank_ballots.

    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
    >>> remove_party(ballots, 'NDP')
    >>> ballots == [['LIBERAL', 'GREEN', 'CPC'],
    ...             ['CPC', 'LIBERAL', 'GREEN'],
    ...             ['CPC', 'GREEN', 'LIBERAL']]
    True


    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'LIBERAL', 'GREEN', 'NDP'],
    ...            ['LIBERAL', 'GREEN', 'NDP', 'CPC']]
    >>> remove_party(ballots, 'NDP')
    >>> ballots == [['LIBERAL', 'GREEN', 'CPC'],
    ...             ['CPC', 'LIBERAL', 'GREEN'],
    ...             ['LIBERAL', 'GREEN', 'CPC']]
    True


    """

    for person in rank_ballots:
        for vote in person:
            if vote == party_to_remove:
                person = person.remove(party_to_remove)


def get_lowest(party_tallies: List[int], party_order: List[str]) -> str:
    """Return the name of the party with the lowest number of votes in the
    list of vote counts per party party_tallies. In case of a tie,
    return the party that occurs earlier in party_order. Totals in
    party_tallies are ordered by party_order.

    Pre: len(party_tallies) == len(party_order) > 0

    >>> get_lowest([16, 100, 4, 200], SAMPLE_ORDER_1)
    'LIBERAL'
    >>> get_lowest([4, 10, 4, 20], SAMPLE_ORDER_1)
    'CPC'
    """

    return party_order[party_tallies.index(min(party_tallies))]


def get_winner(party_tallies: List[int], party_order: List[str]) -> str:
    """Return the name of the party with the highest number of votes in the
    list of vote counts per party party_tallies. In case of a tie,
    return the party that occurs earlier in party_order. Totals in
    party_tallies are ordered by party_order.

    Pre: len(party_tallies) == len(party_order) > 0

    >>> get_winner([16, 100, 4, 200], SAMPLE_ORDER_1)
    'NDP'

    >>> get_winner([16, 200, 200, 200], SAMPLE_ORDER_1)
    'GREEN'
    """

    return party_order[party_tallies.index(max(party_tallies))]


def voting_irv(rank_ballots: List[List[str]], party_order: List[str]) -> str:
    """Return the party which wins when IRV is performed on the list of
    rank ballots rank_ballots. Change rank_ballots and party_order as
    needed in IRV, removing parties that are eliminated in the
    process. Each ballot in rank_ballots is ordered by party_order.

    Pre: each ballot contains all and only elements of party_order
         len(rank_ballots) > 0

    >>> order = ['CPC', 'GREEN', 'LIBERAL', 'NDP']
    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
    >>> voting_irv(ballots, order)
    'NDP'
    >>> ballots == [['LIBERAL', 'NDP'],
    ...             ['NDP', 'LIBERAL'],
    ...             ['NDP', 'LIBERAL']]
    True
    >>> order
    ['LIBERAL', 'NDP']



    >>> order = ['CPC', 'GREEN', 'LIBERAL', 'NDP']
    >>> ballots = [['GREEN', 'LIBERAL', 'CPC', 'NDP'],
    ...            ['GREEN', 'CPC', 'LIBERAL', 'NDP'],
    ...            ['NDP', 'GREEN', 'CPC', 'LIBERAL']]
    >>> voting_irv(ballots, order)
    'GREEN'
    >>> ballots == [['GREEN', 'LIBERAL', 'CPC', 'NDP'],
    ...            ['GREEN', 'CPC', 'LIBERAL', 'NDP'],
    ...            ['NDP', 'GREEN', 'CPC', 'LIBERAL']]
    True
    >>> order
    ['CPC', 'GREEN', 'LIBERAL', 'NDP']


    """

    voting_majority = False
    min_majority = len(rank_ballots)//2
    while not voting_majority:
        data2_votes = voting_plurality(extract_column(rank_ballots, 0),
                                       party_order)

        if max(data2_votes) > min_majority or len(data2_votes) == 1:
            return get_winner(data2_votes, party_order)

        remover = get_lowest(data2_votes, party_order)
        remove_party(rank_ballots, remover)
        party_order.remove(remover)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
