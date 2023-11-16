from datetime import datetime

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import app.keyboard as kb
from app.database.models import save_user, session, User, SleepRecord
from app.logic import get_time_from_location, get_coordinates_from_db

main_router = Router()
start_sleep_times = {}


@main_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    tg_id = message.from_user.id
    user = session.query(User).filter_by(tg_id=tg_id).first()
    if user:
        await message.answer('Добро пожаловать снова!')
    else:
        await message.answer(
            f"Привет, {message.from_user.full_name}! А вы знали, что качественный сон играет ключевую роль "
            f"в общем здоровье и благополучии человека? Он влияет на ваше физическое и эмоциональное состояние. "
            f"Если вам важно оставаться здоровым и энергичным, следите за вашим сном."
            f"\n\nПредлагаем вам использовать нашего бота для отслеживания статистики вашего сна. "
            f"Это поможет вам понять, насколько качественно вы отдыхаете и как это влияет на ваше здоровье."
            f"\n\nСпите вы 7-9 часов в день? Чувствуете ли вы себя отдохнувшими после сна? "
            f"Наш бот поможет вам вести учет и даст ценные рекомендации для улучшения вашего сна.",
        )
        await message.answer(
            'Кажется вы ещё не привязали ваш регион. Нужно будет поделится геолокацией. Не беспокойтесь,'
            'это делается всего один раз.',
            reply_markup=kb.create_location_keyboard())


@main_router.message(F.location)
async def handle_location(message: types.Message):
    tg_id = message.from_user.id
    lat = message.location.latitude
    lon = message.location.longitude
    await save_user(tg_id, lat, lon)
    await message.answer(f"Геолокация получена. Не беспокойтесь. Это абсолютно безопасно!",
                         reply_markup=types.ReplyKeyboardRemove())
    await message.answer(f"Супер! Теперь вы можете получать статистику о вашем сне."
                         f"Сейчас доступны несколько функций отслеживания сна:\n"
                         f"1 - Длительность сна (/hours_analize)",
                         reply_markup=types.ReplyKeyboardRemove())


@main_router.message(F.text == '/hours_analize')
async def analyze_command(message: types.Message) -> None:
    tg_id = message.from_user.id
    user = session.query(User).filter_by(tg_id=tg_id).first()
    try:
        lat, long = get_coordinates_from_db(tg_id)
        current_time = get_time_from_location(lat, long)
        new_sleep_record = SleepRecord(user_id=user.id, start_time=current_time)
        session.add(new_sleep_record)
        session.commit()
        await message.answer("Начало отслеживания сна.", reply_markup=kb.analyze_keyboard())
    except ValueError as e:
        await message.answer(f"Ошибка: {e}")


@main_router.callback_query(F.data == "wake_up")
async def send_random_value(callback: types.CallbackQuery):
    tg_id = callback.from_user.id
    user = session.query(User).filter_by(tg_id=tg_id).first()

    if user:
        sleep_record = session.query(SleepRecord).filter_by(user_id=user.id).order_by(
            SleepRecord.start_time.desc()).first()

        if sleep_record:
            start_time = sleep_record.start_time
            lat, long = get_coordinates_from_db(tg_id)
            end_time = get_time_from_location(lat, long)
            sleep_duration = end_time - start_time
            session.delete(sleep_record)
            session.commit()

            await callback.answer(f"Вы спали {sleep_duration.total_seconds() / 3600:.2f} часов.")
            await callback.message.edit_text(text=f"Вы спали {sleep_duration.total_seconds() / 3600:.2f} часов.")
        else:
            await callback.answer("Запись о начале сна не найдена.")
    else:
        await callback.answer("Пользователь не найден.")
