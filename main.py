import logging
import asyncio
import qrcode
import random
from io import BytesIO
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

API_TOKEN = "YOUR API KEY"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

logging.basicConfig(level=logging.INFO)

user_data = {}

available_colors = ['black', 'red', 'blue', 'green', 'yellow',
                    'orange', 'purple', 'pink', 'brown', 'gray',
                    'cyan', 'lime', 'teal', 'indigo', 'violet',
                    'magenta', 'gold', 'silver', 'navy']


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот для создания QR-кодов. Пожалуйста, отправьте текст или ссылку для генерации QR-кода. "
                         "Вы также можете использовать команду /help для получения справки.")


@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    help_text = "С помощью этого бота вы можете создавать QR-коды из текста или ссылок и настраивать цвета QR-кода.\n\n" \
                "Чтобы создать QR-код, просто отправьте мне текст или ссылку. " \
                "Для настройки цвета заполнения QR-кода используйте команду /color."
    await message.answer(help_text)


@dp.message_handler(lambda message: message.text and not message.text.startswith('/'))
async def generate_qr_from_text(message: types.Message):
    text = message.text
    fill_color = random.choice(available_colors)
    qr_code = create_qr_code(text, fill_color)
    await send_qr_code(message, qr_code)


@dp.message_handler(commands=['color'])
async def set_fill_color(message: types.Message):
    color = random.choice(available_colors)
    user_id = message.from_user.id
    user_data[user_id] = {'fill_color': color}
    await message.answer(f"Цвет заполнения QR-кода установлен на {color}")


def create_qr_code(text: str, fill_color: str) -> BytesIO:
    back_color = 'white'
 
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color)
    buffer = BytesIO()
    qr_img.save(buffer)
    buffer.seek(0)
    return buffer


async def send_qr_code(message: types.Message, qr_code: BytesIO):
    await message.answer_photo(photo=types.InputFile(qr_code))

if __name__ == '__main__':
    from aiogram import executor
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, loop=loop, skip_updates=True)

