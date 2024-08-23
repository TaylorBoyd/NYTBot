import datetime
from datetime import date
from typing import Optional
from helpers.ScoreHelper import ScoreHelper
def tester(month, day, year):
    x = date(year, month, day)
    print(x)


players = ScoreHelper.get_server_players(399680970581737492)

print(ScoreHelper.get_server_daily(players, datetime.date(2024, 8, 22)))