import logging
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F, Bot, Router

from dotenv import load_dotenv
import os
import g4f.Provider


import app.keyboard as kb

load_dotenv()
router = Router()
conversation_history = {}

async def start_context_data(user_id):
    conversation_history[user_id].append({"role": "user", "content": "пиши на русском языке"})
    conversation_history[user_id].append({"role": "user", "content": "пиши только по русски"})
    conversation_history[user_id].append({"role": "user", "content": "не отвечай на английском"})
    

@router.message(CommandStart())
@router.message(F.text == 'На главную')
async def cmd_start(message: Message, bot: Bot):
    me = await bot.get_me()
    await message.reply(f"Привет!\nЯ - ChatGPT", reply_markup=kb.main)
    

def trim_history(history, max_length=4096):
    current_length = sum(len(message["content"]) for message in history)
    while history and current_length > max_length:
        removed_message = history.pop(0)
        current_length -= len(removed_message["content"])
    return history


@router.message(Command('clear'))
async def process_clear_command(message: Message):
    user_id = message.from_user.id
    conversation_history[user_id] = []        
    start_context_data(user_id)
    logging.info(f"{user_id} - История диалога очищена.")
    await message.reply("История диалога очищена.")

async def chat(user_id, user_input):
    if user_id not in conversation_history:
        conversation_history[user_id] = []
        start_context_data(user_id)

    conversation_history[user_id].append({"role": "user", "content": user_input})
    conversation_history[user_id] = trim_history(conversation_history[user_id])

    chat_history = conversation_history[user_id]

    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            #model='gpt-4-0314',
            messages=chat_history,
            #provider=g4f.Provider.Blackbox, #работает, но кривой
            #provider=g4f.Provider.GeminiProChat, #работает, но кривой, чуть менее кривой (ограничение по символам)
            #provider=g4f.Provider.PerplexityLabs, #пока лучше других
            #provider=g4f.Provider.You, #работал, но сейчас не хочет
            provider=g4f.Provider.PerplexityLabs, 
            api_key=os.getenv('openai_token_new')
        )
        chat_gpt_response = response
        conversation_history[user_id].append({"role": "assistant", "content": chat_gpt_response})
    except Exception as e:        
        logging.info(f"ERROR RESPONSE ### {str(e)}")
        chat_gpt_response = "Извините, произошла ошибка. " + str(e)

    return chat_gpt_response


@router.message()
async def any_reply(message: Message, bot: Bot):
    user_id = message.from_user.id
    user_input = message.text
    logging.info(f"Response from {user_id} : {user_input}")
    await message.answer(await chat(user_id, user_input))
    