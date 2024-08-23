def daily_score_helper(wordle: int, connections: int, strands: int, minutes: int) -> int:
    wordle_score = (7-wordle)
    connections_score = (4+connections)
    strands_score = (8-strands)
    if minutes > 9:
        mini_score = 0
    else:
        mini_score = (8-minutes)

    return(wordle_score+connections_score+strands_score+mini_score)


