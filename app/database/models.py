from sqlalchemy import create_engine, Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine('sqlite:///user_data1.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)

    # Установка связи между User и SleepRecord
    sleep_records = relationship("SleepRecord", back_populates="user", cascade="all, delete-orphan")

class SleepRecord(Base):
    __tablename__ = 'sleep_records'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    start_time = Column(DateTime)

    # Установка связи между SleepRecord и User
    user = relationship("User", back_populates="sleep_records")


async def save_user(tg_id, latitude, longitude):
    new_user = User(tg_id=tg_id, latitude=latitude, longitude=longitude)
    session.add(new_user)
    session.commit()


async def async_main():
    Base.metadata.create_all(engine)
