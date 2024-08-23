import sqlite3
import config
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer, Column, Time, Date, BigInteger, VARCHAR

engine = create_engine(config.db_path)

class Base(DeclarativeBase):
    pass
class User(Base):
    __tablename__ = "discord_user"
    discord_id = Column(BigInteger, primary_key=True)
    discord_name = Column(String(50))
    answers: Mapped[List["NYT_scores"]] = relationship()
    channels: Mapped[List["RegisteredPlayers"]] = relationship()

    def __repr__(self):
        return(f"dg_id{self.discord_id}")

class NYT_scores(Base):
    __tablename__ = "nyt_scores"
    id = Column(Integer, primary_key=True, autoincrement=True)
    wordle_score = Column(Integer)
    connections_score = Column(Integer)
    strands_score = Column(Integer)
    mini_time = Column(Integer)
    date = Column(Date)
    #user_id: Mapped[int] = mapped_column(ForeignKey("discord_user.discord_id"))
    user_id = Column(BigInteger, ForeignKey("discord_user.discord_id"))
    daily_score = Column(Integer)

class RegisteredPlayers(Base):
    __tablename__ = "registered_players"
    id = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger)
    #user_id: Mapped[int] = mapped_column(ForeignKey("discord_user.discord_id"))
    user_id = Column(BigInteger, ForeignKey("discord_user.discord_id"))

class AutoChannels(Base):
    __tablename__ = "auto_message_channels"
    guild_id = Column(BigInteger, primary_key=True)
    channel_id = Column(BigInteger)

Base.metadata.create_all(engine)

