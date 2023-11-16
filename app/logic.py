from aiogram import types
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

from app.database.models import session, User


def get_coordinates_from_db(tg_id: int) -> ():
    user = session.query(User).filter_by(tg_id=tg_id).first()
    if user:
        latitude = user.latitude
        longitude = user.longitude
        return latitude, longitude

    else:
        raise ValueError("Пользователь с указанным Telegram ID не найден в базе данных")


def get_time_from_location(lat, lon):
    tz = TimezoneFinder()
    timezone_str = tz.timezone_at(lng=lon, lat=lat)
    if timezone_str:
        timezone = pytz.timezone(timezone_str)
        time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
        return datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    else:
        return "Часовой пояс не найден."
