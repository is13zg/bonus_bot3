from create_bot import bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
import init_data
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

import config

import create_bot
import inspect

router = Router()


@router.message(Command(commands=["start", "Получить_бонус!"]))
async def command_start_handler(message: Message) -> None:
    try:
        # регистрируем пользователя в базе
        if not init_data.db.reg_user_exists(message.from_user.id):
            init_data.db.add_reg_user_to_db(message.from_user.id)

        # проверяем подписан ли на канал
        chat_member = await bot.get_chat_member(config.Chanel_Id, message.from_user.id)
        # проверяем находится ли пользователь вне канала
        if chat_member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED, ChatMemberStatus.RESTRICTED]:
            kb = [
                [
                    KeyboardButton(text="/Получить_бонус!"),
                ],
            ]
            keyboard = ReplyKeyboardMarkup(keyboard=kb)
            await message.answer(f"Вступите в канал для получения бонуса: {config.Url_to_join}",
                                 disable_web_page_preview=True,
                                 reply_markup=keyboard,
                                 parse_mode="HTML")
        else:
            await message.answer("Получи бонус", parse_mode="HTML")

        return
    except Exception as e:
        await create_bot.send_error_message(__name__, inspect.currentframe().f_code.co_name, e)
