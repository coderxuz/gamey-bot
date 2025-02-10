from aiogram import Bot, Dispatcher, types
from aiogram.types import  CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

TOKEN = "7666311289:AAEe4GfqJdptpqbckXPhXg8-pAKVMS8pLFE"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Sample data for pagination
items = [f"Item {i}" for i in range(1, 21)]  # 20 items

# Function to generate inline keyboard for pagination
def get_pagination_keyboard(page: int, total_pages: int):
    builder = InlineKeyboardBuilder()
    if page > 0:
        builder.button(text="⬅ Previous", callback_data=f"page_{page - 1}")
    if page < total_pages - 1:
        builder.button(text="Next ➡", callback_data=f"page_{page + 1}")
    return builder.as_markup()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    page = 0
    total_pages = len(items)
    text = f"{items[page]}\n\nPage {page + 1} of {total_pages}"
    keyboard = get_pagination_keyboard(page, total_pages)
    await message.answer(text, reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("page_"))
async def pagination_handler(callback: CallbackQuery):
    page = int(callback.data.split("_")[1])
    total_pages = len(items)
    text = f"{items[page]}\n\nPage {page + 1} of {total_pages}"
    keyboard = get_pagination_keyboard(page, total_pages)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())