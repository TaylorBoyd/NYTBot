import discord
from discord.ext import commands
from sqlalchemy import create_engine, select, and_, join
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from database_init import User, RegisteredPlayers, NYT_scores
import datetime
from datetime import date, datetime, timedelta
import config

class ScoreHelper:
    def __init__(self):
        pass

    @staticmethod
    def generate_score(wordle: int, connections: int, strands: int, minutes: int) -> int:
        wordle_score = (7 - wordle)
        connections_score = (4 + connections)
        strands_score = (8 - strands)
        if minutes > 9:
            mini_score = 0
        else:
            mini_score = (8 - minutes)

        return (wordle_score + connections_score + strands_score + mini_score)


    @staticmethod
    def get_server_players(guild_id: int) -> list:
        stmt = select(RegisteredPlayers).where(RegisteredPlayers.guild_id == guild_id)
        engine = create_engine(config.db_path)
        player_list = []
        with Session(engine) as session:
            for user in session.scalars(stmt).all():
                player_list.append(user.user_id)
        return(player_list)

    @staticmethod
    def get_server_daily(player_list: list, date: date) -> list:
        '''
        Parameters
        ----------
            player_list: list
                Takes in a list of player discord_id's
            date:
                Should be in YYYY/MM/DD format as a datetime.date object
            returns a list of players and their daily scores sorted in order
        '''
        score_list = []
        engine = create_engine(config.db_path)
        with Session(engine) as session:
            for player in player_list:
                stmt = select(NYT_scores).where(and_(NYT_scores.user_id == player), (NYT_scores.date == date))
                for score in session.execute(stmt):
                    score_list.append([player, score[0].daily_score, score[0].mini_time])
        score_list.sort(key=lambda x: x[2])
        score_list.sort(key=lambda x: (x[1]), reverse=True)
        return(score_list)

