import re
import asyncio
import logging
from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext

from bot.data_config.config import ADMIN_GROUP_ID
from bot.keyboards.default import phone_request_keyboard, no_contact_markup

# Регулярное выражение для проверки номера телефона
phone_pattern = re.compile(r'^\+\d\s\d{3}\s\d{3}\s\d{2}\s\d{2}$')

class Form(StatesGroup):
    full_name = State()
    company = State()
    phone = State()
    shop_number = State()
    question = State()


async def start_command(message: types.Message):
    await Form.full_name.set()
    await message.bot.send_message(message.chat.id,"Здравствуйте! Введите, пожалуйста, ваше ФИО:")

async def process_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await Form.next()
    await message.bot.send_message(message.chat.id,"Хорошо, теперь введите, пожалуйста, вашу компанию:")

async def process_company(message: types.Message, state: FSMContext):
    await state.update_data(company=message.text)
    await Form.next()
    await message.bot.send_message(message.chat.id,"Отлично,теперь используйте кнопку для отправки номера телефона или введите номер в формате +X (XXX) XXX-XX-XX, чтобы наш специалист смог связаться с Вами:", reply_markup=phone_request_keyboard())
    
async def process_phone(message: types.Message, state: FSMContext):
    # if message.contact:
    #     await state.update_data(phone=message.contact.phone_number)
    #     await Form.next()
    #     await message.bot.send_message(message.chat.id,"Прекрасно, теперь введите, пожалуйста, номер проблемного магазина:", reply_markup=types.ReplyKeyboardRemove())
    if phone_pattern.match(message.text):
        await state.update_data(phone=message.text)
        await Form.next()
        await message.bot.send_message(message.chat.id,"Прекрасно, теперь введите, пожалуйста, номер проблемного магазина:", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.bot.send_message(message.chat.id,"Пожалуйста, используйте кнопку для отправки номера телефона или введите номер в формате +X (XXX) XXX XX XX.", reply_markup=phone_request_keyboard())

async def process_shop_number(message: types.Message, state: FSMContext):
    await state.update_data(shop_number=message.text)
    await Form.next()
    await message.bot.send_message(message.chat.id, "Замечательно! Теперь, пожалуйста, опишите ваш вопрос к специалисту:", reply_markup=types.ReplyKeyboardRemove())
        
async def process_question(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_data['question'] = message.text

    group_message  = (
        f"Новый запрос от: {user_data['full_name']}\n"
        f"Компания: {user_data['company']}\n"
        f"Телефон: {user_data['phone']}\n"
        f"Номер магазина: {user_data['shop_number']}\n"
        f"Вопрос: {user_data['question']}"
    )

    sent_message = await message.bot.send_message(message.chat.id,"Ваше обращение принято, в ближайшее время с вами свяжутся.")
    
    try:
        sent_admin_message = await message.bot.send_message(chat_id=ADMIN_GROUP_ID, text=group_message )
    except Exception as e:
        await logging.error(f"Ошибка: {e}")

    await state.finish()

    # Ожидание 5 минут и отправка кнопки, если никто не связался
    await asyncio.sleep(30)
    await sent_message.bot.send_message(message.chat.id,"Если с Вами никто не связался, нажмите кнопку ниже:", reply_markup=no_contact_markup(sent_admin_message.message_id))
    
async def no_contact(callback_query: types.CallbackQuery):
    _, admin_message_id = callback_query.data.split(":")
    await callback_query.bot.send_message(chat_id=ADMIN_GROUP_ID, text=f"Пользователь сообщает, что с ним никто не связался.", reply_to_message_id=int(admin_message_id))
    await callback_query.message.edit_text("Ваше сообщение отправлено специалистам, ожидайте пожалуйста, скоро с вами свяжутся.")

def register_handlers(dp: Dispatcher, bot: Bot):
    dp.register_message_handler(start_command, commands=['start', 'new_appeal'], state="*")
    dp.register_message_handler(process_full_name, state=Form.full_name)
    dp.register_message_handler(process_company, state=Form.company)
    dp.register_message_handler(process_phone, content_types=['contact', 'text'], state=Form.phone)
    dp.register_message_handler(process_shop_number, state=Form.shop_number)
    dp.register_message_handler(process_question, state=Form.question)
    dp.register_callback_query_handler(no_contact, lambda c: c.data.startswith("no_contact"))