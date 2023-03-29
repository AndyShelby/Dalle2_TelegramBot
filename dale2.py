from pathlib import Path
from base64 import b64decode
import openai
from aiogram import Dispatcher, Bot, executor, types
import asyncio

openai.api_key = ("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")
BOT_TOKEN ="5938378024:AAHj52bQYnSMKjXYIgPVhxq86B46I_Z2I84"

loop = asyncio.new_event_loop()
bot  = Bot(BOT_TOKEN, parse_mode='HTML')
dp   = Dispatcher(bot, loop=loop)

@dp.message_handler(commands= "start")
async def start(message: types.Message):
    await message.bot.send_message(message.from_user.id, "Привет, сбрось описание картины и я её нарисую")

@dp.message_handler()
async def generate_response(message: types.Message):
    DATA_DIR = Path.cwd() / "responses"
    DATA_DIR.mkdir(exist_ok=True)
    PROMPT = message.text
    response = openai.Image.create(
        prompt=PROMPT,
        n=1,
        size="1024x1024",
        response_format="b64_json",
    )

    for index, image_dict in enumerate(response["data"]):
        image_data = b64decode(image_dict["b64_json"])
    await message.answer_photo(image_data)

executor.start_polling(dp)
